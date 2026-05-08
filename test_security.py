import requests
import json

BASE = 'https://jsonplaceholder.typicode.com'

results = []

# TC-SEC-001 — Headers de segurança presentes na resposta da API
try:
    r = requests.get(BASE + '/users', headers={'Content-Type': 'application/json'}, timeout=15)
    h = r.headers

    checks = [
        {
            'check': 'X-Content-Type-Options: nosniff',
            'result': 'passed' if h.get('X-Content-Type-Options') == 'nosniff' else 'failed',
            'actual': h.get('X-Content-Type-Options', 'ausente')
        },
        {
            'check': 'X-Frame-Options presente',
            'result': 'passed' if h.get('X-Frame-Options') in ['DENY', 'SAMEORIGIN'] else 'failed',
            'actual': h.get('X-Frame-Options', 'ausente')
        },
        {
            'check': 'Content-Type contém application/json',
            'result': 'passed' if 'application/json' in h.get('Content-Type', '') else 'failed',
            'actual': h.get('Content-Type', 'ausente')
        },
    ]

    all_pass = all(c['result'] == 'passed' for c in checks)

    results.append({
        'id': 'TC-SEC-001',
        'title': 'Headers de segurança presentes na API',
        'status': 'passed' if all_pass else 'failed',
        'checks': checks,
        'severity': None if all_pass else 'medium',
        'error': None if all_pass else 'Um ou mais headers de segurança ausentes — ' + ', '.join(
            c['check'] for c in checks if c['result'] == 'failed'
        )
    })
except Exception as e:
    results.append({
        'id': 'TC-SEC-001',
        'title': 'Headers de segurança presentes na API',
        'status': 'error',
        'checks': [],
        'severity': 'medium',
        'error': str(e)
    })

print(json.dumps(results, ensure_ascii=False, indent=2))
