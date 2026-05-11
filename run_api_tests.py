
import sys, os, json, datetime, time

SUITE_DIR = 'suite_axe_core_db_http_k6_magnitude_playwright_20260511_083909'
os.makedirs(f'{SUITE_DIR}/api', exist_ok=True)

try:
    import requests
except ImportError:
    import subprocess
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'requests'], capture_output=True)
    import requests

def ts():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def run_test(test_id, title, method, url, body=None, headers=None, expected_status=None, validations=None):
    start = time.time()
    logs = []
    error = None
    status = 'passed'
    details = {'method': method, 'url': url, 'status_code': None, 'validations': []}
    try:
        logs.append(f'[REQUEST] {method} {url}')
        resp = requests.request(method, url, json=body, headers=headers or {}, timeout=20, verify=False)
        duration_ms = int((time.time() - start) * 1000)
        details['status_code'] = resp.status_code
        logs.append(f'[RESPONSE] {resp.status_code} -- {duration_ms}ms')
        if expected_status is not None:
            exp_list = expected_status if isinstance(expected_status, list) else [expected_status]
            ok = resp.status_code in exp_list
            r = 'passed' if ok else 'failed'
            details['validations'].append({'check': f'status in {exp_list}', 'result': r})
            logs.append(f'[ASSERT] status {resp.status_code} esperado={exp_list} {"OK" if ok else "FALHOU"}')
            if not ok:
                status = 'failed'
                error = f'Esperado status {exp_list}, recebido {resp.status_code}'
        if validations:
            try:
                body_json = resp.json()
            except Exception:
                body_json = None
            for v in validations:
                vtype = v.get('type')
                field = v.get('field')
                expected = v.get('expected')
                try:
                    val = body_json
                    if field and isinstance(body_json, dict):
                        for p in field.split('.'):
                            val = val.get(p) if isinstance(val, dict) else None
                    if vtype == 'field_equals':
                        ok = val == expected
                    elif vtype == 'field_not_empty':
                        ok = val is not None and val != ''
                    elif vtype == 'field_gt':
                        ok = isinstance(val, (int, float)) and val > expected
                    elif vtype == 'array_not_empty':
                        ok = isinstance(val, list) and len(val) > 0
                    elif vtype == 'array_empty':
                        ok = isinstance(val, list) and len(val) == 0
                    elif vtype == 'array_length':
                        ok = isinstance(val, list) and len(val) == expected
                    elif vtype == 'contains':
                        ok = isinstance(val, str) and expected.lower() in val.lower()
                    elif vtype == 'field_equals_0':
                        ok = val == 0
                    elif vtype == 'is_array':
                        ok = isinstance(body_json, list)
                    elif vtype == 'body_contains':
                        ok = expected.lower() in resp.text.lower()
                    elif vtype == 'field_number_gt':
                        ok = isinstance(val, (int, float)) and val > expected
                    else:
                        ok = True
                    r = 'passed' if ok else 'failed'
                    details['validations'].append({'check': f'{vtype}:{field}:{expected}', 'result': r})
                    logs.append(f'[ASSERT] {vtype} {field}={expected}: got={str(val)[:80]} {"OK" if ok else "FALHOU"}')
                    if not ok:
                        status = 'failed'
                        error = error or f'{field}: esperado {expected}, recebido {str(val)[:80]}'
                except Exception as ve:
                    details['validations'].append({'check': str(v), 'result': 'error'})
                    logs.append(f'[ASSERT ERROR] {ve}')
                    status = 'failed'
                    error = error or str(ve)
        return {'id': test_id, 'title': title, 'status': status,
                'duration_ms': int((time.time()-start)*1000),
                'details': details, 'logs': logs, 'error': error}
    except Exception as e:
        logs.append(f'[ERROR] {str(e)}')
        return {'id': test_id, 'title': title, 'status': 'error',
                'duration_ms': int((time.time()-start)*1000),
                'details': details, 'logs': logs, 'error': str(e)}

results = []
log_lines = [f'[{ts()}] === executor-api -- inicio ===']

# ==================== SWAPI ====================
print('=== SWAPI ===')

r = run_test('TC-API-001','Buscar personagem por ID','GET','https://swapi.dev/api/people/1/',
    expected_status=200,
    validations=[
        {'type':'field_equals','field':'name','expected':'Luke Skywalker'},
        {'type':'field_equals','field':'birth_year','expected':'19BBY'},
        {'type':'field_equals','field':'gender','expected':'male'},
        {'type':'field_not_empty','field':'homeworld'},
        {'type':'array_not_empty','field':'films'},
    ])
results.append(r); print(f'TC-API-001: {r["status"]}')

r = run_test('TC-API-002','ID inexistente 404','GET','https://swapi.dev/api/people/9999/',
    expected_status=404,
    validations=[{'type':'contains','field':'detail','expected':'Not found'}])
results.append(r); print(f'TC-API-002: {r["status"]}')

r = run_test('TC-API-003','Listar filmes','GET','https://swapi.dev/api/films/',
    expected_status=200,
    validations=[
        {'type':'field_gt','field':'count','expected':0},
        {'type':'array_not_empty','field':'results'},
    ])
results.append(r); print(f'TC-API-003: {r["status"]}')

r = run_test('TC-API-004','Busca X-wing','GET','https://swapi.dev/api/starships/?search=X-wing',
    expected_status=200,
    validations=[
        {'type':'field_gt','field':'count','expected':0},
        {'type':'array_not_empty','field':'results'},
    ])
results.append(r); print(f'TC-API-004: {r["status"]}')

r = run_test('TC-API-005','Busca inexistente','GET','https://swapi.dev/api/starships/?search=TERMOINEXISTENTEXXX',
    expected_status=200,
    validations=[
        {'type':'field_equals_0','field':'count'},
        {'type':'array_empty','field':'results'},
    ])
results.append(r); print(f'TC-API-005: {r["status"]}')

r = run_test('TC-API-006','Planeta Tatooine','GET','https://swapi.dev/api/planets/1/',
    expected_status=200,
    validations=[
        {'type':'field_equals','field':'name','expected':'Tatooine'},
        {'type':'field_not_empty','field':'climate'},
        {'type':'field_not_empty','field':'terrain'},
        {'type':'field_not_empty','field':'population'},
    ])
results.append(r); print(f'TC-API-006: {r["status"]}')

# ==================== NASA APOD ====================
print('=== NASA APOD ===')

r = run_test('TC-API-007','APOD com DEMO_KEY','GET','https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY',
    expected_status=200,
    validations=[
        {'type':'field_not_empty','field':'title'},
        {'type':'field_not_empty','field':'url'},
        {'type':'field_not_empty','field':'explanation'},
    ])
results.append(r); print(f'TC-API-007: {r["status"]}')

r = run_test('TC-API-008','APOD data especifica','GET','https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&date=2024-07-04',
    expected_status=200,
    validations=[
        {'type':'field_equals','field':'date','expected':'2024-07-04'},
        {'type':'field_not_empty','field':'title'},
    ])
results.append(r); print(f'TC-API-008: {r["status"]}')

r = run_test('TC-API-009','APOD sem API key','GET','https://api.nasa.gov/planetary/apod',
    expected_status=[400, 403],
    validations=[{'type':'body_contains','expected':'api_key'}])
results.append(r); print(f'TC-API-009: {r["status"]}')

r = run_test('TC-API-010','NEO feed','GET','https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key=DEMO_KEY',
    expected_status=200,
    validations=[
        {'type':'field_gt','field':'element_count','expected':0},
        {'type':'field_not_empty','field':'near_earth_objects'},
    ])
results.append(r); print(f'TC-API-010: {r["status"]}')

# ==================== DummyJSON ====================
print('=== DummyJSON ===')

r_login = run_test('TC-API-011','Login DummyJSON','POST','https://dummyjson.com/auth/login',
    body={'username':'kminchelle','password':'0lelplR'},
    expected_status=200,
    validations=[
        {'type':'field_not_empty','field':'token'},
        {'type':'field_not_empty','field':'refreshToken'},
        {'type':'field_gt','field':'id','expected':0},
        {'type':'field_equals','field':'username','expected':'kminchelle'},
    ])
results.append(r_login); print(f'TC-API-011: {r_login["status"]}')

# Get token from login
dj_token = None
try:
    resp_login = requests.post('https://dummyjson.com/auth/login',
        json={'username':'kminchelle','password':'0lelplR'}, timeout=15)
    if resp_login.status_code == 200:
        dj_token = resp_login.json().get('token') or resp_login.json().get('accessToken')
except Exception:
    pass

r = run_test('TC-API-012','Login senha errada','POST','https://dummyjson.com/auth/login',
    body={'username':'kminchelle','password':'senhaerrada123'},
    expected_status=[400, 401])
results.append(r); print(f'TC-API-012: {r["status"]}')

if dj_token:
    r = run_test('TC-API-013','Perfil autenticado','GET','https://dummyjson.com/auth/me',
        headers={'Authorization': f'Bearer {dj_token}'},
        expected_status=200,
        validations=[{'type':'field_equals','field':'username','expected':'kminchelle'}])
else:
    r = {'id':'TC-API-013','title':'Perfil autenticado','status':'skipped',
         'duration_ms':0,'details':{},'logs':['[SKIP] Token nao obtido'],'error':'Login falhou'}
results.append(r); print(f'TC-API-013: {r["status"]}')

r = run_test('TC-API-014','Rota protegida sem token','GET','https://dummyjson.com/auth/me',
    expected_status=401)
results.append(r); print(f'TC-API-014: {r["status"]}')

if dj_token:
    r = run_test('TC-API-015','Criar produto','POST','https://dummyjson.com/products/add',
        headers={'Authorization': f'Bearer {dj_token}'},
        body={'title':'Produto QA Squad - TC015','price':99.99,'description':'Produto de teste','category':'electronics','thumbnail':'https://placehold.co/300x300'},
        expected_status=[200, 201],
        validations=[
            {'type':'field_gt','field':'id','expected':0},
            {'type':'contains','field':'title','expected':'Produto QA Squad'},
        ])
else:
    r = {'id':'TC-API-015','title':'Criar produto','status':'skipped',
         'duration_ms':0,'details':{},'logs':['[SKIP] Token nao obtido'],'error':'Login falhou'}
results.append(r); print(f'TC-API-015: {r["status"]}')

if dj_token:
    r = run_test('TC-API-016','PATCH produto','PATCH','https://dummyjson.com/products/1',
        headers={'Authorization': f'Bearer {dj_token}'},
        body={'price':149.99},
        expected_status=200,
        validations=[
            {'type':'field_equals','field':'id','expected':1},
        ])
else:
    r = {'id':'TC-API-016','title':'PATCH produto','status':'skipped',
         'duration_ms':0,'details':{},'logs':['[SKIP] Token nao obtido'],'error':'Login falhou'}
results.append(r); print(f'TC-API-016: {r["status"]}')

r = run_test('TC-API-017','Listar produtos publico','GET','https://dummyjson.com/products?limit=5',
    expected_status=200,
    validations=[
        {'type':'array_length','field':'products','expected':5},
        {'type':'field_gt','field':'total','expected':0},
    ])
results.append(r); print(f'TC-API-017: {r["status"]}')

# ==================== Restful-Booker ====================
print('=== Restful-Booker ===')

r_rb_auth = run_test('TC-API-018','Gerar token Restful-Booker','POST','https://restful-booker.herokuapp.com/auth',
    body={'username':'admin','password':'password123'},
    expected_status=200,
    validations=[{'type':'field_not_empty','field':'token'}])
results.append(r_rb_auth); print(f'TC-API-018: {r_rb_auth["status"]}')

rb_token = None
try:
    resp_rb = requests.post('https://restful-booker.herokuapp.com/auth',
        json={'username':'admin','password':'password123'}, timeout=15)
    if resp_rb.status_code == 200:
        rb_token = resp_rb.json().get('token')
        if rb_token == 'Bad credentials':
            rb_token = None
except Exception:
    pass

r = run_test('TC-API-019','Credenciais incorretas','POST','https://restful-booker.herokuapp.com/auth',
    body={'username':'admin','password':'senhaerrada'},
    expected_status=200,
    validations=[{'type':'contains','field':'reason','expected':'Bad credentials'}])
results.append(r); print(f'TC-API-019: {r["status"]}')

r = run_test('TC-API-020','Listar reservas','GET','https://restful-booker.herokuapp.com/booking',
    expected_status=200,
    validations=[{'type':'is_array'}])
results.append(r); print(f'TC-API-020: {r["status"]}')

r_create = run_test('TC-API-021','Criar reserva','POST','https://restful-booker.herokuapp.com/booking',
    headers={'Content-Type':'application/json','Accept':'application/json'},
    body={'firstname':'QA','lastname':'Squad','totalprice':500,'depositpaid':True,
          'bookingdates':{'checkin':'2025-06-01','checkout':'2025-06-07'},'additionalneeds':'Breakfast'},
    expected_status=200,
    validations=[
        {'type':'field_gt','field':'bookingid','expected':0},
    ])
results.append(r_create); print(f'TC-API-021: {r_create["status"]}')

booking_id = None
try:
    resp_c = requests.post('https://restful-booker.herokuapp.com/booking',
        json={'firstname':'QA','lastname':'Squad','totalprice':500,'depositpaid':True,
              'bookingdates':{'checkin':'2025-06-01','checkout':'2025-06-07'},'additionalneeds':'Breakfast'},
        headers={'Content-Type':'application/json','Accept':'application/json'}, timeout=15)
    if resp_c.status_code == 200:
        booking_id = resp_c.json().get('bookingid')
except Exception:
    pass

if booking_id:
    r = run_test('TC-API-022','Ler reserva por ID','GET',f'https://restful-booker.herokuapp.com/booking/{booking_id}',
        headers={'Accept':'application/json'},
        expected_status=200,
        validations=[
            {'type':'field_equals','field':'firstname','expected':'QA'},
            {'type':'field_equals','field':'lastname','expected':'Squad'},
        ])
else:
    r = {'id':'TC-API-022','title':'Ler reserva por ID','status':'skipped',
         'duration_ms':0,'details':{},'logs':['[SKIP] booking_id nao obtido'],'error':'Create falhou'}
results.append(r); print(f'TC-API-022: {r["status"]}')

if booking_id and rb_token:
    r = run_test('TC-API-023','PUT reserva','PUT',f'https://restful-booker.herokuapp.com/booking/{booking_id}',
        headers={'Content-Type':'application/json','Accept':'application/json','Cookie':f'token={rb_token}'},
        body={'firstname':'QA-Atualizado','lastname':'Squad-Atualizado','totalprice':750,'depositpaid':False,
              'bookingdates':{'checkin':'2025-07-01','checkout':'2025-07-10'},'additionalneeds':'Lunch'},
        expected_status=200,
        validations=[
            {'type':'field_equals','field':'firstname','expected':'QA-Atualizado'},
            {'type':'field_equals','field':'totalprice','expected':750},
        ])
else:
    r = {'id':'TC-API-023','title':'PUT reserva','status':'skipped',
         'duration_ms':0,'details':{},'logs':['[SKIP] Token ou booking_id indisponivel'],'error':'Dependencia nao disponivel'}
results.append(r); print(f'TC-API-023: {r["status"]}')

basic_auth = 'YWRtaW46cGFzc3dvcmQxMjM='
if booking_id:
    r = run_test('TC-API-024','PATCH reserva Basic','PATCH',f'https://restful-booker.herokuapp.com/booking/{booking_id}',
        headers={'Content-Type':'application/json','Accept':'application/json','Authorization':f'Basic {basic_auth}'},
        body={'totalprice':900},
        expected_status=200,
        validations=[{'type':'field_equals','field':'totalprice','expected':900}])
else:
    r = {'id':'TC-API-024','title':'PATCH reserva Basic','status':'skipped',
         'duration_ms':0,'details':{},'logs':['[SKIP] booking_id indisponivel'],'error':'Dependencia nao disponivel'}
results.append(r); print(f'TC-API-024: {r["status"]}')

if booking_id and rb_token:
    r = run_test('TC-API-025','DELETE reserva','DELETE',f'https://restful-booker.herokuapp.com/booking/{booking_id}',
        headers={'Cookie':f'token={rb_token}'},
        expected_status=201)
else:
    r = {'id':'TC-API-025','title':'DELETE reserva','status':'skipped',
         'duration_ms':0,'details':{},'logs':['[SKIP] Token ou booking_id indisponivel'],'error':'Dependencia nao disponivel'}
results.append(r); print(f'TC-API-025: {r["status"]}')

if booking_id:
    r = run_test('TC-API-026','Reserva deletada nao existe','GET',f'https://restful-booker.herokuapp.com/booking/{booking_id}',
        headers={'Accept':'application/json'},
        expected_status=404)
else:
    r = {'id':'TC-API-026','title':'Reserva deletada nao existe','status':'skipped',
         'duration_ms':0,'details':{},'logs':['[SKIP] booking_id indisponivel'],'error':'Dependencia nao disponivel'}
results.append(r); print(f'TC-API-026: {r["status"]}')

r = run_test('TC-API-027','DELETE sem token 403','DELETE','https://restful-booker.herokuapp.com/booking/1',
    expected_status=403)
results.append(r); print(f'TC-API-027: {r["status"]}')

r = run_test('TC-API-028','Filtrar reservas','GET','https://restful-booker.herokuapp.com/booking?firstname=QA&lastname=Squad',
    expected_status=200,
    validations=[{'type':'is_array'}])
results.append(r); print(f'TC-API-028: {r["status"]}')

# ==================== SUMMARY ====================
passed = sum(1 for r in results if r['status'] == 'passed')
failed = sum(1 for r in results if r['status'] == 'failed')
skipped = sum(1 for r in results if r['status'] == 'skipped')
error = sum(1 for r in results if r['status'] == 'error')

summary = {'total': len(results), 'passed': passed, 'failed': failed,
           'skipped': skipped, 'error': error, 'credentials_failed': False}

output_json = {
    'executor': 'api',
    'environment': 'swapi.dev|api.nasa.gov|dummyjson.com|restful-booker.herokuapp.com',
    'credentials_failed': False,
    'generated_files': None,
    'results': results,
    'summary': summary
}

with open(f'{SUITE_DIR}/api/resultado.json', 'w', encoding='utf-8') as f:
    json.dump(output_json, f, ensure_ascii=False, indent=2)

log_lines = [f'[{ts()}] === executor-api -- inicio ===']
log_lines.append(f'[{ts()}] Ambientes: swapi.dev, api.nasa.gov, dummyjson.com, restful-booker.herokuapp.com')
for res in results:
    log_lines.append(f'[{ts()}] [{res["id"]}] {res["title"]}')
    for line in (res.get('logs') or []):
        log_lines.append(f'[{ts()}]   {line}')
    log_lines.append(f'[{ts()}]   -> STATUS: {res["status"].upper()}')
log_lines.append(f'[{ts()}] === Fim: {passed} passou, {failed} falhou, {skipped} skipped ===')

with open(f'{SUITE_DIR}/api/execution.log', 'w', encoding='utf-8') as f:
    f.write('\n'.join(log_lines))

print(f'\n=== API SUMMARY: {passed} passed, {failed} failed, {skipped} skipped, {error} error ===')
