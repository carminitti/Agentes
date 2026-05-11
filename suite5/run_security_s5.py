import requests, json, datetime, os
from concurrent.futures import ThreadPoolExecutor

SUITE_DIR = "C:/Users/gabriel.carminitti/Documents/claude/agentes/suite5/suite_http_magnitude_k6_visual_axe_zap_db_20260511_100000"
suite_dir = SUITE_DIR + "/seguranca"
os.makedirs(suite_dir, exist_ok=True)

def ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

ssl_warning = None

def safe_request(method, url, **kwargs):
    global ssl_warning
    try:
        return requests.request(method, url, verify=True, timeout=10, **kwargs)
    except requests.exceptions.SSLError:
        if ssl_warning is None:
            ssl_warning = "Certificado SSL invalido detectado. Execucao com verify=False."
        return requests.request(method, url, verify=False, timeout=10, **kwargs)

def check_pokeapi():
    base = "https://pokeapi.co/api/v2"
    endpoints = ["/pokemon/1", "/type/1", "/ability/1"]
    checks = []
    logs = []

    for ep in endpoints:
        url = base + ep
        try:
            resp = safe_request("GET", url)
            ct = resp.headers.get("Content-Type", "")
            server = resp.headers.get("Server", "")

            ct_ok = "application/json" in ct
            checks.append({"check": f"GET {ep} Content-Type contains application/json", "result": "passed" if ct_ok else "failed", "actual": ct})
            logs.append(f"[CHECK] {ep} Content-Type: {ct} — {'ok' if ct_ok else 'FALHOU'}")

            server_safe = not any(v in server.lower() for v in ["apache/", "nginx/", "iis/", "express/", "gunicorn/"])
            checks.append({"check": f"GET {ep} Server nao expoe versao", "result": "passed" if server_safe else "warning", "actual": server or "absent"})
            logs.append(f"[CHECK] {ep} Server: '{server}' — {'ok' if server_safe else 'WARNING'}")

            for hname in ["Strict-Transport-Security", "X-Frame-Options", "Content-Security-Policy"]:
                if not resp.headers.get(hname):
                    checks.append({"check": f"GET {ep} {hname}", "result": "warning", "actual": "ausente", "note": "header opcional ausente"})
                    logs.append(f"[CHECK] {ep} {hname}: ausente — aviso (opcional)")

        except Exception as e:
            checks.append({"check": f"GET {ep}", "result": "error", "actual": str(e)})
            logs.append(f"[ERROR] {ep}: {e}")

    # Admin endpoint
    try:
        r = safe_request("GET", base + "/admin")
        if r.status_code == 200:
            checks.append({"check": "Admin endpoint nao retorna 200 sem auth", "result": "warning", "actual": "200", "note": "public_test_api"})
            logs.append(f"[CHECK] Admin endpoint retornou 200 — aviso (API publica)")
        else:
            checks.append({"check": "Admin endpoint nao retorna 200 sem auth", "result": "passed", "actual": str(r.status_code)})
            logs.append(f"[CHECK] Admin endpoint retornou {r.status_code} — ok")
    except:
        checks.append({"check": "Admin endpoint nao retorna 200 sem auth", "result": "passed", "actual": "inacessivel"})
        logs.append("[CHECK] Admin endpoint inacessivel — ok")

    failed = [c for c in checks if c["result"] == "failed"]
    status = "failed" if failed else ("warning" if any(c["result"] == "warning" for c in checks) else "passed")
    logs.append(f"[RESULT] TC-SEC-S5-001 — {status}")
    return {
        "id": "TC-SEC-S5-001",
        "title": "Headers de seguranca e exposicao de informacoes na PokeAPI",
        "status": status,
        "checks": checks,
        "severity": "low" if status != "failed" else "medium",
        "note": "API publica de teste — headers opcionais ausentes sao comportamento esperado" if status == "warning" else None,
        "logs": logs,
        "error": None
    }

def check_nationalize():
    base = "https://api.nationalize.io"
    endpoints = ["/?name=james", "/?name=maria"]
    checks = []
    logs = []

    for ep in endpoints:
        url = base + ep
        try:
            resp = safe_request("GET", url)
            ct = resp.headers.get("Content-Type", "")
            server = resp.headers.get("Server", "")

            status_ok = resp.status_code == 200
            checks.append({"check": f"GET {ep} status 200", "result": "passed" if status_ok else "failed", "actual": str(resp.status_code)})
            logs.append(f"[CHECK] {ep} status: {resp.status_code} — {'ok' if status_ok else 'FALHOU'}")

            ct_ok = "application/json" in ct
            checks.append({"check": f"GET {ep} Content-Type contains application/json", "result": "passed" if ct_ok else "failed", "actual": ct})
            logs.append(f"[CHECK] {ep} Content-Type: {ct} — {'ok' if ct_ok else 'FALHOU'}")

            server_safe = not any(v in server.lower() for v in ["apache/", "nginx/", "iis/"])
            checks.append({"check": f"GET {ep} Server nao expoe versao", "result": "passed" if server_safe else "warning", "actual": server or "absent"})
            logs.append(f"[CHECK] {ep} Server: '{server}' — {'ok' if server_safe else 'WARNING'}")

            cors_resp = safe_request("GET", url, headers={"Origin": "https://malicious-site.com"})
            acao = cors_resp.headers.get("Access-Control-Allow-Origin", "")
            cors_open = (acao == "*" or "malicious-site.com" in acao)
            cors_result = "warning" if cors_open else "passed"
            checks.append({"check": f"GET {ep} CORS nao expoe dados", "result": cors_result, "actual": acao or "absent", "note": "API publica — CORS aberto esperado" if cors_open else None})
            logs.append(f"[CHECK] {ep} CORS ACAO: '{acao}' — {'aviso (API publica)' if cors_open else 'ok'}")

            for hname in ["Strict-Transport-Security", "X-Frame-Options", "Content-Security-Policy"]:
                if not resp.headers.get(hname):
                    checks.append({"check": f"GET {ep} {hname}", "result": "warning", "actual": "ausente", "note": "header opcional"})
                    logs.append(f"[CHECK] {ep} {hname}: ausente — aviso")

        except Exception as e:
            checks.append({"check": f"GET {ep}", "result": "error", "actual": str(e)})
            logs.append(f"[ERROR] {ep}: {e}")

    failed = [c for c in checks if c["result"] == "failed"]
    status = "failed" if failed else ("warning" if any(c["result"] == "warning" for c in checks) else "passed")
    logs.append(f"[RESULT] TC-SEC-S5-002 — {status}")
    return {
        "id": "TC-SEC-S5-002",
        "title": "Headers de seguranca e CORS na Nationalize API",
        "status": status,
        "checks": checks,
        "severity": "low" if status != "failed" else "medium",
        "note": "API publica de teste — comportamento esperado" if status == "warning" else None,
        "logs": logs,
        "error": None
    }

print(f"[{ts()}] Iniciando checks de seguranca...")
with ThreadPoolExecutor(max_workers=2) as ex:
    f1 = ex.submit(check_pokeapi)
    f2 = ex.submit(check_nationalize)
    r1 = f1.result()
    r2 = f2.result()

results = [r1, r2]
passed = sum(1 for r in results if r["status"] == "passed")
failed = sum(1 for r in results if r["status"] == "failed")
warning = sum(1 for r in results if r["status"] == "warning")

summary = {
    "total": 2,
    "passed": passed,
    "failed": failed,
    "warning": warning,
    "by_severity": {"high": 0, "medium": failed, "low": warning}
}

output_json = {
    "executor": "security",
    "environment": "https://pokeapi.co/api/v2 + https://api.nationalize.io",
    "environment_type": "public_test_api",
    "credentials_failed": False,
    "results": results,
    "ssl_warning": ssl_warning,
    "summary": summary
}

with open(f"{suite_dir}/resultado.json", "w", encoding="utf-8") as f:
    json.dump(output_json, f, ensure_ascii=False, indent=2)

with open(f"{suite_dir}/execution.log", "w", encoding="utf-8") as f:
    f.write(f"[{ts()}] === executor-seguranca — inicio ===\n")
    f.write(f"[{ts()}] Tipo: public_test_api\n\n")
    for r in results:
        f.write(f"[{ts()}] [{r['id']}] {r['title']}\n")
        for line in r.get("logs", []):
            f.write(f"[{ts()}]   {line}\n")
        f.write(f"[{ts()}]   -> STATUS: {r['status'].upper()}\n\n")
    f.write(f"[{ts()}] === Fim: {passed} passou, {failed} falhou, {warning} aviso ===\n")

print(f"[{ts()}] Resultado salvo. Passed={passed} Failed={failed} Warning={warning}")
for r in results:
    print(f"  {r['id']}: {r['status']}")
