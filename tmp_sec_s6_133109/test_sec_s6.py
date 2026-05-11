# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests, json, os, re, warnings
from datetime import datetime

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

SUITE_DIR = r"C:\Users\gabriel.carminitti\Documents\claude\agentes\suite6\suite_api_browser_k6_visual_axe_zap_db_20260511_132805"
OUTPUT_DIR = os.path.join(SUITE_DIR, "seguranca")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ok_mark(b): return "OK" if b else "FAIL"

results = []
log_lines = [f"[{ts()}] === executor-seguranca -- inicio ===", f"[{ts()}] Modo: analise nao invasiva de headers HTTP"]

OPTIONAL_HEADERS = ["strict-transport-security", "content-security-policy", "x-frame-options",
                    "x-content-type-options", "referrer-policy"]

def check_endpoint(base_url, path):
    url = base_url.rstrip("/") + "/" + path.lstrip("/")
    logs = [f"[REQUEST] GET {url}"]
    checks = []
    warnings_list = []
    blocking_fail = False
    error_msg = None

    try:
        resp = requests.get(url, timeout=10, allow_redirects=True, verify=False)
        logs.append(f"[RESPONSE] {resp.status_code}")
        hdrs = {k.lower(): v for k, v in resp.headers.items()}

        ok_200 = resp.status_code == 200
        checks.append({"check": f"status 200 em {path}", "result": "passed" if ok_200 else "failed", "blocking": True})
        if not ok_200: blocking_fail = True; error_msg = f"Status {resp.status_code} em {path}"
        logs.append(f"[ASSERT] status 200 {ok_mark(ok_200)}")

        ct = hdrs.get("content-type", "")
        ok_ct = "json" in ct.lower()
        chk_ct = {"check": f"Content-Type contem json em {path}", "result": "passed" if ok_ct else "warning", "blocking": False}
        checks.append(chk_ct)
        if not ok_ct: warnings_list.append(f"Content-Type em {path}: '{ct}'")
        logs.append(f"[ASSERT] Content-Type={ct!r} {'OK' if ok_ct else 'AVISO'}")

        server = hdrs.get("server", "")
        version_exposed = bool(re.search(r'\d+\.\d+', server))
        chk_sv = {"check": f"Server nao expoe versao em {path}", "result": "warning" if version_exposed else "passed", "blocking": False}
        checks.append(chk_sv)
        if version_exposed: warnings_list.append(f"Header 'Server' expoe versao: '{server}'")
        logs.append(f"[ASSERT] Server={server!r} {ok_mark(not version_exposed)}")

        for h in OPTIONAL_HEADERS:
            if h not in hdrs:
                warnings_list.append(f"Header opcional ausente: '{h}' em {path}")
                logs.append(f"[WARN] Header '{h}' ausente em {path} (nao bloqueante)")

        body_text = resp.text[:500].lower()
        has_trace = any(k in body_text for k in ["traceback", "exception", "stack trace", "at line", "error in file"])
        checks.append({"check": f"Sem stack trace no body em {path}", "result": "failed" if has_trace else "passed", "blocking": True})
        if has_trace: blocking_fail = True; error_msg = error_msg or f"Stack trace detectado em {path}"
        logs.append(f"[ASSERT] Sem stack trace {ok_mark(not has_trace)}")

    except Exception as e:
        blocking_fail = True; error_msg = str(e)
        logs.append(f"[ERROR] {e}")
        checks.append({"check": f"conexao com {url}", "result": "failed", "blocking": True})

    return checks, warnings_list, logs, blocking_fail, error_msg


def test_advice_slip():
    tc_id = "TC-SEC-S6-001"
    title = "Headers de seguranca e exposicao de dados na Advice Slip API"
    all_checks, all_warnings, all_logs = [], [], []
    overall_fail = False; overall_error = None
    t0 = datetime.now()

    for path in ["/advice", "/advice/search/work"]:
        chks, warns, logs, bf, err = check_endpoint("https://api.adviceslip.com", path)
        all_checks.extend(chks); all_warnings.extend(warns); all_logs.extend(logs)
        if bf: overall_fail = True; overall_error = overall_error or err

    status = "failed" if overall_fail else "passed"
    duration_ms = int((datetime.now() - t0).total_seconds() * 1000)
    all_logs.append(f"-> STATUS: {status.upper()}")
    if all_warnings: all_logs.append(f"[WARN] {len(all_warnings)} avisos nao bloqueantes")

    return {"id": tc_id, "title": title, "status": status, "duration_ms": duration_ms,
            "details": {"validations": all_checks, "warnings": all_warnings},
            "logs": all_logs, "error": overall_error}


def test_open_trivia():
    tc_id = "TC-SEC-S6-002"
    title = "Headers de seguranca e endpoint de token na Open Trivia DB"
    all_checks, all_warnings, all_logs = [], [], []
    overall_fail = False; overall_error = None
    t0 = datetime.now()

    for path in ["/api.php?amount=1", "/api_token.php?command=request"]:
        chks, warns, logs, bf, err = check_endpoint("https://opentdb.com", path)
        all_checks.extend(chks); all_warnings.extend(warns); all_logs.extend(logs)
        if bf: overall_fail = True; overall_error = overall_error or err

    try:
        r1 = requests.get("https://opentdb.com/api_token.php?command=request", timeout=10, verify=False)
        r2 = requests.get("https://opentdb.com/api_token.php?command=request", timeout=10, verify=False)
        if r1.ok and r2.ok:
            t1, t2 = r1.json().get("token", ""), r2.json().get("token", "")
            tokens_diff = t1 != t2
            all_checks.append({"check": "tokens de sessoes diferentes sao unicos", "result": "passed" if tokens_diff else "warning", "blocking": False})
            all_logs.append(f"[ASSERT] tokens unicos por sessao {ok_mark(tokens_diff)}")
            if not tokens_diff: all_warnings.append("Mesmo token gerado para duas requisicoes anonimas consecutivas")
    except Exception as e:
        all_logs.append(f"[WARN] Nao foi possivel verificar unicidade de tokens: {e}")

    status = "failed" if overall_fail else "passed"
    duration_ms = int((datetime.now() - t0).total_seconds() * 1000)
    all_logs.append(f"-> STATUS: {status.upper()}")
    if all_warnings: all_logs.append(f"[WARN] {len(all_warnings)} avisos nao bloqueantes")

    return {"id": tc_id, "title": title, "status": status, "duration_ms": duration_ms,
            "details": {"validations": all_checks, "warnings": all_warnings},
            "logs": all_logs, "error": overall_error}


log_lines.append(f"[{ts()}] Executando TC-SEC-S6-001...")
r1 = test_advice_slip()
results.append(r1)
for l in r1["logs"]: log_lines.append(f"[{ts()}]   {l}")
log_lines.append(f"[{ts()}] [TC-SEC-S6-001] -> {r1['status'].upper()}")

log_lines.append(f"[{ts()}] Executando TC-SEC-S6-002...")
r2 = test_open_trivia()
results.append(r2)
for l in r2["logs"]: log_lines.append(f"[{ts()}]   {l}")
log_lines.append(f"[{ts()}] [TC-SEC-S6-002] -> {r2['status'].upper()}")

passed = sum(1 for r in results if r["status"] == "passed")
failed = sum(1 for r in results if r["status"] == "failed")

summary = {"total": 2, "passed": passed, "failed": failed, "skipped": 0, "credentials_failed": False}
output = {
    "executor": "seguranca",
    "environment": "https://api.adviceslip.com + https://opentdb.com",
    "credentials_failed": False,
    "generated_files": None,
    "results": results,
    "summary": summary
}

log_lines.append(f"[{ts()}] === Fim: {passed} passou, {failed} falhou ===")

with open(os.path.join(OUTPUT_DIR, "resultado.json"), "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
with open(os.path.join(OUTPUT_DIR, "execution.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))

print(json.dumps(output, ensure_ascii=False, indent=2))
