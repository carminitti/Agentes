import requests
import time
import json

BASE = 'https://jsonplaceholder.typicode.com'
HEADERS = {'Content-Type': 'application/json'}

results = []

def val_ok(check, ok, actual=None):
    entry = {'check': check, 'result': 'passed' if ok else 'failed'}
    if not ok and actual is not None:
        entry['actual'] = str(actual)
    return entry, ok

def run_test(id_, title, method, path, body=None, expected_status=None, validations=None, timeout=20):
    url = BASE + path
    try:
        start = time.time()
        if method == 'GET':
            r = requests.get(url, headers=HEADERS, timeout=timeout)
        elif method == 'POST':
            r = requests.post(url, headers=HEADERS, json=body, timeout=timeout)
        elif method == 'PUT':
            r = requests.put(url, headers=HEADERS, json=body, timeout=timeout)
        elif method == 'PATCH':
            r = requests.patch(url, headers=HEADERS, json=body, timeout=timeout)
        elif method == 'DELETE':
            r = requests.delete(url, headers=HEADERS, timeout=timeout)
        duration = round((time.time() - start) * 1000, 2)

        try:
            resp_body = r.json()
        except Exception:
            resp_body = r.text

        checks = []
        all_pass = True

        if expected_status:
            ok = r.status_code == expected_status
            all_pass = all_pass and ok
            e, _ = val_ok(f'status == {expected_status}', ok, r.status_code if not ok else None)
            checks.append(e)

        if validations:
            for vfn in validations:
                chk, ok, actual = vfn(r, resp_body, duration)
                all_pass = all_pass and ok
                e, _ = val_ok(chk, ok, actual if not ok else None)
                checks.append(e)

        results.append({
            'id': id_,
            'title': title,
            'status': 'passed' if all_pass else 'failed',
            'duration_ms': duration,
            'details': {
                'method': method,
                'url': url,
                'status_code': r.status_code,
                'validations': checks
            },
            'error': None if all_pass else next(
                (f"{c['check']} — actual: {c.get('actual','?')}" for c in checks if c['result'] == 'failed'),
                'unknown'
            )
        })
    except Exception as e:
        results.append({
            'id': id_,
            'title': title,
            'status': 'error',
            'duration_ms': None,
            'details': {'method': method, 'url': url},
            'error': str(e)
        })


# TC-AMB-001
run_test(
    'TC-AMB-001', 'API está acessível e respondendo', 'GET', '/users',
    expected_status=200,
    validations=[
        lambda r, b, d: ('tempo < 3000ms', d < 3000, d),
        lambda r, b, d: ('header Content-Type contém application/json', 'application/json' in r.headers.get('Content-Type', ''), r.headers.get('Content-Type', '')),
        lambda r, b, d: ('body é lista não vazia', isinstance(b, list) and len(b) > 0, type(b).__name__),
    ]
)

# TC-USR-001
run_test(
    'TC-USR-001', 'Listar todos os usuários', 'GET', '/users',
    expected_status=200,
    validations=[
        lambda r, b, d: ('retorna 10 usuários', len(b) == 10, len(b)),
        lambda r, b, d: ('cada usuário tem id, name, email, username', all(all(k in u for k in ['id','name','email','username']) for u in b), 'campos faltando'),
    ]
)

# TC-USR-002
run_test(
    'TC-USR-002', 'Buscar usuário existente por ID', 'GET', '/users/1',
    expected_status=200,
    validations=[
        lambda r, b, d: ('id == 1', b.get('id') == 1, b.get('id')),
        lambda r, b, d: ('name == Leanne Graham', b.get('name') == 'Leanne Graham', b.get('name')),
        lambda r, b, d: ('email == Sincere@april.biz', b.get('email') == 'Sincere@april.biz', b.get('email')),
        lambda r, b, d: ('username == Bret', b.get('username') == 'Bret', b.get('username')),
    ]
)

# TC-USR-003
run_test(
    'TC-USR-003', 'Buscar usuário inexistente retorna 404', 'GET', '/users/999',
    expected_status=404,
    validations=[
        lambda r, b, d: ('body é objeto vazio {}', b == {}, b),
    ]
)

# TC-USR-004
run_test(
    'TC-USR-004', 'Criar novo usuário', 'POST', '/users',
    body={'name': 'QA Tester', 'username': 'qa_tester', 'email': 'qa@test.com'},
    expected_status=201,
    validations=[
        lambda r, b, d: ('name == QA Tester', b.get('name') == 'QA Tester', b.get('name')),
        lambda r, b, d: ('id gerado automaticamente', bool(b.get('id')), b.get('id')),
    ]
)

# TC-USR-005
run_test(
    'TC-USR-005', 'Atualizar usuário com PUT', 'PUT', '/users/1',
    body={'id': 1, 'name': 'Leanne Updated', 'username': 'leanne_v2', 'email': 'updated@test.com'},
    expected_status=200,
    validations=[
        lambda r, b, d: ('name == Leanne Updated', b.get('name') == 'Leanne Updated', b.get('name')),
        lambda r, b, d: ('id == 1', b.get('id') == 1, b.get('id')),
    ]
)

# TC-USR-006
run_test(
    'TC-USR-006', 'Atualizar usuário parcialmente com PATCH', 'PATCH', '/users/1',
    body={'name': 'Leanne Patched'},
    expected_status=200,
    validations=[
        lambda r, b, d: ('name == Leanne Patched', b.get('name') == 'Leanne Patched', b.get('name')),
    ]
)

# TC-USR-007
run_test(
    'TC-USR-007', 'Deletar usuário', 'DELETE', '/users/1',
    expected_status=200,
    validations=[
        lambda r, b, d: ('body é objeto vazio {}', b == {}, b),
    ]
)

# TC-POST-001
run_test(
    'TC-POST-001', 'Listar posts do usuário 1', 'GET', '/posts?userId=1',
    expected_status=200,
    validations=[
        lambda r, b, d: ('retorna lista não vazia', isinstance(b, list) and len(b) > 0, len(b) if isinstance(b, list) else 0),
        lambda r, b, d: ('todos os posts pertencem ao userId 1', all(p.get('userId') == 1 for p in b), 'userId divergente'),
        lambda r, b, d: ('cada post tem id, title, body, userId', all(all(k in p for k in ['id','title','body','userId']) for p in b), 'campos faltando'),
    ]
)

# TC-POST-002
run_test(
    'TC-POST-002', 'Buscar post existente por ID', 'GET', '/posts/1',
    expected_status=200,
    validations=[
        lambda r, b, d: ('id == 1', b.get('id') == 1, b.get('id')),
        lambda r, b, d: ('userId == 1', b.get('userId') == 1, b.get('userId')),
        lambda r, b, d: ('title presente e não vazio', bool(b.get('title')), b.get('title')),
        lambda r, b, d: ('body presente e não vazio', bool(b.get('body')), b.get('body')),
    ]
)

# TC-POST-003
run_test(
    'TC-POST-003', 'Criar novo post', 'POST', '/posts',
    body={'title': 'Post de teste', 'body': 'Conteúdo do post', 'userId': 1},
    expected_status=201,
    validations=[
        lambda r, b, d: ('title == Post de teste', b.get('title') == 'Post de teste', b.get('title')),
        lambda r, b, d: ('userId == 1', b.get('userId') == 1, b.get('userId')),
        lambda r, b, d: ('id gerado automaticamente', bool(b.get('id')), b.get('id')),
    ]
)

# TC-COMM-001
run_test(
    'TC-COMM-001', 'Listar comentários do post 1', 'GET', '/comments?postId=1',
    expected_status=200,
    validations=[
        lambda r, b, d: ('retorna lista não vazia', isinstance(b, list) and len(b) > 0, len(b) if isinstance(b, list) else 0),
        lambda r, b, d: ('cada comentário tem id, name, email, body', all(all(k in c for k in ['id','name','email','body']) for c in b), 'campos faltando'),
        lambda r, b, d: ('email de cada comentário é válido', all('@' in c.get('email','') for c in b), 'email inválido'),
    ]
)

# TC-TODO-001
run_test(
    'TC-TODO-001', 'Buscar todo existente por ID', 'GET', '/todos/1',
    expected_status=200,
    validations=[
        lambda r, b, d: ('id == 1', b.get('id') == 1, b.get('id')),
        lambda r, b, d: ('userId presente', bool(b.get('userId')), b.get('userId')),
        lambda r, b, d: ('title presente', bool(b.get('title')), b.get('title')),
        lambda r, b, d: ('completed é booleano', isinstance(b.get('completed'), bool), type(b.get('completed')).__name__),
    ]
)

# TC-TODO-002
run_test(
    'TC-TODO-002', 'Filtrar todos concluídos', 'GET', '/todos?completed=true',
    expected_status=200,
    validations=[
        lambda r, b, d: ('retorna lista não vazia', isinstance(b, list) and len(b) > 0, len(b) if isinstance(b, list) else 0),
        lambda r, b, d: ('todos os itens têm completed == true', all(t.get('completed') is True for t in b), 'item com completed=false encontrado'),
    ]
)

print(json.dumps(results, ensure_ascii=False, indent=2))
