import sqlite3, json, datetime, os

SUITE_DIR = "C:/Users/gabriel.carminitti/Documents/claude/agentes/suite5/suite_http_magnitude_k6_visual_axe_zap_db_20260511_100000"
suite_dir = SUITE_DIR + "/banco"
os.makedirs(suite_dir, exist_ok=True)

def ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

results = []

# ============================================================
# TC-DB-S5-001: Schema financeiro (accounts, transactions, balances)
# ============================================================
def run_tc_db_s5_001():
    logs = []
    logs.append("[CONNECT] Conectando ao banco simulado (SQLite :memory:)")
    conn = sqlite3.connect(":memory:")
    # Habilita FK enforcement
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        logs.append("[SETUP] Criando schema financeiro...")
        cursor.executescript("""
            CREATE TABLE accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_name TEXT NOT NULL,
                account_type TEXT NOT NULL,
                balance REAL NOT NULL CHECK(balance >= 0),
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_account_id INTEGER NOT NULL,
                to_account_id INTEGER NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                transaction_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_account_id) REFERENCES accounts(id),
                FOREIGN KEY (to_account_id) REFERENCES accounts(id)
            );
            CREATE TABLE balances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                computed_balance REAL,
                computed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            );
        """)
        logs.append("[SETUP] Tabelas criadas: accounts, transactions, balances")

        # Verificar tabelas existem
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        tables_ok = set(["accounts", "transactions", "balances"]).issubset(set(tables))
        logs.append(f"[ASSERT] Tabelas criadas: {tables} — {'ok' if tables_ok else 'FALHOU'}")

        # Verificar CHECK balance >= 0
        try:
            cursor.execute("INSERT INTO accounts (owner_name, account_type, balance) VALUES ('Bad', 'checking', -1)")
            conn.commit()
            logs.append("[ASSERT] CHECK balance >= 0 — FALHOU (inseriu saldo negativo)")
            check_balance = False
        except sqlite3.IntegrityError:
            logs.append("[ASSERT] CHECK balance >= 0 ativo — ok (rejeita saldo negativo)")
            check_balance = True
            conn.rollback()

        # Verificar CHECK amount > 0
        cursor.execute("INSERT INTO accounts (owner_name, account_type, balance) VALUES ('Acc1', 'checking', 500)")
        cursor.execute("INSERT INTO accounts (owner_name, account_type, balance) VALUES ('Acc2', 'savings', 1000)")
        conn.commit()
        acc1_id = cursor.lastrowid - 1
        acc2_id = cursor.lastrowid
        try:
            cursor.execute("INSERT INTO transactions (from_account_id, to_account_id, amount) VALUES (?, ?, -100)", (acc1_id, acc2_id))
            conn.commit()
            logs.append("[ASSERT] CHECK amount > 0 — FALHOU (inseriu amount negativo)")
            check_amount = False
        except sqlite3.IntegrityError:
            logs.append("[ASSERT] CHECK amount > 0 ativo — ok (rejeita amount negativo)")
            check_amount = True
            conn.rollback()

        # Verificar FK from_account_id
        try:
            cursor.execute("INSERT INTO transactions (from_account_id, to_account_id, amount) VALUES (9999, ?, 100)", (acc2_id,))
            conn.commit()
            logs.append("[ASSERT] FK from_account_id — FALHOU (inseriu FK inválida sem erro)")
            fk_ok = False
        except sqlite3.IntegrityError:
            logs.append("[ASSERT] FK from_account_id valida — ok (rejeita FK inexistente)")
            fk_ok = True
            conn.rollback()

        # Inserir conta de teste e recuperar
        cursor.execute("INSERT INTO accounts (owner_name, account_type, balance) VALUES ('QA Tester', 'checking', 1000.00)")
        conn.commit()
        qa_id = cursor.lastrowid
        cursor.execute("SELECT owner_name, account_type, balance FROM accounts WHERE id = ?", (qa_id,))
        row = cursor.fetchone()
        select_ok = row is not None and row[0] == "QA Tester" and row[1] == "checking" and abs(row[2] - 1000.00) < 0.001
        logs.append(f"[ASSERT] SELECT conta inserida: {row} — {'ok' if select_ok else 'FALHOU'}")

        all_passed = tables_ok and check_balance and check_amount and fk_ok and select_ok
        status = "passed" if all_passed else "failed"
        logs.append(f"[RESULT] TC-DB-S5-001 — {status}")

        return {
            "id": "TC-DB-S5-001",
            "title": "Integridade do schema financeiro (accounts, transactions, balances)",
            "status": status,
            "simulated": True,
            "query": "CREATE TABLE + INSERT + SELECT + constraint checks",
            "expected": "Tabelas criadas, constraints CHECK e FK funcionando, SELECT retorna dados corretos",
            "actual": f"tables_ok={tables_ok}, check_balance={check_balance}, check_amount={check_amount}, fk_ok={fk_ok}, select_ok={select_ok}",
            "logs": logs,
            "error": None if all_passed else "Uma ou mais verificacoes de schema falharam"
        }
    except Exception as e:
        logs.append(f"[ERROR] {e}")
        return {
            "id": "TC-DB-S5-001",
            "title": "Integridade do schema financeiro (accounts, transactions, balances)",
            "status": "failed",
            "simulated": True,
            "logs": logs,
            "error": str(e)
        }
    finally:
        conn.close()
        logs.append("[DISCONNECT] Conexao encerrada")

# ============================================================
# TC-DB-S5-002: Schema biblioteca (books, authors, loans)
# ============================================================
def run_tc_db_s5_002():
    logs = []
    logs.append("[CONNECT] Conectando ao banco simulado (SQLite :memory:)")
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        logs.append("[SETUP] Criando schema de biblioteca...")
        cursor.executescript("""
            CREATE TABLE authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                nationality TEXT,
                birth_year INTEGER
            );
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                published_year INTEGER,
                available INTEGER NOT NULL DEFAULT 1 CHECK(available IN (0,1)),
                FOREIGN KEY (author_id) REFERENCES authors(id)
            );
            CREATE TABLE loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                borrower_name TEXT NOT NULL,
                loan_date TEXT DEFAULT CURRENT_TIMESTAMP,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books(id)
            );
        """)
        logs.append("[SETUP] Tabelas criadas: authors, books, loans")

        # Verificar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        tables_ok = set(["authors", "books", "loans"]).issubset(set(tables))
        logs.append(f"[ASSERT] Tabelas criadas: {tables} — {'ok' if tables_ok else 'FALHOU'}")

        # FK author_id em books
        try:
            cursor.execute("INSERT INTO books (title, author_id, isbn, published_year, available) VALUES ('TestBook', 9999, 'ISBN-TEST-001', 2020, 1)")
            conn.commit()
            logs.append("[ASSERT] FK author_id — FALHOU (inseriu FK invalida sem erro)")
            fk_author = False
        except sqlite3.IntegrityError:
            logs.append("[ASSERT] FK author_id valida — ok (rejeita author_id inexistente)")
            fk_author = True
            conn.rollback()

        # Inserir autor real
        cursor.execute("INSERT INTO authors (name, nationality, birth_year) VALUES ('Robert C. Martin', 'American', 1952)")
        conn.commit()
        author_id = cursor.lastrowid

        # UNIQUE isbn
        cursor.execute("INSERT INTO books (title, author_id, isbn, published_year, available) VALUES ('Clean Code', ?, 'ISBN-9780132350884', 2008, 1)", (author_id,))
        conn.commit()
        try:
            cursor.execute("INSERT INTO books (title, author_id, isbn, published_year, available) VALUES ('Duplicate', ?, 'ISBN-9780132350884', 2009, 1)", (author_id,))
            conn.commit()
            logs.append("[ASSERT] UNIQUE isbn — FALHOU (inseriu ISBN duplicado)")
            isbn_unique = False
        except sqlite3.IntegrityError:
            logs.append("[ASSERT] UNIQUE isbn ativo — ok (rejeita ISBN duplicado)")
            isbn_unique = True
            conn.rollback()

        # CHECK available IN (0,1)
        try:
            cursor.execute("INSERT INTO books (title, author_id, isbn, published_year, available) VALUES ('BadAvail', ?, 'ISBN-9999', 2020, 5)", (author_id,))
            conn.commit()
            logs.append("[ASSERT] CHECK available IN (0,1) — FALHOU (inseriu available=5)")
            avail_check = False
        except sqlite3.IntegrityError:
            logs.append("[ASSERT] CHECK available IN (0,1) ativo — ok")
            avail_check = True
            conn.rollback()

        # FK book_id em loans
        try:
            cursor.execute("INSERT INTO loans (book_id, borrower_name) VALUES (9999, 'Tester')")
            conn.commit()
            logs.append("[ASSERT] FK book_id em loans — FALHOU (inseriu FK invalida)")
            fk_book = False
        except sqlite3.IntegrityError:
            logs.append("[ASSERT] FK book_id em loans valida — ok")
            fk_book = True
            conn.rollback()

        # SELECT autor inserido
        cursor.execute("SELECT name, nationality, birth_year FROM authors WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        select_ok = row is not None and row[0] == "Robert C. Martin" and row[1] == "American" and row[2] == 1952
        logs.append(f"[ASSERT] SELECT autor: {row} — {'ok' if select_ok else 'FALHOU'}")

        all_passed = tables_ok and fk_author and isbn_unique and avail_check and fk_book and select_ok
        status = "passed" if all_passed else "failed"
        logs.append(f"[RESULT] TC-DB-S5-002 — {status}")

        return {
            "id": "TC-DB-S5-002",
            "title": "Integridade do schema de biblioteca (books, authors, loans)",
            "status": status,
            "simulated": True,
            "query": "CREATE TABLE + INSERT + SELECT + constraint checks",
            "expected": "Tabelas criadas, FK/UNIQUE/CHECK funcionando, SELECT retorna dados corretos",
            "actual": f"tables_ok={tables_ok}, fk_author={fk_author}, isbn_unique={isbn_unique}, avail_check={avail_check}, fk_book={fk_book}, select_ok={select_ok}",
            "logs": logs,
            "error": None if all_passed else "Uma ou mais verificacoes de schema falharam"
        }
    except Exception as e:
        logs.append(f"[ERROR] {e}")
        return {
            "id": "TC-DB-S5-002",
            "title": "Integridade do schema de biblioteca (books, authors, loans)",
            "status": "failed",
            "simulated": True,
            "logs": logs,
            "error": str(e)
        }
    finally:
        conn.close()
        logs.append("[DISCONNECT] Conexao encerrada")

print(f"[{ts()}] Iniciando testes de banco (SQLite :memory:)...")
r1 = run_tc_db_s5_001()
r2 = run_tc_db_s5_002()
results = [r1, r2]

passed = sum(1 for r in results if r["status"] == "passed")
failed = sum(1 for r in results if r["status"] == "failed")

summary = {
    "total": 2,
    "passed": passed,
    "failed": failed,
    "skipped": 0,
    "credentials_failed": False
}

output_json = {
    "executor": "db",
    "environment": "simulado-local",
    "database": "sqlite://:memory:",
    "simulated": True,
    "simulation_note": "Execucao em ambiente simulado (SQLite em memoria). Os dados foram gerados automaticamente com base nos cenarios de teste. Os resultados devem ser revalidados contra o banco real antes do deploy.",
    "credentials_failed": False,
    "results": results,
    "summary": summary
}

with open(f"{suite_dir}/resultado.json", "w", encoding="utf-8") as f:
    json.dump(output_json, f, ensure_ascii=False, indent=2)

with open(f"{suite_dir}/execution.log", "w", encoding="utf-8") as f:
    f.write(f"[{ts()}] === executor-banco — inicio ===\n")
    f.write(f"[{ts()}] Ambiente: sqlite://:memory:\n")
    f.write(f"[{ts()}] Modo: simulado\n\n")
    for r in results:
        f.write(f"[{ts()}] [{r['id']}] {r['title']}\n")
        for line in r.get("logs", []):
            f.write(f"[{ts()}]   {line}\n")
        f.write(f"[{ts()}]   -> STATUS: {r['status'].upper()}\n\n")
    f.write(f"[{ts()}] === Fim: {passed} passou, {failed} falhou ===\n")

print(f"[{ts()}] Resultado salvo. Passed={passed} Failed={failed}")
for r in results:
    print(f"  {r['id']}: {r['status']}")
    if r.get("error"):
        print(f"    ERROR: {r['error']}")
