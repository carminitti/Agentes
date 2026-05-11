
import sys, os, json, datetime, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

SUITE_DIR = 'suite_axe_core_db_http_k6_magnitude_playwright_20260511_083909'
os.makedirs(f'{SUITE_DIR}/seguranca', exist_ok=True)

try:
    import requests
    from requests.exceptions import SSLError
except ImportError:
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'requests'], capture_output=True)
    import requests
    from requests.exceptions import SSLError

def ts():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

ssl_warning = None

def safe_request(method, url, **kwargs):
    global ssl_warning
    try:
        return requests.request(method, url, verify=True, timeout=15, **kwargs)
    except SSLError:
        if ssl_warning is None:
            ssl_warning = 'Certificado SSL invalido detectado. Execucao com verify=False.'
        return requests.request(method, url, verify=False, timeout=15, **kwargs)
    except Exception as e:
        raise e

PUBLIC_TEST_API_DOMAINS = [
    'jsonplaceholder.typicode.com', 'reqres.in', 'swapi.dev', 'swapi.tech',
    'httpbin.org', 'pokeapi.co', 'fakestoreapi.com', 'dummyjson.com',
    'gorest.co.in', 'mockapi.io', 'api.restful-api.dev',
]

results = []

def classify_env(base_url):
    netloc = urlparse(base_url).netloc.lower()
    is_pub = any(d in netloc for d in PUBLIC_TEST_API_DOMAINS)
    return 'public_test_api' if is_pub else 'production'

# ==================== TC-SEC-001: SWAPI headers ====================
def run_sec001():
    start = time.time()
    logs = []
    status = 'passed'
    checks = []
    error = None
    env_type = 'public_test_api'
    try:
        resp = safe_request('GET', 'https://swapi.dev/api/')
        logs.append(f'[CHECK] GET https://swapi.dev/api/ -> {resp.status_code}')
        hdrs = resp.headers
        security_headers = ['Strict-Transport-Security','X-Content-Type-Options','X-Frame-Options','Content-Security-Policy']
        for h in security_headers:
            present = h in hdrs
            r = 'warning' if not present else 'passed'
            checks.append({'check': f'{h} presente', 'result': r,
                           'actual': hdrs.get(h, 'AUSENTE'), 'note': 'API publica de teste -- comportamento esperado' if not present else None})
            logs.append(f'[CHECK] {h}: {"presente" if present else "AUSENTE (warning -- API publica)"} ')
        # Server header
        server = hdrs.get('Server', '')
        import re
        has_version = bool(re.search(r'/[\d.]', server))
        r = 'failed' if has_version else 'passed'
        checks.append({'check': 'Server sem versao detalhada', 'result': r, 'actual': server})
        logs.append(f'[CHECK] Server header: "{server}" -> {"FALHOU" if has_version else "OK"}')
        if has_version:
            status = 'failed'
            error = f'Header Server revela versao: {server}'
        # Only warnings present -- overall is warning not failed
        has_failed = any(c['result'] == 'failed' for c in checks)
        has_warning = any(c['result'] == 'warning' for c in checks)
        if not has_failed and has_warning:
            status = 'warning'
    except Exception as e:
        status = 'error'
        error = str(e)
        logs.append(f'[ERROR] {e}')
    return {'id':'TC-SEC-001','title':'Headers seguranca SWAPI',
            'status': status,'checks':checks,'severity':None,
            'note':'API publica de teste -- headers ausentes sao warning' if status=='warning' else None,
            'logs':logs,'error':error,'duration_ms':int((time.time()-start)*1000)}

# ==================== TC-SEC-002: SWAPI endpoints sensiveis ====================
def run_sec002():
    start = time.time()
    logs = []
    status = 'passed'
    checks = []
    error = None
    sensitive = ['/admin','/.env','/.git','/debug','/config','/swagger','/api-docs']
    for path in sensitive:
        try:
            url = f'https://swapi.dev{path}'
            resp = safe_request('GET', url)
            ok = resp.status_code in [401, 403, 404]
            r = 'passed' if ok else 'failed'
            checks.append({'check': f'GET {path} retorna 401/403/404', 'result': r, 'actual': resp.status_code})
            logs.append(f'[CHECK] GET {path} -> {resp.status_code} {"OK" if ok else "FALHOU"}')
            if not ok:
                status = 'failed'
                error = error or f'Endpoint {path} retornou {resp.status_code}'
        except Exception as e:
            checks.append({'check': f'GET {path}', 'result': 'error', 'actual': str(e)})
            logs.append(f'[ERROR] GET {path}: {e}')
    return {'id':'TC-SEC-002','title':'Endpoints sensiveis SWAPI',
            'status':status,'checks':checks,'severity':'medium' if status=='failed' else None,
            'note':None,'logs':logs,'error':error,'duration_ms':int((time.time()-start)*1000)}

# ==================== TC-SEC-003: SWAPI CORS ====================
def run_sec003():
    start = time.time()
    logs = []
    status = 'passed'
    checks = []
    error = None
    malicious_origin = 'https://malicious-site-teste.com'
    try:
        resp_get = safe_request('GET', 'https://swapi.dev/api/people/',
            headers={'Origin': malicious_origin})
        acao_get = resp_get.headers.get('Access-Control-Allow-Origin', '')
        cors_open_get = (acao_get == '*' or 'malicious-site-teste.com' in acao_get)
        logs.append(f'[CHECK] CORS GET: Access-Control-Allow-Origin = "{acao_get}"')

        resp_opt = safe_request('OPTIONS', 'https://swapi.dev/api/people/',
            headers={'Origin': malicious_origin, 'Access-Control-Request-Method': 'DELETE'})
        acao_opt = resp_opt.headers.get('Access-Control-Allow-Origin', '')
        cors_open_opt = (acao_opt == '*' or 'malicious-site-teste.com' in acao_opt)
        logs.append(f'[CHECK] CORS OPTIONS: Access-Control-Allow-Origin = "{acao_opt}"')

        cors_open = cors_open_get or cors_open_opt
        if cors_open:
            status = 'warning'
            checks.append({'check': 'CORS rejeita origem maliciosa', 'result': 'warning',
                           'actual': acao_get or acao_opt, 'note': 'API publica de teste -- comportamento esperado'})
            logs.append('[CHECK] CORS aceita origem maliciosa -> warning (API publica de teste)')
        else:
            checks.append({'check': 'CORS rejeita origem maliciosa', 'result': 'passed', 'actual': 'rejeitado'})
            logs.append('[CHECK] CORS rejeita origem maliciosa -> passed')
    except Exception as e:
        status = 'error'
        error = str(e)
        logs.append(f'[ERROR] {e}')
    return {'id':'TC-SEC-003','title':'CORS SWAPI',
            'status':status,'checks':checks,'severity':None,
            'note':'API publica de teste -- CORS aberto e esperado' if status=='warning' else None,
            'logs':logs,'error':error,'duration_ms':int((time.time()-start)*1000)}

# ==================== TC-SEC-004: RB 403 sem auth ====================
def run_sec004():
    start = time.time()
    logs = []
    status = 'passed'
    checks = []
    error = None
    try:
        resp = safe_request('DELETE', 'https://restful-booker.herokuapp.com/booking/1')
        ok = resp.status_code == 403
        r = 'passed' if ok else 'failed'
        checks.append({'check': 'DELETE /booking/1 sem auth retorna 403', 'result': r, 'actual': resp.status_code})
        logs.append(f'[CHECK] DELETE /booking/1 sem auth -> {resp.status_code} {"OK" if ok else "FALHOU"}')
        if not ok:
            status = 'failed'
            error = f'Esperado 403, recebido {resp.status_code}'
    except Exception as e:
        status = 'error'
        error = str(e)
        logs.append(f'[ERROR] {e}')
    return {'id':'TC-SEC-004','title':'RB endpoint protegido 403',
            'status':status,'checks':checks,'severity':'high' if status=='failed' else None,
            'note':None,'logs':logs,'error':error,'duration_ms':int((time.time()-start)*1000)}

# ==================== TC-SEC-005: RB token invalido ====================
def run_sec005():
    start = time.time()
    logs = []
    status = 'passed'
    checks = []
    error = None
    try:
        resp = safe_request('DELETE', 'https://restful-booker.herokuapp.com/booking/1',
            headers={'Cookie': 'token=tokeninvalido12345xyz'})
        ok = resp.status_code == 403
        r = 'passed' if ok else 'failed'
        checks.append({'check': 'DELETE com token invalido retorna 403', 'result': r, 'actual': resp.status_code})
        logs.append(f'[CHECK] DELETE com token invalido -> {resp.status_code} {"OK" if ok else "FALHOU"}')
        if not ok:
            status = 'failed'
            error = f'Esperado 403, recebido {resp.status_code}'
    except Exception as e:
        status = 'error'
        error = str(e)
        logs.append(f'[ERROR] {e}')
    return {'id':'TC-SEC-005','title':'RB token invalido rejeitado',
            'status':status,'checks':checks,'severity':'high' if status=='failed' else None,
            'note':None,'logs':logs,'error':error,'duration_ms':int((time.time()-start)*1000)}

# ==================== TC-SEC-006: RB headers ====================
def run_sec006():
    start = time.time()
    logs = []
    status = 'passed'
    checks = []
    error = None
    try:
        resp = safe_request('GET', 'https://restful-booker.herokuapp.com/booking')
        hdrs = resp.headers
        security_headers = ['Strict-Transport-Security','X-Content-Type-Options','X-Frame-Options','Content-Security-Policy']
        for h in security_headers:
            present = h in hdrs
            r = 'failed' if not present else 'passed'
            checks.append({'check': f'{h} presente', 'result': r,
                           'actual': hdrs.get(h, 'AUSENTE'), 'severity': 'medium'})
            logs.append(f'[CHECK] {h}: {"presente" if present else "AUSENTE (medium)"} ')
            if not present:
                status = 'failed'
                error = error or f'Header {h} ausente'
    except Exception as e:
        status = 'error'
        error = str(e)
        logs.append(f'[ERROR] {e}')
    return {'id':'TC-SEC-006','title':'Headers seguranca Restful-Booker',
            'status':status,'checks':checks,'severity':'medium' if status=='failed' else None,
            'note':None,'logs':logs,'error':error,'duration_ms':int((time.time()-start)*1000)}

# ==================== TC-SEC-007: RB CORS preflight ====================
def run_sec007():
    start = time.time()
    logs = []
    status = 'passed'
    checks = []
    error = None
    malicious_origin = 'https://malicious-site-teste.com'
    try:
        resp = safe_request('OPTIONS', 'https://restful-booker.herokuapp.com/booking',
            headers={
                'Origin': malicious_origin,
                'Access-Control-Request-Method': 'DELETE',
                'Access-Control-Request-Headers': 'Authorization'
            })
        acao = resp.headers.get('Access-Control-Allow-Origin', '')
        logs.append(f'[CHECK] OPTIONS CORS: Access-Control-Allow-Origin = "{acao}"')
        ok_wildcard = acao != '*'
        ok_malicious = 'malicious-site-teste.com' not in acao
        checks.append({'check': 'ACAO nao e wildcard', 'result': 'passed' if ok_wildcard else 'failed', 'actual': acao})
        checks.append({'check': 'ACAO nao aceita origem maliciosa', 'result': 'passed' if ok_malicious else 'failed', 'actual': acao})
        logs.append(f'[CHECK] ACAO != * : {"OK" if ok_wildcard else "FALHOU"}')
        logs.append(f'[CHECK] ACAO nao contem malicious : {"OK" if ok_malicious else "FALHOU"}')
        if not ok_wildcard or not ok_malicious:
            status = 'failed'
            error = f'CORS aceita origem maliciosa: {acao}'
    except Exception as e:
        status = 'error'
        error = str(e)
        logs.append(f'[ERROR] {e}')
    return {'id':'TC-SEC-007','title':'CORS preflight Restful-Booker',
            'status':status,'checks':checks,'severity':'high' if status=='failed' else None,
            'note':None,'logs':logs,'error':error,'duration_ms':int((time.time()-start)*1000)}

# ==================== TC-SEC-008: RB endpoints sensiveis ====================
def run_sec008():
    start = time.time()
    logs = []
    status = 'passed'
    checks = []
    error = None
    sensitive = ['/admin','/.env','/debug','/actuator','/metrics','/swagger']
    for path in sensitive:
        try:
            url = f'https://restful-booker.herokuapp.com{path}'
            resp = safe_request('GET', url)
            ok = resp.status_code in [401, 403, 404]
            r = 'passed' if ok else 'failed'
            checks.append({'check': f'GET {path} retorna 401/403/404', 'result': r, 'actual': resp.status_code})
            logs.append(f'[CHECK] GET {path} -> {resp.status_code} {"OK" if ok else "FALHOU"}')
            if not ok:
                status = 'failed'
                error = error or f'Endpoint {path} retornou {resp.status_code}'
        except Exception as e:
            checks.append({'check': f'GET {path}', 'result': 'error', 'actual': str(e)})
            logs.append(f'[ERROR] GET {path}: {e}')
    return {'id':'TC-SEC-008','title':'Endpoints sensiveis Restful-Booker',
            'status':status,'checks':checks,'severity':'high' if status=='failed' else None,
            'note':None,'logs':logs,'error':error,'duration_ms':int((time.time()-start)*1000)}

# ==================== TC-SEC-009: RB campos sensiveis ====================
def run_sec009():
    start = time.time()
    logs = []
    status = 'passed'
    checks = []
    error = None
    try:
        resp = safe_request('GET', 'https://restful-booker.herokuapp.com/booking/1',
            headers={'Accept': 'application/json'})
        ok_status = resp.status_code in [200, 404]
        checks.append({'check': 'status 200 ou 404', 'result': 'passed' if ok_status else 'failed', 'actual': resp.status_code})
        logs.append(f'[CHECK] GET /booking/1 -> {resp.status_code} {"OK" if ok_status else "FALHOU"}')
        if not ok_status:
            status = 'failed'
            error = f'Status inesperado: {resp.status_code}'

        if resp.status_code == 200:
            body_text = resp.text.lower()
            sensitive_fields = ['password', 'cpf', 'ssn', 'credit_card', 'secret']
            for sf in sensitive_fields:
                found = sf in body_text
                r = 'failed' if found else 'passed'
                checks.append({'check': f'campo "{sf}" ausente', 'result': r})
                logs.append(f'[CHECK] campo "{sf}" na resposta: {"ENCONTRADO (FALHOU)" if found else "ausente (OK)"}')
                if found:
                    status = 'failed'
                    error = error or f'Campo sensivel "{sf}" encontrado na resposta'
    except Exception as e:
        status = 'error'
        error = str(e)
        logs.append(f'[ERROR] {e}')
    return {'id':'TC-SEC-009','title':'Resposta GET sem campos sensiveis',
            'status':status,'checks':checks,'severity':'high' if status=='failed' else None,
            'note':None,'logs':logs,'error':error,'duration_ms':int((time.time()-start)*1000)}

# Run all in parallel
check_fns = [run_sec001, run_sec002, run_sec003, run_sec004, run_sec005,
             run_sec006, run_sec007, run_sec008, run_sec009]

results_dict = {}
with ThreadPoolExecutor(max_workers=6) as executor:
    futures = {executor.submit(fn): fn.__name__ for fn in check_fns}
    for future in as_completed(futures):
        try:
            result = future.result()
            results_dict[result['id']] = result
            print(f'{result["id"]}: {result["status"]}')
        except Exception as e:
            print(f'ERROR in {futures[future]}: {e}')

# Order by ID
results_ordered = [results_dict.get(f'TC-SEC-{str(i).zfill(3)}') for i in range(1, 10) if results_dict.get(f'TC-SEC-{str(i).zfill(3)}')]

passed = sum(1 for r in results_ordered if r['status'] == 'passed')
failed = sum(1 for r in results_ordered if r['status'] == 'failed')
warning = sum(1 for r in results_ordered if r['status'] == 'warning')
error_count = sum(1 for r in results_ordered if r['status'] == 'error')

by_severity = {'high': 0, 'medium': 0, 'low': 0}
for r in results_ordered:
    if r['status'] == 'failed' and r.get('severity'):
        sv = r['severity']
        if sv in by_severity:
            by_severity[sv] += 1

summary = {'total': len(results_ordered), 'passed': passed, 'failed': failed,
           'warning': warning, 'error': error_count, 'by_severity': by_severity, 'credentials_failed': False}

output_json = {
    'executor': 'security',
    'environment': 'swapi.dev|restful-booker.herokuapp.com',
    'environment_type': 'mixed (public_test_api + production)',
    'credentials_failed': False,
    'ssl_warning': ssl_warning,
    'generated_files': None,
    'results': results_ordered,
    'summary': summary
}

with open(f'{SUITE_DIR}/seguranca/resultado.json', 'w', encoding='utf-8') as f:
    json.dump(output_json, f, ensure_ascii=False, indent=2)

log_lines = [f'[{ts()}] === executor-seguranca -- inicio ===']
log_lines.append(f'[{ts()}] Ambientes: swapi.dev, restful-booker.herokuapp.com')
for res in results_ordered:
    log_lines.append(f'[{ts()}] [{res["id"]}] {res["title"]}')
    for line in (res.get('logs') or []):
        log_lines.append(f'[{ts()}]   {line}')
    log_lines.append(f'[{ts()}]   -> STATUS: {res["status"].upper()}')
log_lines.append(f'[{ts()}] === Fim: {passed} passou, {failed} falhou, {warning} warning ===')

with open(f'{SUITE_DIR}/seguranca/execution.log', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_lines))

print(f'\n=== SECURITY SUMMARY: {passed} passed, {failed} failed, {warning} warning ===')
