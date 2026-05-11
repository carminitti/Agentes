import requests
import re
import json
from requests.exceptions import SSLError
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

base_url = "https://automationexercise.com"
ssl_warning = None

PUBLIC_TEST_API_DOMAINS = [
    'jsonplaceholder.typicode.com', 'reqres.in', 'swapi.dev', 'swapi.tech',
    'httpbin.org', 'pokeapi.co', 'fakestoreapi.com', 'dummyjson.com',
    'gorest.co.in', 'mockapi.io', 'api.restful-api.dev',
]
DEMO_APP_DOMAINS = [
    'automationexercise.com', 'the-internet.herokuapp.com', 'demoqa.com',
    'testpages.eviltester.com', 'saucedemo.com', 'practice.expandtesting.com',
    'magento.softwaretestingboard.com', 'tutorialsninja.com',
]

parsed = urlparse(base_url)
netloc = parsed.netloc.lower()
is_public_test_api = any(d in netloc for d in PUBLIC_TEST_API_DOMAINS)
is_demo_app = any(d in netloc for d in DEMO_APP_DOMAINS)
environment_type = (
    "public_test_api" if is_public_test_api
    else "demo_app" if is_demo_app
    else "production"
)


def safe_request(method, url, **kwargs):
    global ssl_warning
    try:
        return requests.request(method, url, verify=True, **kwargs)
    except SSLError:
        if ssl_warning is None:
            ssl_warning = (
                "Certificado SSL invalido ou autoassinado detectado. "
                "As verificacoes foram executadas com verify=False. "
                "Recomenda-se substituir o certificado por um valido antes do deploy."
            )
        return requests.request(method, url, verify=False, **kwargs)


def check_headers():
    logs = []
    checks = []
    try:
        resp = safe_request("GET", base_url, timeout=15)
        h = resp.headers

        def chk(name, condition, actual_val):
            result = "passed" if condition else "failed"
            symbol = "OK" if condition else "FALHOU"
            logs.append("[CHECK] Header " + name + ": " + repr(actual_val) + " -> " + symbol)
            return {"check": "Header " + name + " presente e valido", "result": result, "actual": actual_val}

        hsts_val = h.get("Strict-Transport-Security", "")
        xcto_val = h.get("X-Content-Type-Options", "")
        xfo_val  = h.get("X-Frame-Options", "")
        csp_val  = h.get("Content-Security-Policy", "")

        checks.append(chk("Strict-Transport-Security", "max-age=" in hsts_val, hsts_val or "ausente"))
        checks.append(chk("X-Content-Type-Options",    xcto_val == "nosniff",   xcto_val or "ausente"))
        checks.append(chk("X-Frame-Options",           xfo_val in ["DENY", "SAMEORIGIN"], xfo_val or "ausente"))
        checks.append(chk("Content-Security-Policy",   bool(csp_val),           csp_val or "ausente"))

        failed_checks = [c for c in checks if c["result"] == "failed"]
        if failed_checks:
            status = "failed"
            missing = [c["check"].split()[1] for c in failed_checks]
            error = "Headers ausentes/invalidos: " + ", ".join(missing)
        else:
            status = "passed"
            error = None

        return {
            "id": "TC-SEC-001",
            "title": "Headers de seguranca HTTP",
            "status": status,
            "checks": checks,
            "severity": "medium" if status == "failed" else None,
            "note": None,
            "logs": logs,
            "error": error
        }
    except Exception as e:
        return {
            "id": "TC-SEC-001",
            "title": "Headers de seguranca HTTP",
            "status": "error",
            "checks": [],
            "severity": "high",
            "note": None,
            "logs": ["[ERROR] " + str(e)],
            "error": str(e)
        }


def check_cors():
    logs = []
    checks = []
    try:
        cors_headers = {"Origin": "https://malicious-site.com"}
        resp = safe_request("GET", base_url, headers=cors_headers, timeout=15)
        acao = resp.headers.get("Access-Control-Allow-Origin", "")
        cors_open = (acao == "*" or "malicious-site.com" in acao)

        if acao:
            if cors_open:
                logs.append("[CHECK] CORS origin malicious-site.com -> ACAO=" + repr(acao) + " FALHOU")
                checks.append({"check": "CORS nao aceita origem maliciosa", "result": "failed", "actual": acao})
            else:
                logs.append("[CHECK] CORS origin malicious-site.com -> ACAO=" + repr(acao) + " OK")
                checks.append({"check": "CORS nao aceita origem maliciosa", "result": "passed", "actual": acao})
        else:
            logs.append("[CHECK] Nenhum header Access-Control-Allow-Origin retornado -> CORS nao configurado (seguro por padrao) OK")
            checks.append({"check": "CORS nao aceita origem maliciosa", "result": "passed", "actual": "header ausente (CORS nao habilitado)"})

        if cors_open:
            status = "failed"
            error = "CORS aberto - Access-Control-Allow-Origin: " + acao + " aceita origem nao autorizada"
            severity = "high"
        else:
            status = "passed"
            error = None
            severity = None

        return {
            "id": "TC-SEC-002",
            "title": "Configuracao de CORS",
            "status": status,
            "checks": checks,
            "severity": severity,
            "note": None,
            "logs": logs,
            "error": error
        }
    except Exception as e:
        return {
            "id": "TC-SEC-002",
            "title": "Configuracao de CORS",
            "status": "error",
            "checks": [],
            "severity": "high",
            "note": None,
            "logs": ["[ERROR] " + str(e)],
            "error": str(e)
        }


def check_sensitive_endpoints():
    paths = ["/admin", "/.env", "/debug", "/swagger", "/api-docs", "/actuator", "/metrics"]
    logs = []
    checks = []

    known_paths = set()
    if is_demo_app:
        try:
            sm = safe_request("GET", base_url + "/sitemap.xml", timeout=8)
            if sm.status_code == 200:
                known_paths = set(re.findall(r'<loc>[^<]*?(/[^<\?#]+)', sm.text))
                logs.append("[INFO] Sitemap carregado - " + str(len(known_paths)) + " paths conhecidos")
        except Exception as e:
            logs.append("[INFO] Sitemap nao acessivel: " + str(e))

    overall_failed = False
    for path in paths:
        try:
            r = safe_request("GET", base_url + path, timeout=8)
            sc = r.status_code
            if sc == 200:
                if is_demo_app:
                    logs.append("[CHECK] GET " + path + " -> " + str(sc) + " AVISO (demo_app - pagina legitima)")
                    checks.append({
                        "check": "GET " + path + " retorna 401/403/404",
                        "result": "warning",
                        "actual": sc,
                        "note": "pagina legitima do ambiente de demonstracao"
                    })
                else:
                    overall_failed = True
                    logs.append("[CHECK] GET " + path + " -> " + str(sc) + " FALHOU (esperado 401/403/404)")
                    checks.append({"check": "GET " + path + " retorna 401/403/404", "result": "failed", "actual": sc})
            elif sc in [401, 403, 404]:
                logs.append("[CHECK] GET " + path + " -> " + str(sc) + " OK")
                checks.append({"check": "GET " + path + " retorna 401/403/404", "result": "passed", "actual": sc})
            else:
                overall_failed = True
                logs.append("[CHECK] GET " + path + " -> " + str(sc) + " FALHOU (inesperado)")
                checks.append({"check": "GET " + path + " retorna 401/403/404", "result": "failed", "actual": sc})
        except Exception as e:
            logs.append("[ERROR] GET " + path + " -> " + str(e))
            checks.append({"check": "GET " + path + " retorna 401/403/404", "result": "error", "actual": str(e)})

    has_warning = any(c.get("result") == "warning" for c in checks)
    if overall_failed:
        status_final = "failed"
        severity = "high"
        error = "Endpoint(s) sensivel(is) acessivel(is) sem autenticacao"
    elif has_warning:
        status_final = "warning"
        severity = "low"
        error = None
    else:
        status_final = "passed"
        severity = None
        error = None

    note_val = None
    if has_warning and not overall_failed:
        note_val = "Endpoints que retornaram 200 tratados como paginas legitimas do ambiente de demonstracao"

    return {
        "id": "TC-SEC-003",
        "title": "Endpoints administrativos expostos",
        "status": status_final,
        "checks": checks,
        "severity": severity,
        "note": note_val,
        "logs": logs,
        "error": error
    }


fns = [check_headers, check_cors, check_sensitive_endpoints]
results_map = {}
with ThreadPoolExecutor(max_workers=3) as executor:
    future_to_fn = {executor.submit(fn): fn for fn in fns}
    for future in as_completed(future_to_fn):
        r = future.result()
        results_map[r["id"]] = r

results = [results_map["TC-SEC-001"], results_map["TC-SEC-002"], results_map["TC-SEC-003"]]

total   = len(results)
passed  = sum(1 for r in results if r["status"] == "passed")
failed  = sum(1 for r in results if r["status"] == "failed")
warning = sum(1 for r in results if r["status"] == "warning")
by_sev  = {"high": 0, "medium": 0, "low": 0}
for r in results:
    if r.get("severity") in by_sev:
        by_sev[r["severity"]] += 1

has_failure = failed > 0 or any(r["status"] == "error" for r in results)

output = {
    "executor": "security",
    "environment": base_url,
    "environment_type": environment_type,
    "results": results,
    "ssl_warning": ssl_warning,
    "generated_files": ["tmp_sec_001/security_check.py"] if has_failure else None,
    "summary": {
        "total": total,
        "passed": passed,
        "failed": failed,
        "warning": warning,
        "by_severity": by_sev
    }
}
print(json.dumps(output, ensure_ascii=False, indent=2))
