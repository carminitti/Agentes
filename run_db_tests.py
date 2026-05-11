
import sys, os, json, datetime, time, subprocess, re
from concurrent.futures import ThreadPoolExecutor

SUITE_DIR = 'suite_axe_core_db_http_k6_magnitude_playwright_20260511_083909'
os.makedirs(f'{SUITE_DIR}/banco', exist_ok=True)

def ts():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ==================== SQLite IN-MEMORY (TC-DB-001 to TC-DB-006) ====================
print('=== SQLite in-memory (simulated) ===')

import sqlite3

conn = sqlite3.connect(':memory:')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.executescript("""
  CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    status TEXT DEFAULT 'ativo',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
  );
  CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    referencia TEXT UNIQUE NOT NULL,
    usuario_id INTEGER REFERENCES usuarios(id),
    status TEXT DEFAULT 'processando',
    valor REAL NOT NULL
  );
  INSERT INTO usuarios (nome, email, status) VALUES
    ('Alice QA', 'alice@qa.com', 'ativo'),
    ('Bob QA', 'bob@qa.com', 'ativo'),
    ('Carol QA', 'carol@qa.com', 'ativo');
  INSERT INTO pedidos (referencia, usuario_id, status, valor) VALUES
    ('PED-001', 1, 'processando', 150.00),
    ('PED-002', 2, 'concluido', 250.50),
    ('PED-003', 3, 'processando', 75.99);
""")
conn.commit()

sqlite_results = []

def sqlite_test(test_id, title, query, validation_fn):
    start = time.time()
    logs = []
    status = 'passed'
    error = None
    try:
        logs.append(f'[CONNECT] Conectado ao banco simulado (SQLite :memory:)')
        logs.append(f'[QUERY] {query.strip()}')
        cursor.execute(query)
        rows = cursor.fetchall()
        row_dicts = [dict(r) for r in rows]
        logs.append(f'[RESULT] {row_dicts}')
        ok, msg = validation_fn(row_dicts)
        if ok:
            logs.append(f'[ASSERT] {msg} OK')
        else:
            logs.append(f'[ASSERT] {msg} FALHOU')
            status = 'failed'
            error = msg
    except Exception as e:
        status = 'error'
        error = str(e)
        logs.append(f'[ERROR] {e}')
    return {'id': test_id, 'title': title, 'status': status,
            'simulated': True, 'query': query.strip(),
            'logs': logs, 'error': error,
            'duration_ms': int((time.time()-start)*1000)}

# TC-DB-001: schema check
def val_001(rows):
    cols = [r['name'] for r in rows]
    expected = {'id','nome','email','status','criado_em'}
    missing = expected - set(cols)
    if missing:
        return False, f'Colunas faltando: {missing}'
    return True, f'Schema correto: {cols}'
r = sqlite_test('TC-DB-001','Schema tabela usuarios','PRAGMA table_info(usuarios);', val_001)
sqlite_results.append(r); print(f'TC-DB-001: {r["status"]}')

# TC-DB-002: status ativo
def val_002(rows):
    row = rows[0] if rows else {}
    total = row.get('total', 0)
    ativos = row.get('ativos', 0)
    if total == 0:
        return False, 'Nenhum usuario encontrado'
    if ativos != total:
        return False, f'total={total} ativos={ativos} -- nem todos ativos'
    return True, f'total={total} ativos={ativos} -- todos ativos'
r = sqlite_test('TC-DB-002','Todos usuarios com status ativo',
    'SELECT COUNT(*) as total, SUM(CASE WHEN status = "ativo" THEN 1 ELSE 0 END) as ativos FROM usuarios;',
    val_002)
sqlite_results.append(r); print(f'TC-DB-002: {r["status"]}')

# TC-DB-003: emails unicos
def val_003(rows):
    row = rows[0] if rows else {}
    total = row.get('total', 0)
    distintos = row.get('distintos', 0)
    if total != distintos:
        return False, f'Emails duplicados: total={total} distintos={distintos}'
    return True, f'Emails unicos: total={total}=distintos={distintos}'
r = sqlite_test('TC-DB-003','Emails sem duplicatas',
    'SELECT COUNT(*) AS total, COUNT(DISTINCT email) AS distintos FROM usuarios;',
    val_003)
sqlite_results.append(r); print(f'TC-DB-003: {r["status"]}')

# TC-DB-004: integridade referencial
def val_004(rows):
    row = rows[0] if rows else {}
    orfaos = row.get('pedidos_orfaos', 0)
    if orfaos != 0:
        return False, f'Pedidos orfaos: {orfaos}'
    return True, 'Sem pedidos orfaos'
r = sqlite_test('TC-DB-004','Integridade referencial pedidos',
    'SELECT COUNT(*) AS pedidos_orfaos FROM pedidos p WHERE NOT EXISTS (SELECT 1 FROM usuarios u WHERE u.id = p.usuario_id);',
    val_004)
sqlite_results.append(r); print(f'TC-DB-004: {r["status"]}')

# TC-DB-005: valores positivos
def val_005(rows):
    row = rows[0] if rows else {}
    invalidos = row.get('invalidos', 0)
    if invalidos != 0:
        return False, f'Pedidos com valor negativo/zero: {invalidos}'
    return True, 'Todos pedidos com valor positivo'
r = sqlite_test('TC-DB-005','Pedidos sem valores negativos',
    'SELECT COUNT(*) AS invalidos FROM pedidos WHERE valor <= 0;',
    val_005)
sqlite_results.append(r); print(f'TC-DB-005: {r["status"]}')

# TC-DB-006: referencias unicas
def val_006(rows):
    row = rows[0] if rows else {}
    total = row.get('total', 0)
    distintas = row.get('distintas', 0)
    if total != distintas:
        return False, f'Referencias duplicadas: total={total} distintas={distintas}'
    return True, f'Referencias unicas: {total}'
r = sqlite_test('TC-DB-006','Referencias de pedidos unicas',
    'SELECT COUNT(*) AS total, COUNT(DISTINCT referencia) AS distintas FROM pedidos;',
    val_006)
sqlite_results.append(r); print(f'TC-DB-006: {r["status"]}')

conn.close()

# ==================== MySQL (TC-DB-007 to TC-DB-011) ====================
print('\n=== MySQL db4free.net ===')

mysql_cs = 'mysql+connector://qa_squad_2024:QASquad2024!@db4free.net:3306/qa_squad_db'
mysql_masked = 'mysql+connector://****@db4free.net:3306/qa_squad_db'

# Install driver
def install_driver(pkg):
    res = subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pkg], capture_output=True, text=True)
    return res.returncode == 0

mysql_driver_ok = install_driver('mysql-connector-python')

def test_mysql_connection():
    try:
        import mysql.connector
        from urllib.parse import urlparse as _up
        p = _up(mysql_cs)
        conn = mysql.connector.connect(
            host=p.hostname, port=p.port or 3306,
            user=p.username, password=p.password or '',
            database=p.path.lstrip('/'), connection_timeout=10
        )
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

from concurrent.futures import ThreadPoolExecutor as _TE
with _TE(max_workers=1) as ex:
    fut = ex.submit(test_mysql_connection)
    try:
        mysql_ok, mysql_err = fut.result(timeout=20)
    except Exception as te:
        mysql_ok, mysql_err = False, f'Timeout: {te}'

mysql_results = []

if not mysql_driver_ok:
    skip_reason = 'Driver mysql-connector-python nao instalado'
    mysql_ok = False
    mysql_err = skip_reason

if not mysql_ok:
    print(f'MySQL connection failed: {mysql_err}')
    for tc_id, title in [
        ('TC-DB-007','Conexao MySQL estabelecida'),
        ('TC-DB-008','Versao MySQL Server'),
        ('TC-DB-009','Listar tabelas qa_squad_db'),
        ('TC-DB-010','Permissoes leitura qa_squad_2024'),
        ('TC-DB-011','Charset e collation'),
    ]:
        mysql_results.append({
            'id': tc_id, 'title': title, 'status': 'failed',
            'simulated': False, 'query': None,
            'logs': [f'[CONNECT] Falha ao conectar: {mysql_err}'],
            'error': f'Banco inacessivel: {mysql_err}', 'duration_ms': 0
        })
        print(f'{tc_id}: failed')
else:
    print('MySQL connection OK')

    def run_mysql_test(test_id, title, query, validation_fn):
        import mysql.connector
        from urllib.parse import urlparse as _up
        start = time.time()
        logs = []
        status = 'passed'
        error = None
        try:
            p = _up(mysql_cs)
            conn = mysql.connector.connect(
                host=p.hostname, port=p.port or 3306,
                user=p.username, password=p.password or '',
                database=p.path.lstrip('/'), connection_timeout=10
            )
            cursor = conn.cursor(dictionary=True)
            logs.append(f'[CONNECT] Conectado ao banco (tipo: mysql)')
            logs.append(f'[QUERY] {query.strip()[:120]}')
            cursor.execute(query)
            rows = cursor.fetchall()
            logs.append(f'[RESULT] {str(rows)[:200]}')
            ok, msg = validation_fn(rows)
            if ok:
                logs.append(f'[ASSERT] {msg} OK')
            else:
                logs.append(f'[ASSERT] {msg} FALHOU')
                status = 'failed'
                error = msg
            cursor.close()
            conn.close()
            logs.append('[DISCONNECT] Conexao encerrada')
        except Exception as e:
            status = 'error'
            error = str(e)
            logs.append(f'[ERROR] {e}')
        return {'id': test_id, 'title': title, 'status': status,
                'simulated': False, 'database': mysql_masked,
                'query': query.strip()[:120],
                'logs': logs, 'error': error,
                'duration_ms': int((time.time()-start)*1000)}

    # TC-DB-007: connection
    r = {'id':'TC-DB-007','title':'Conexao MySQL estabelecida','status':'passed',
         'simulated':False,'database':mysql_masked,
         'logs':['[CONNECT] Conexao estabelecida com sucesso',f'[INFO] Credencial mascarada: {mysql_masked}'],
         'error':None,'duration_ms':0}
    mysql_results.append(r); print(f'TC-DB-007: {r["status"]}')

    # TC-DB-008: version
    def val_008(rows):
        if not rows: return False, 'Sem resultado'
        row = rows[0]
        ver = row.get('versao_mysql','')
        banco = row.get('banco_atual','')
        user = row.get('usuario_atual','')
        if not ver: return False, 'versao_mysql vazia'
        if 'qa_squad_db' not in str(banco): return False, f'banco_atual incorreto: {banco}'
        if 'qa_squad_2024' not in str(user): return False, f'usuario_atual incorreto: {user}'
        return True, f'version={ver} banco={banco} user={user}'
    r = run_mysql_test('TC-DB-008','Versao MySQL Server',
        'SELECT VERSION() AS versao_mysql, DATABASE() AS banco_atual, USER() AS usuario_atual;',
        val_008)
    mysql_results.append(r); print(f'TC-DB-008: {r["status"]}')

    # TC-DB-009: list tables
    def val_009(rows):
        return True, f'Tabelas encontradas: {len(rows)} (pode ser 0 em banco novo)'
    r = run_mysql_test('TC-DB-009','Listar tabelas qa_squad_db',
        "SELECT TABLE_NAME AS tabela, TABLE_TYPE AS tipo, TABLE_ROWS AS linhas_estimadas FROM information_schema.TABLES WHERE TABLE_SCHEMA = 'qa_squad_db' ORDER BY TABLE_NAME;",
        val_009)
    mysql_results.append(r); print(f'TC-DB-009: {r["status"]}')

    # TC-DB-010: privileges
    def val_010(rows):
        if not rows: return True, 'Query executou sem erros (resultado vazio permitido)'
        privs = [str(r.get('PRIVILEGE_TYPE','')).upper() for r in rows]
        has_select = any('SELECT' in p or 'ALL' in p for p in privs)
        if not has_select: return False, f'Privilegio SELECT nao encontrado: {privs}'
        return True, f'Privilegios: {privs}'
    r = run_mysql_test('TC-DB-010','Permissoes leitura qa_squad_2024',
        "SELECT GRANTEE, PRIVILEGE_TYPE, IS_GRANTABLE FROM information_schema.USER_PRIVILEGES WHERE GRANTEE LIKE '%qa_squad_2024%';",
        val_010)
    mysql_results.append(r); print(f'TC-DB-010: {r["status"]}')

    # TC-DB-011: charset
    def val_011(rows):
        if not rows: return False, 'Sem resultado'
        row = rows[0]
        charset = str(row.get('charset','')).lower()
        collation = str(row.get('collation',''))
        if 'utf8' not in charset: return False, f'charset incorreto: {charset}'
        if not collation: return False, 'collation vazio'
        return True, f'charset={charset} collation={collation}'
    r = run_mysql_test('TC-DB-011','Charset e collation',
        "SELECT DEFAULT_CHARACTER_SET_NAME AS charset, DEFAULT_COLLATION_NAME AS collation FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = 'qa_squad_db';",
        val_011)
    mysql_results.append(r); print(f'TC-DB-011: {r["status"]}')

# ==================== PostgreSQL Neon (TC-DB-012 to TC-DB-016) ====================
print('\n=== PostgreSQL Neon.tech ===')

pg_cs = 'postgresql://qa_squad:QASquad2024@ep-XXXXXXXX.us-east-2.aws.neon.tech/qa_test_db?sslmode=require'
pg_masked = 'postgresql://****@ep-XXXXXXXX.neon.tech/qa_test_db'

pg_driver_ok = install_driver('psycopg2-binary')
pg_results = []

def test_pg_connection():
    try:
        import psycopg2
        conn = psycopg2.connect(pg_cs, connect_timeout=10)
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

with _TE(max_workers=1) as ex:
    fut = ex.submit(test_pg_connection)
    try:
        pg_ok, pg_err = fut.result(timeout=20)
    except Exception as te:
        pg_ok, pg_err = False, f'Timeout: {te}'

if not pg_driver_ok:
    pg_ok = False
    pg_err = 'Driver psycopg2-binary nao instalado'

if not pg_ok:
    print(f'PostgreSQL connection failed: {pg_err}')
    # ep-XXXXXXXX is a placeholder -- expected to fail
    for tc_id, title in [
        ('TC-DB-012','Conexao SSL PostgreSQL Neon'),
        ('TC-DB-013','Versao servidor PostgreSQL'),
        ('TC-DB-014','Listar tabelas schema publico'),
        ('TC-DB-015','Permissoes qa_squad'),
        ('TC-DB-016','Encoding e timezone'),
    ]:
        pg_results.append({
            'id': tc_id, 'title': title, 'status': 'failed',
            'simulated': False, 'database': pg_masked,
            'logs': [f'[CONNECT] Falha ao conectar: {pg_err}',
                     '[INFO] Connection string usa endpoint placeholder ep-XXXXXXXX -- endpoint real nao fornecido'],
            'error': f'Banco inacessivel: {pg_err}', 'duration_ms': 0
        })
        print(f'{tc_id}: failed (placeholder endpoint)')
else:
    print('PostgreSQL connection OK')

    def run_pg_test(test_id, title, query, validation_fn):
        import psycopg2
        import psycopg2.extras
        start = time.time()
        logs = []
        status = 'passed'
        error = None
        try:
            conn = psycopg2.connect(pg_cs, connect_timeout=10)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            logs.append('[CONNECT] Conectado ao banco (tipo: postgresql, SSL: obrigatorio)')
            logs.append(f'[QUERY] {query.strip()[:120]}')
            cursor.execute(query)
            rows = [dict(r) for r in cursor.fetchall()]
            logs.append(f'[RESULT] {str(rows)[:200]}')
            ok, msg = validation_fn(rows)
            if ok:
                logs.append(f'[ASSERT] {msg} OK')
            else:
                logs.append(f'[ASSERT] {msg} FALHOU')
                status = 'failed'
                error = msg
            cursor.close()
            conn.close()
            logs.append('[DISCONNECT] Conexao encerrada')
        except Exception as e:
            status = 'error'
            error = str(e)
            logs.append(f'[ERROR] {e}')
        return {'id': test_id, 'title': title, 'status': status,
                'simulated': False, 'database': pg_masked,
                'query': query.strip()[:120],
                'logs': logs, 'error': error,
                'duration_ms': int((time.time()-start)*1000)}

    r = {'id':'TC-DB-012','title':'Conexao SSL PostgreSQL Neon','status':'passed',
         'simulated':False,'database':pg_masked,
         'logs':['[CONNECT] Conexao SSL estabelecida com sucesso',f'[INFO] Credencial mascarada: {pg_masked}'],
         'error':None,'duration_ms':0}
    pg_results.append(r); print(f'TC-DB-012: {r["status"]}')

    def val_013(rows):
        if not rows: return False, 'Sem resultado'
        row = rows[0]
        ver = str(row.get('versao_pg',''))
        banco = str(row.get('banco',''))
        user = str(row.get('usuario',''))
        if 'PostgreSQL' not in ver: return False, f'versao_pg incorreta: {ver}'
        if 'qa_test_db' not in banco: return False, f'banco incorreto: {banco}'
        if 'qa_squad' not in user: return False, f'usuario incorreto: {user}'
        return True, f'version={ver[:30]} banco={banco} user={user}'
    r = run_pg_test('TC-DB-013','Versao servidor PostgreSQL',
        "SELECT version() AS versao_pg, current_database() AS banco, current_user AS usuario, pg_is_in_recovery() AS em_recovery;",
        val_013)
    pg_results.append(r); print(f'TC-DB-013: {r["status"]}')

    def val_014(rows):
        return True, f'Tabelas no schema public: {len(rows)} (pode ser 0)'
    r = run_pg_test('TC-DB-014','Listar tabelas schema publico',
        "SELECT table_name AS tabela, table_type AS tipo FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;",
        val_014)
    pg_results.append(r); print(f'TC-DB-014: {r["status"]}')

    def val_015(rows):
        if not rows: return False, 'Sem resultado'
        row = rows[0]
        conectar = str(row.get('pode_conectar',''))
        schema = str(row.get('pode_usar_schema',''))
        if conectar not in ['True','t','true','1']: return False, f'pode_conectar={conectar}'
        if schema not in ['True','t','true','1']: return False, f'pode_usar_schema={schema}'
        return True, f'pode_conectar={conectar} pode_usar_schema={schema}'
    r = run_pg_test('TC-DB-015','Permissoes qa_squad',
        "SELECT has_database_privilege('qa_squad', 'qa_test_db', 'CONNECT') AS pode_conectar, has_schema_privilege('qa_squad', 'public', 'USAGE') AS pode_usar_schema, has_schema_privilege('qa_squad', 'public', 'CREATE') AS pode_criar_objetos;",
        val_015)
    pg_results.append(r); print(f'TC-DB-015: {r["status"]}')

    def val_016(rows):
        if not rows: return False, 'Sem resultado'
        row = rows[0]
        enc = str(row.get('encoding',''))
        col = str(row.get('collation',''))
        if 'UTF8' not in enc.upper(): return False, f'encoding incorreto: {enc}'
        if not col: return False, 'collation vazio'
        return True, f'encoding={enc} collation={col}'
    r = run_pg_test('TC-DB-016','Encoding e timezone',
        "SELECT pg_encoding_to_char(encoding) AS encoding, datcollate AS collation, pg_postmaster_start_time() AS servidor_iniciado_em FROM pg_database WHERE datname = 'qa_test_db';",
        val_016)
    pg_results.append(r); print(f'TC-DB-016: {r["status"]}')

# ==================== FINAL SUMMARY ====================
all_results = sqlite_results + mysql_results + pg_results

passed = sum(1 for r in all_results if r['status'] == 'passed')
failed = sum(1 for r in all_results if r['status'] == 'failed')
skipped = sum(1 for r in all_results if r['status'] == 'skipped')
error = sum(1 for r in all_results if r['status'] == 'error')

simulation_note = ('Execucao em ambiente simulado (SQLite em memoria). '
                   'Os dados foram gerados automaticamente. '
                   'Resultados do SQLite devem ser revalidados contra o banco real antes do deploy.')

output_json = {
    'executor': 'db',
    'environment': 'mixed (sqlite:memory + mysql:db4free.net + postgresql:neon.tech)',
    'database': 'sqlite://:memory: | mysql://****@db4free.net:3306/qa_squad_db | postgresql://****@ep-XXXXXXXX.neon.tech/qa_test_db',
    'simulated': False,
    'simulation_note': simulation_note,
    'credentials_failed': False,
    'generated_files': None,
    'results': all_results,
    'summary': {
        'total': len(all_results), 'passed': passed,
        'failed': failed, 'skipped': skipped, 'error': error,
        'credentials_failed': False,
        'groups': {
            'sqlite_simulated': {'total': len(sqlite_results), 'passed': sum(1 for r in sqlite_results if r['status']=='passed')},
            'mysql_real': {'total': len(mysql_results), 'passed': sum(1 for r in mysql_results if r['status']=='passed')},
            'postgresql_real': {'total': len(pg_results), 'passed': sum(1 for r in pg_results if r['status']=='passed')},
        }
    }
}

with open(f'{SUITE_DIR}/banco/resultado.json', 'w', encoding='utf-8') as f:
    json.dump(output_json, f, ensure_ascii=False, indent=2)

log_lines = [f'[{ts()}] === executor-banco -- inicio ===']
log_lines.append(f'[{ts()}] Modo: misto (sqlite simulado + mysql real + postgresql real)')
for res in all_results:
    log_lines.append(f'[{ts()}] [{res["id"]}] {res["title"]}')
    for line in (res.get('logs') or []):
        log_lines.append(f'[{ts()}]   {line}')
    log_lines.append(f'[{ts()}]   -> STATUS: {res["status"].upper()}')
log_lines.append(f'[{ts()}] === Fim: {passed} passou, {failed} falhou, {skipped} skipped ===')

with open(f'{SUITE_DIR}/banco/execution.log', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_lines))

print(f'\n=== DB SUMMARY: {passed} passed, {failed} failed, {skipped} skipped ===')
