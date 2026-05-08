import requests
import time
import json

BASE = 'https://jsonplaceholder.typicode.com'
HEADERS = {'Content-Type': 'application/json'}

results = []

# TC-PERF-001 — GET /posts deve responder em menos de 1500ms (100 registros)
try:
    start = time.time()
    r = requests.get(BASE + '/posts', headers=HEADERS, timeout=15)
    duration = round((time.time() - start) * 1000, 2)

    try:
        body = r.json()
    except Exception:
        body = []

    checks = []
    all_pass = True

    ok_status = r.status_code == 200
    all_pass = all_pass and ok_status
    checks.append({'check': 'status == 200', 'result': 'passed' if ok_status else 'failed', 'actual': r.status_code if not ok_status else None})

    ok_sla = duration < 1500
    all_pass = all_pass and ok_sla
    checks.append({'check': 'tempo de resposta < 1500ms', 'result': 'passed' if ok_sla else 'failed', 'actual': f'{duration}ms' if not ok_sla else None})

    ok_data = isinstance(body, list) and len(body) == 100
    all_pass = all_pass and ok_data
    checks.append({'check': 'retorna 100 posts', 'result': 'passed' if ok_data else 'failed', 'actual': len(body) if isinstance(body, list) else 0})

    results.append({
        'id': 'TC-PERF-001',
        'title': 'GET /posts responde dentro do SLA (p95 < 1500ms)',
        'status': 'passed' if all_pass else 'failed',
        'type': 'performance',
        'duration_ms': duration,
        'metrics': {
            'response_time_ms': duration,
            'status_code': r.status_code,
            'records_returned': len(body) if isinstance(body, list) else 0
        },
        'thresholds': checks,
        'error': None if all_pass else next(
            (c['check'] + ' — actual: ' + str(c.get('actual', '?')) for c in checks if c['result'] == 'failed'),
            'unknown'
        )
    })
except Exception as e:
    results.append({
        'id': 'TC-PERF-001',
        'title': 'GET /posts responde dentro do SLA (p95 < 1500ms)',
        'status': 'error',
        'type': 'performance',
        'duration_ms': None,
        'metrics': {},
        'thresholds': [],
        'error': str(e)
    })

print(json.dumps(results, ensure_ascii=False, indent=2))
