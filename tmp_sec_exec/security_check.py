import requests
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import re as _re

base_url = "https://automationexercise.com"
ssl_warning = None

DEMO_APP_DOMAINS = [
    'automationexercise.com', 'the-internet.herokuapp.com', 'demoqa.com',
    'testpages.eviltester.com', 'saucedemo.com', 'practice.expandtesting.com',
    'magento.softwaretestingboard.com', 'tutorialsninja.com',
]
PUBLIC_TEST_API_DOMAINS = [
    'jsonplaceholder.typicode.com', 'reqres.in', 'swapi.dev', 'swapi.tech',
    'httpbin.org', 'pokeapi.co', 'fakestoreapi.com', 'dummyjson.com',
    'gorest.co.in', 'mockapi.io', 'api.restful-api.dev',
]

parsed = urlparse(base_url)
netloc = parsed.netloc.lower()
is_demo_app = any(d in netloc for d in DEMO_APP_DOMAINS)
is_public_test_api = any(d in netloc for d in PUBLIC_TEST_API_DOMAINS)
environment_type = "demo_app" if is_demo_app else ("public_test_api" if is_public_test_api else "production")

def safe_request(method, url, **kwargs):
    global ssl_warning
    try:
        return requests.request(method, url, verify=True, timeout=15, **kwargs)
    except requests.exceptions.SSLError:
        if ssl_warning is None:
            ssl_warning = "Certificado SSL invalido detectado. Execucao com verify=False."
        return requests.request(method, url, verify=False, timeout=15, **kwargs)

def check_sec_001():
    logs = []
    checks = []
    try:
        r = safe_request("GET", base_url)
        hdrs = r.headers
        logs.append(f"[CHECK] GET {base_url} -> {r.status_code}")

        hsts = "max-age=" in hdrs.get("Strict-Transport-Security", "")
        xcto = hdrs.get("X-Content-Type-Options", "").lower() == "nosniff"
        xfo_val = hdrs.get("X-Frame-Options", "")
        xfo = xfo_val.upper() in ["DENY", "SAMEORIGIN"]
        csp = "Content-Security-Policy" in hdrs

        checks.append({"check": "Strict-Transport-Security com max-age", "result": "passed" if hsts else "warning", "actual": hdrs.get("Strict-Transport-Security", "ausente")})
        checks.append({"check": "X-Content-Type-Options: nosniff", "result": "passed" if xcto else "warning", "actual": hdrs.get("X-Content-Type-Options", "ausente")})
        checks.append({"check": "X-Frame-Options: DENY ou SAMEORIGIN", "result": "passed" if xfo else "warning", "actual": hdrs.get("X-Frame-Options", "ausente")})
        checks.append({"check": "Content-Security-Policy presente", "result": "passed" if csp else "warning", "actual": hdrs.get("Content-Security-Policy", "ausente")})

        for c in checks:
            mark = "OK" if c["result"] == "passed" else "WARN"
            logs.append(f"[CHECK] {c['check']} -> {c['actual']} [{mark}]")

        any_missing = any(c["result"] == "warning" for c in checks)
        overall = "warning" if any_missing else "passed"

        return {
            "id": "TC-SEC-001",
            "title": "Headers de seguranca no AutomationExercise",
            "status": overall,
            "checks": checks,
            "severity": "low" if any_missing else None,
            "note": "Ambiente de demonstracao - headers ausentes como WARNING (nao FAILED)" if any_missing else None,
            "logs": logs,
            "error": None
        }
    except Exception as e:
        return {"id": "TC-SEC-001", "title": "Headers de seguranca no AutomationExercise", "status": "error", "checks": [], "severity": None, "note": None, "logs": logs, "error": str(e)}

def check_sec_002():
    logs = []
    checks = []
    try:
        cors_headers = {"Origin": "https://malicious-site.com"}
        r = safe_request("GET", base_url, headers=cors_headers)
        acao = r.headers.get("Access-Control-Allow-Origin", "")
        logs.append(f"[CHECK] GET {base_url} Origin:malicious-site.com -> ACAO: '{acao}'")

        cors_open = (acao == "*" or "malicious-site.com" in acao)
        check_result = "warning" if cors_open else "passed"
        actual_val = acao if acao else "header ausente (correto)"
        checks.append({
            "check": "Access-Control-Allow-Origin nao reflete origem maliciosa",
            "result": check_result,
            "actual": actual_val
        })

        if cors_open:
            logs.append(f"[CHECK] CORS permissivo detectado (ACAO: {acao}) [WARN] - demo_app, WARNING")
        else:
            logs.append(f"[CHECK] CORS nao reflete origem maliciosa [OK]")

        return {
            "id": "TC-SEC-002",
            "title": "Configuracao de CORS no AutomationExercise",
            "status": "warning" if cors_open else "passed",
            "checks": checks,
            "severity": "low" if cors_open else None,
            "note": "Ambiente de demonstracao - CORS permissivo como WARNING (nao FAILED)" if cors_open else None,
            "logs": logs,
            "error": None
        }
    except Exception as e:
        return {"id": "TC-SEC-002", "title": "Configuracao de CORS no AutomationExercise", "status": "error", "checks": [], "severity": None, "note": None, "logs": logs, "error": str(e)}

def check_sec_003():
    logs = []
    checks = []
    paths = ["/admin", "/.env", "/debug", "/swagger", "/api-docs"]

    known_paths = set()
    try:
        sr = safe_request("GET", f"{base_url}/sitemap.xml")
        if sr.status_code == 200:
            known_paths = set(_re.findall(r'<loc>[^<]*?(/[^<\?#]+)', sr.text))
            logs.append(f"[INFO] Sitemap consultado - {len(known_paths)} paths conhecidos")
    except Exception:
        logs.append("[INFO] Sitemap nao disponivel")

    overall_statuses = []
    for path in paths:
        try:
            r = safe_request("GET", f"{base_url}{path}")
            sc = r.status_code
            if sc == 200:
                status_val = "warning"
                note_val = "pagina legitima do ambiente de demonstracao"
            elif sc in [401, 403, 404, 302, 301]:
                status_val = "passed"
                note_val = None
            else:
                status_val = "warning"
                note_val = f"status inesperado: {sc}"

            logs.append(f"[CHECK] GET {path} -> {sc} -> {status_val}")
            checks.append({"check": f"GET {path}", "result": status_val, "actual": sc, "note": note_val})
            overall_statuses.append(status_val)
        except Exception as e:
            logs.append(f"[CHECK] GET {path} -> ERROR: {e}")
            checks.append({"check": f"GET {path}", "result": "error", "actual": str(e), "note": None})
            overall_statuses.append("error")

    if any(s == "error" for s in overall_statuses):
        overall = "error"
    elif any(s == "failed" for s in overall_statuses):
        overall = "failed"
    elif any(s == "warning" for s in overall_statuses):
        overall = "warning"
    else:
        overall = "passed"

    return {
        "id": "TC-SEC-003",
        "title": "Endpoints sensiveis expostos no AutomationExercise",
        "status": overall,
        "checks": checks,
        "severity": "low" if overall == "warning" else None,
        "note": "Ambiente de demonstracao - endpoints 200 como WARNING" if overall == "warning" else None,
        "logs": logs,
        "error": None
    }

results_map = {}
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        executor.submit(check_sec_001): "TC-SEC-001",
        executor.submit(check_sec_002): "TC-SEC-002",
        executor.submit(check_sec_003): "TC-SEC-003",
    }
    for future in as_completed(futures):
        r = future.result()
        results_map[r["id"]] = r

results_ordered = [results_map.get(k) for k in ["TC-SEC-001","TC-SEC-002","TC-SEC-003"] if results_map.get(k)]

passed = sum(1 for r in results_ordered if r["status"] == "passed")
failed = sum(1 for r in results_ordered if r["status"] == "failed")
warning = sum(1 for r in results_ordered if r["status"] == "warning")
error_count = sum(1 for r in results_ordered if r["status"] == "error")

output = {
    "executor": "security",
    "environment": base_url,
    "environment_type": environment_type,
    "results": results_ordered,
    "ssl_warning": ssl_warning,
    "summary": {
        "total": len(results_ordered),
        "passed": passed,
        "failed": failed,
        "warning": warning,
        "error": error_count,
        "by_severity": {"high": 0, "medium": 0, "low": warning + failed}
    }
}

print(json.dumps(output, ensure_ascii=False, indent=2))
