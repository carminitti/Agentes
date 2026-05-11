import requests
import json
import time
import sys
import io
from requests.exceptions import SSLError, ConnectionError

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

BASE_URL = "https://jsonplaceholder.typicode.com"
ssl_warning = None

def safe_request(method, url, **kwargs):
    global ssl_warning
    try:
        return requests.request(method, url, verify=True, timeout=10, **kwargs)
    except SSLError:
        if ssl_warning is None:
            ssl_warning = (
                "Certificado SSL invalido ou autoassinado detectado. "
                "As verificacoes foram executadas com verify=False. "
                "Recomenda-se substituir o certificado por um valido antes do deploy."
            )
        return requests.request(method, url, verify=False, timeout=10, **kwargs)

results = []

# TC-SEC-001 | Headers de segurança presentes na API
print("[CHECK] Iniciando TC-SEC-001 — Headers de segurança presentes na API")
start = time.time()
try:
    response = safe_request("GET", f"{BASE_URL}/users")
    resp_headers = response.headers
    duration_ms = round((time.time() - start) * 1000, 2)

    checks = []
    logs = []

    # Verificar X-Content-Type-Options == nosniff
    xcto = resp_headers.get("X-Content-Type-Options", "")
    xcto_pass = xcto.lower() == "nosniff"
    checks.append({
        "check": "X-Content-Type-Options == nosniff",
        "result": "passed" if xcto_pass else "failed",
        "actual": xcto if xcto else "ausente"
    })
    if xcto_pass:
        logs.append(f"[CHECK] Header X-Content-Type-Options: nosniff ✓")
    else:
        logs.append(f"[CHECK] Header X-Content-Type-Options ausente ou incorreto — FALHOU (recebido: '{xcto}')")

    # Verificar X-Frame-Options presente (DENY ou SAMEORIGIN)
    xfo = resp_headers.get("X-Frame-Options", "")
    xfo_pass = xfo.upper() in ["DENY", "SAMEORIGIN"]
    checks.append({
        "check": "X-Frame-Options presente (DENY ou SAMEORIGIN)",
        "result": "passed" if xfo_pass else "failed",
        "actual": xfo if xfo else "ausente"
    })
    if xfo_pass:
        logs.append(f"[CHECK] Header X-Frame-Options: {xfo} ✓")
    else:
        logs.append(f"[CHECK] Header X-Frame-Options ausente ou incorreto — FALHOU (recebido: '{xfo}')")

    # Verificar Content-Type contém application/json
    ct = resp_headers.get("Content-Type", "")
    ct_pass = "application/json" in ct.lower()
    checks.append({
        "check": "Content-Type contém application/json",
        "result": "passed" if ct_pass else "failed",
        "actual": ct if ct else "ausente"
    })
    if ct_pass:
        logs.append(f"[CHECK] Header Content-Type contém application/json ✓ (valor: '{ct}')")
    else:
        logs.append(f"[CHECK] Header Content-Type ausente ou incorreto — FALHOU (recebido: '{ct}')")

    all_passed = all(c["result"] == "passed" for c in checks)
    failed_checks = [c for c in checks if c["result"] == "failed"]

    result = {
        "id": "TC-SEC-001",
        "title": "Headers de segurança presentes na API",
        "status": "passed" if all_passed else "failed",
        "duration_ms": duration_ms,
        "checks": checks,
        "severity": None if all_passed else "medium",
        "logs": logs,
        "error": None if all_passed else f"Headers ausentes/incorretos: {', '.join([c['check'] for c in failed_checks])}"
    }
    results.append(result)
    print(f"[STATUS] TC-SEC-001: {'PASSOU' if all_passed else 'FALHOU'} — {len([c for c in checks if c['result']=='passed'])}/{len(checks)} checks")

except ConnectionError as e:
    results.append({
        "id": "TC-SEC-001",
        "title": "Headers de segurança presentes na API",
        "status": "error",
        "duration_ms": 0,
        "checks": [],
        "severity": None,
        "logs": [f"[ERROR] Falha de conexão: {str(e)}"],
        "error": f"Falha de conexão: {str(e)}"
    })
    print(f"[ERROR] TC-SEC-001: Falha de conexão")

passed_count = len([r for r in results if r["status"] == "passed"])
failed_count = len([r for r in results if r["status"] == "failed"])
error_count = len([r for r in results if r["status"] == "error"])

output = {
    "executor": "security",
    "environment": BASE_URL,
    "results": results,
    "ssl_warning": ssl_warning,
    "summary": {
        "total": len(results),
        "passed": passed_count,
        "failed": failed_count,
        "by_severity": {
            "high": 0,
            "medium": failed_count,
            "low": 0
        }
    }
}

print(json.dumps(output, ensure_ascii=False, indent=2))
