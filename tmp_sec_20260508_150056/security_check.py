import requests
from requests.exceptions import SSLError, ConnectionError, Timeout
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time

BASE_URL = "http://localhost:9999"
ssl_warning = None

def safe_request(method, url, **kwargs):
    global ssl_warning
    try:
        return requests.request(method, url, verify=True, **kwargs)
    except SSLError:
        if ssl_warning is None:
            ssl_warning = (
                "Certificado SSL inválido ou autoassinado detectado. "
                "As verificações foram executadas com verify=False. "
                "Recomenda-se substituir o certificado por um válido antes do deploy."
            )
        return requests.request(method, url, verify=False, **kwargs)

def run_checks_parallel(check_fns):
    results = []
    with ThreadPoolExecutor(max_workers=min(len(check_fns), 8)) as executor:
        futures = {executor.submit(fn): fn for fn in check_fns}
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                results.append({
                    "status": "error",
                    "error": f"Exceção não capturada no future: {type(e).__name__}: {e}"
                })
    return results

# ─── TC-S01 — Check 1: autenticação (sem token → 401/403) ───────────────────

def check_autenticacao():
    check_name = "GET / sem token retorna 401 ou 403"
    log = []
    try:
        response = safe_request("GET", f"{BASE_URL}/", timeout=5)
        actual = response.status_code
        if actual in [401, 403]:
            log.append(f"[CHECK] GET / sem token → esperado 401/403, recebido {actual} ✓")
            return {
                "check": check_name,
                "result": "passed",
                "actual": actual,
                "logs": log
            }
        else:
            log.append(f"[CHECK] GET / sem token → esperado 401/403, recebido {actual} — FALHOU")
            return {
                "check": check_name,
                "result": "failed",
                "actual": actual,
                "logs": log
            }
    except (ConnectionError, ConnectionRefusedError, OSError) as e:
        log.append(f"[ERROR] Conexão recusada ao tentar GET /: {type(e).__name__}: {e}")
        return {
            "check": check_name,
            "result": "error",
            "actual": None,
            "error": f"Conexão recusada — ambiente inacessível: {type(e).__name__}",
            "logs": log
        }
    except Timeout as e:
        log.append(f"[ERROR] Timeout ao tentar GET /: {e}")
        return {
            "check": check_name,
            "result": "error",
            "actual": None,
            "error": f"Timeout — ambiente não respondeu",
            "logs": log
        }
    except Exception as e:
        log.append(f"[ERROR] Erro inesperado em GET /: {type(e).__name__}: {e}")
        return {
            "check": check_name,
            "result": "error",
            "actual": None,
            "error": f"Erro inesperado: {type(e).__name__}: {e}",
            "logs": log
        }

# ─── TC-S01 — Check 2: headers de segurança ──────────────────────────────────

def check_security_headers():
    log = []
    header_checks = []
    try:
        response = safe_request("GET", f"{BASE_URL}/", timeout=5)
        resp_headers = response.headers

        hsts_val = resp_headers.get("Strict-Transport-Security", "")
        hsts_ok = "max-age=" in hsts_val
        header_checks.append({
            "check": "Strict-Transport-Security presente com max-age",
            "result": "passed" if hsts_ok else "failed",
            "actual": hsts_val if hsts_val else "ausente"
        })
        if hsts_ok:
            log.append("[CHECK] Header Strict-Transport-Security presente ✓")
        else:
            log.append("[CHECK] Header Strict-Transport-Security ausente ou sem max-age — FALHOU")

        xcto_val = resp_headers.get("X-Content-Type-Options", "")
        xcto_ok = xcto_val == "nosniff"
        header_checks.append({
            "check": "X-Content-Type-Options: nosniff",
            "result": "passed" if xcto_ok else "failed",
            "actual": xcto_val if xcto_val else "ausente"
        })
        if xcto_ok:
            log.append("[CHECK] Header X-Content-Type-Options: nosniff ✓")
        else:
            log.append(f"[CHECK] Header X-Content-Type-Options ausente ou incorreto — FALHOU (recebido: '{xcto_val}')")

        xfo_val = resp_headers.get("X-Frame-Options", "")
        xfo_ok = xfo_val in ["DENY", "SAMEORIGIN"]
        header_checks.append({
            "check": "X-Frame-Options: DENY ou SAMEORIGIN",
            "result": "passed" if xfo_ok else "failed",
            "actual": xfo_val if xfo_val else "ausente"
        })
        if xfo_ok:
            log.append("[CHECK] Header X-Frame-Options presente ✓")
        else:
            log.append(f"[CHECK] Header X-Frame-Options ausente ou incorreto — FALHOU (recebido: '{xfo_val}')")

        csp_val = resp_headers.get("Content-Security-Policy", "")
        csp_ok = bool(csp_val)
        header_checks.append({
            "check": "Content-Security-Policy presente",
            "result": "passed" if csp_ok else "failed",
            "actual": csp_val if csp_val else "ausente"
        })
        if csp_ok:
            log.append("[CHECK] Header Content-Security-Policy presente ✓")
        else:
            log.append("[CHECK] Header Content-Security-Policy ausente — FALHOU")

        return {
            "group": "headers_de_segurança",
            "result": "passed" if all(c["result"] == "passed" for c in header_checks) else "failed",
            "checks": header_checks,
            "logs": log
        }

    except (ConnectionError, ConnectionRefusedError, OSError) as e:
        log.append(f"[ERROR] Conexão recusada ao verificar headers: {type(e).__name__}: {e}")
        return {
            "group": "headers_de_segurança",
            "result": "error",
            "checks": [
                {"check": "Strict-Transport-Security presente com max-age", "result": "error", "actual": None},
                {"check": "X-Content-Type-Options: nosniff", "result": "error", "actual": None},
                {"check": "X-Frame-Options: DENY ou SAMEORIGIN", "result": "error", "actual": None},
                {"check": "Content-Security-Policy presente", "result": "error", "actual": None},
            ],
            "error": f"Conexão recusada — ambiente inacessível: {type(e).__name__}",
            "logs": log
        }
    except Timeout as e:
        log.append(f"[ERROR] Timeout ao verificar headers: {e}")
        return {
            "group": "headers_de_segurança",
            "result": "error",
            "checks": [],
            "error": "Timeout — ambiente não respondeu",
            "logs": log
        }
    except Exception as e:
        log.append(f"[ERROR] Erro inesperado ao verificar headers: {type(e).__name__}: {e}")
        return {
            "group": "headers_de_segurança",
            "result": "error",
            "checks": [],
            "error": f"Erro inesperado: {type(e).__name__}: {e}",
            "logs": log
        }

# ─── Execução paralela ────────────────────────────────────────────────────────

check_fns = [check_autenticacao, check_security_headers]
raw_results = run_checks_parallel(check_fns)

# Normalizar resultado de check_autenticacao
auth_result = next((r for r in raw_results if "check" in r), None)
headers_result = next((r for r in raw_results if "group" in r), None)

# Se run_checks_parallel capturou exceção de um future, pode ter retornado dict com "status"
error_results = [r for r in raw_results if "status" in r and r.get("status") == "error"]

# Montar checks finais do TC-S01
all_checks = []
all_logs = []

if auth_result:
    all_checks.append({
        "check": auth_result["check"],
        "result": auth_result["result"],
        "actual": auth_result.get("actual")
    })
    all_logs.extend(auth_result.get("logs", []))
elif error_results:
    all_checks.append({
        "check": "GET / sem token retorna 401 ou 403",
        "result": "error",
        "actual": None,
        "error": error_results[0].get("error")
    })

if headers_result:
    all_checks.extend(headers_result.get("checks", []))
    all_logs.extend(headers_result.get("logs", []))
elif len(error_results) > 1:
    all_checks.append({
        "check": "Headers de segurança HTTP",
        "result": "error",
        "actual": None,
        "error": error_results[1].get("error")
    })

# Determinar status geral do TC
any_failed = any(c["result"] == "failed" for c in all_checks)
any_error = any(c["result"] == "error" for c in all_checks)
tc_status = "failed" if any_failed else ("error" if any_error else "passed")

# Montar erro consolidado
error_msg = None
if auth_result and auth_result.get("result") == "error":
    error_msg = auth_result.get("error")
elif headers_result and headers_result.get("result") == "error":
    error_msg = headers_result.get("error")

# Severidade
severity = None
if tc_status in ["failed", "error"]:
    severity = "high"

# Resultado final
output = {
    "executor": "security",
    "environment": BASE_URL,
    "results": [
        {
            "id": "TC-S01",
            "title": "Verificar autenticação e headers de segurança",
            "status": tc_status,
            "checks": all_checks,
            "severity": severity,
            "logs": all_logs,
            "error": error_msg
        }
    ],
    "ssl_warning": ssl_warning,
    "summary": {
        "total": 1,
        "passed": 1 if tc_status == "passed" else 0,
        "failed": 1 if tc_status == "failed" else 0,
        "error": 1 if tc_status == "error" else 0,
        "by_severity": {
            "high": 1 if severity == "high" else 0,
            "medium": 0,
            "low": 0
        }
    }
}

print(json.dumps(output, ensure_ascii=False, indent=2))
