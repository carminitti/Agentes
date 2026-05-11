"""
Executor Seguranca - Verificacoes nao invasivas
TC-SEC-001 a TC-SEC-008
"""
import requests
import warnings
import json
import sys

warnings.filterwarnings('ignore')

ssl_warning = None
results = []

def safe_request(method, url, **kwargs):
    global ssl_warning
    from requests.exceptions import SSLError
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
    except Exception as e:
        raise e

def run_test(tc_id, title, fn):
    try:
        status, checks, logs, severity = fn()
        results.append({
            "id": tc_id,
            "title": title,
            "status": status,
            "checks": checks,
            "severity": severity,
            "logs": logs,
            "error": None if status == "passed" else (checks[-1].get("detail", "") if checks else "")
        })
    except Exception as e:
        results.append({
            "id": tc_id,
            "title": title,
            "status": "failed",
            "checks": [],
            "severity": "high",
            "logs": [f"[ERROR] {str(e)}"],
            "error": str(e)
        })

# TC-SEC-001: Headers de seguranca no JSONPlaceholder
def test_001():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    logs = [f"[CHECK] GET {url}"]
    r = safe_request("GET", url, timeout=10)
    logs.append(f"[RESPONSE] {r.status_code}")
    h = r.headers
    checks = []
    all_pass = True
    for header in ["X-Content-Type-Options", "X-Frame-Options", "Strict-Transport-Security", "Content-Security-Policy"]:
        present = header in h
        status = "passed" if present else "failed"
        if not present:
            all_pass = False
        checks.append({"check": f"{header} presente", "result": status, "actual": h.get(header, "AUSENTE")})
        icon = "OK" if present else "FAIL"
        logs.append(f"[CHECK] Header {header}: {icon}")
    return ("passed" if all_pass else "failed"), checks, logs, ("medium" if not all_pass else None)

run_test("TC-SEC-001", "Headers de seguranca no JSONPlaceholder", test_001)

# TC-SEC-002: CORS com origem maliciosa no JSONPlaceholder
def test_002():
    url = "https://jsonplaceholder.typicode.com/posts"
    logs = [f"[CHECK] GET {url} com Origin: https://evil-site.com"]
    r = safe_request("GET", url, headers={"Origin": "https://evil-site.com"}, timeout=10)
    acao = r.headers.get("Access-Control-Allow-Origin", "")
    logs.append(f"[CHECK] Access-Control-Allow-Origin: '{acao}'")
    checks = []
    if acao == "*":
        checks.append({"check": "CORS aberto (*)", "result": "warning", "actual": "*"})
        logs.append("[WARNING] CORS aberto (*) - esperado para API publica sem dados sensiveis")
        return "warning", checks, logs, "low"
    elif "evil-site.com" in acao:
        checks.append({"check": "Origem maliciosa refletida", "result": "failed", "actual": acao})
        logs.append("[FAIL] Origem maliciosa refletida no CORS")
        return "failed", checks, logs, "high"
    else:
        checks.append({"check": "CORS nao reflete origem maliciosa", "result": "passed", "actual": acao})
        logs.append("[OK] CORS nao reflete evil-site.com")
        return "passed", checks, logs, None

run_test("TC-SEC-002", "CORS com origem maliciosa no JSONPlaceholder", test_002)

# TC-SEC-003: API de notas exige auth
def test_003():
    url = "https://practice.expandtesting.com/notes/api/notes"
    logs = [f"[CHECK] GET {url} sem x-auth-token"]
    r = safe_request("GET", url, timeout=10)
    logs.append(f"[RESPONSE] {r.status_code}")
    checks = [{"check": "GET /notes sem token retorna 401", "result": "passed" if r.status_code == 401 else "failed", "actual": r.status_code}]
    if r.status_code == 401:
        logs.append("[OK] endpoint protegido corretamente - autenticacao exigida")
        return "passed", checks, logs, None
    else:
        logs.append(f"[FAIL] esperado 401, recebido {r.status_code}")
        return "failed", checks, logs, "high"

run_test("TC-SEC-003", "API de notas exige auth em endpoint protegido", test_003)

# TC-SEC-004: DELETE sem auth retorna 401
def test_004():
    url = "https://practice.expandtesting.com/notes/api/notes/qualquer-id"
    logs = [f"[CHECK] DELETE {url} sem x-auth-token"]
    r = safe_request("DELETE", url, timeout=10)
    logs.append(f"[RESPONSE] {r.status_code}")
    checks = [{"check": "DELETE sem token retorna 401", "result": "passed" if r.status_code == 401 else "failed", "actual": r.status_code}]
    if r.status_code == 401:
        logs.append("[OK] DELETE protegido corretamente")
        return "passed", checks, logs, None
    else:
        logs.append(f"[FAIL] esperado 401, recebido {r.status_code}")
        return "failed", checks, logs, "high"

run_test("TC-SEC-004", "DELETE sem auth retorna 401 no Practice Expand", test_004)

# TC-SEC-005: Caminhos administrativos no AutomationExercise
def test_005():
    base = "https://automationexercise.com"
    paths = ["/admin", "/.env", "/config", "/internal", "/debug", "/phpinfo.php"]
    logs = []
    checks = []
    all_pass = True
    for path in paths:
        url = base + path
        try:
            r = safe_request("GET", url, timeout=8, allow_redirects=True)
            final_status = r.status_code
            ok = final_status in [403, 404]
            if not ok:
                all_pass = False
            checks.append({"check": f"GET {path}", "result": "passed" if ok else "failed", "actual": final_status})
            icon = "OK" if ok else "FAIL-VULNERABILIDADE-CRITICA"
            logs.append(f"[CHECK] GET {path} -> {final_status}: {icon}")
        except Exception as e:
            checks.append({"check": f"GET {path}", "result": "error", "actual": str(e)})
            logs.append(f"[CHECK] GET {path} -> ERROR: {e}")
    return ("passed" if all_pass else "failed"), checks, logs, ("high" if not all_pass else None)

run_test("TC-SEC-005", "Caminhos administrativos nao expostos no AutomationExercise", test_005)

# TC-SEC-006: Ausencia de stack trace em 404 do JSONPlaceholder
def test_006():
    url = "https://jsonplaceholder.typicode.com/posts/99999"
    logs = [f"[CHECK] GET {url}"]
    r = safe_request("GET", url, timeout=10)
    logs.append(f"[RESPONSE] {r.status_code}")
    checks = []
    ok_status = r.status_code == 404
    checks.append({"check": "status 404", "result": "passed" if ok_status else "failed", "actual": r.status_code})
    if not ok_status:
        return "failed", checks, logs, "medium"
    logs.append("[OK] status 404 correto")
    body = r.text.lower()
    bad_terms = ["stack", "traceback", "exception", "at com."]
    found_any = False
    for term in bad_terms:
        if term in body:
            found_any = True
            checks.append({"check": f"body nao contem '{term}'", "result": "failed", "actual": f"'{term}' encontrado"})
            logs.append(f"[FAIL] body contem '{term}'")
        else:
            checks.append({"check": f"body nao contem '{term}'", "result": "passed", "actual": "ausente"})
            logs.append(f"[OK] body nao contem '{term}'")
    if not found_any:
        logs.append("[OK] sem exposicao de stack trace")
        return "passed", checks, logs, None
    else:
        return "failed", checks, logs, "medium"

run_test("TC-SEC-006", "Ausencia de stack trace em erro 404 no JSONPlaceholder", test_006)

# TC-SEC-007: Lidar com certificado SSL invalido sem abortar
def test_007():
    # Simulamos o cenario usando practice.expandtesting.com que tem cert issues
    url = "https://practice.expandtesting.com/notes/api/health-check"
    logs = [f"[CHECK] GET {url} com verify=True (pode ter SSLError)"]
    r = safe_request("GET", url, timeout=10)
    logs.append(f"[RESPONSE] {r.status_code}")
    checks = []
    if ssl_warning:
        checks.append({"check": "SSL invalido tratado sem abort", "result": "passed", "actual": "warning registrado"})
        logs.append(f"[SSL] WARNING: {ssl_warning}")
    else:
        checks.append({"check": "Requisicao HTTPS completada", "result": "passed", "actual": r.status_code})
        logs.append("[OK] Requisicao HTTPS completada normalmente")
    return "warning" if ssl_warning else "passed", checks, logs, None

run_test("TC-SEC-007", "Lidar com certificado SSL invalido sem abortar", test_007)

# TC-SEC-008: AutomationExercise forca HTTPS
def test_008():
    url = "http://automationexercise.com"
    logs = [f"[CHECK] GET {url} (HTTP sem HTTPS)"]
    try:
        r = requests.get(url, timeout=10, verify=False, allow_redirects=True)
        final_url = r.url
        logs.append(f"[RESPONSE] {r.status_code} — URL final: {final_url}")
        is_https = final_url.startswith("https://")
        checks = [{"check": "URL final usa HTTPS", "result": "passed" if is_https else "failed", "actual": final_url}]
        if is_https:
            logs.append("[OK] redirecionamento para HTTPS confirmado")
            return "passed", checks, logs, None
        else:
            logs.append("[FAIL] URL final nao usa HTTPS")
            return "failed", checks, logs, "medium"
    except Exception as e:
        checks = [{"check": "Acesso HTTP", "result": "error", "actual": str(e)}]
        logs.append(f"[ERROR] {e}")
        return "failed", checks, logs, "medium"

run_test("TC-SEC-008", "AutomationExercise forca HTTPS", test_008)

# Output
passed = sum(1 for r in results if r["status"] == "passed")
failed = sum(1 for r in results if r["status"] == "failed")
warning = sum(1 for r in results if r["status"] == "warning")

output = {
    "executor": "security",
    "environment": "multiple (JSONPlaceholder / Practice Expand / AutomationExercise)",
    "results": results,
    "ssl_warning": ssl_warning,
    "summary": {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "warning": warning,
        "by_severity": {
            "high": sum(1 for r in results if r.get("severity") == "high"),
            "medium": sum(1 for r in results if r.get("severity") == "medium"),
            "low": sum(1 for r in results if r.get("severity") == "low")
        }
    }
}

sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps(output, indent=2, ensure_ascii=True))
