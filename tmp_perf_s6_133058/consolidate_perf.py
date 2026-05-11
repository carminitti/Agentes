# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import json, os
from datetime import datetime

SUITE_DIR = r"C:\Users\gabriel.carminitti\Documents\claude\agentes\suite6\suite_api_browser_k6_visual_axe_zap_db_20260511_132805"
OUTPUT_DIR = os.path.join(SUITE_DIR, "performance")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def read_k6_metrics(path):
    metrics = {}
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                try:
                    obj = json.loads(line)
                    if obj.get('type') == 'Point':
                        m = obj.get('metric', '')
                        if m not in metrics: metrics[m] = []
                        metrics[m].append(obj['data']['value'])
                except: pass
    except Exception as e:
        print(f"ERRO ao ler {path}: {e}")
    return metrics

log_lines = [f"[{ts()}] === executor-performance -- inicio ==="]
results = []

# TC-PERF-S6-001: Advice Slip API — 8 VUs / 25s
m1 = read_k6_metrics(r"C:\Users\gabriel.carminitti\Documents\claude\agentes\tmp_perf_s6_133058\k6_out_001.json")
durs1 = sorted(m1.get('http_req_duration', []))
fails1 = m1.get('http_req_failed', [])
p95_1 = durs1[int(len(durs1)*0.95)] if durs1 else 9999
avg1 = sum(durs1)/len(durs1) if durs1 else 0
err_rate_1 = sum(fails1)/len(fails1)*100 if fails1 else 0
reqs1 = len(durs1)

passed1 = p95_1 < 3000 and err_rate_1 < 2
status1 = "passed" if passed1 else "failed"

log_lines.append(f"[{ts()}] TC-PERF-S6-001: p95={p95_1:.0f}ms avg={avg1:.0f}ms err={err_rate_1:.2f}% reqs={reqs1}")
log_lines.append(f"[{ts()}] TC-PERF-S6-001 -> {status1.upper()}")

validations1 = [
    {"check": f"p95={p95_1:.0f}ms < 3000ms", "result": "passed" if p95_1 < 3000 else "failed"},
    {"check": f"taxa_erro={err_rate_1:.2f}% < 2%", "result": "passed" if err_rate_1 < 2 else "failed"},
    {"check": f"requisicoes={reqs1} executadas", "result": "passed" if reqs1 > 0 else "failed"},
]

results.append({
    "id": "TC-PERF-S6-001",
    "title": "Carga em GET /advice da Advice Slip API (8 VUs / 25s)",
    "status": status1,
    "duration_ms": 25000,
    "type": "carga",
    "details": {
        "vus": 8,
        "duration": "25s",
        "total_requests": reqs1,
        "p95_ms": round(p95_1, 2),
        "avg_ms": round(avg1, 2),
        "error_rate_percent": round(err_rate_1, 2),
        "thresholds": {"p95_ms": 3000, "error_rate_percent": 2},
        "validations": validations1
    },
    "logs": [
        f"[K6] Script: perf_s6_001.js — 8 VUs / 25s",
        f"[K6] Total requisicoes: {reqs1}",
        f"[K6] p95: {p95_1:.0f}ms (threshold: 3000ms) {'OK' if p95_1 < 3000 else 'FAIL'}",
        f"[K6] Taxa de erro: {err_rate_1:.2f}% (threshold: 2%) {'OK' if err_rate_1 < 2 else 'FAIL'}",
        f"-> STATUS: {status1.upper()}"
    ],
    "error": None if passed1 else f"p95={p95_1:.0f}ms, erro={err_rate_1:.2f}%"
})

# TC-PERF-S6-002: Open Trivia DB — 5 VUs / 20s
m2 = read_k6_metrics(r"C:\Users\gabriel.carminitti\Documents\claude\agentes\tmp_perf_s6_133058\k6_out_002.json")
durs2 = sorted(m2.get('http_req_duration', []))
fails2 = m2.get('http_req_failed', [])
p95_2 = durs2[int(len(durs2)*0.95)] if durs2 else 9999
avg2 = sum(durs2)/len(durs2) if durs2 else 0
err_rate_2 = sum(fails2)/len(fails2)*100 if fails2 else 0
reqs2 = len(durs2)

passed2 = p95_2 < 3500 and err_rate_2 < 2
status2 = "passed" if passed2 else "failed"

log_lines.append(f"[{ts()}] TC-PERF-S6-002: p95={p95_2:.0f}ms avg={avg2:.0f}ms err={err_rate_2:.2f}% reqs={reqs2}")
log_lines.append(f"[{ts()}] TC-PERF-S6-002 -> {status2.upper()}")

validations2 = [
    {"check": f"p95={p95_2:.0f}ms < 3500ms", "result": "passed" if p95_2 < 3500 else "failed"},
    {"check": f"taxa_erro={err_rate_2:.2f}% < 2%", "result": "passed" if err_rate_2 < 2 else "failed"},
    {"check": f"requisicoes={reqs2} executadas", "result": "passed" if reqs2 > 0 else "failed"},
]

results.append({
    "id": "TC-PERF-S6-002",
    "title": "Performance em GET /api.php da Open Trivia DB (5 VUs / 20s)",
    "status": status2,
    "duration_ms": 20000,
    "type": "performance",
    "details": {
        "vus": 5,
        "duration": "20s",
        "total_requests": reqs2,
        "p95_ms": round(p95_2, 2),
        "avg_ms": round(avg2, 2),
        "error_rate_percent": round(err_rate_2, 2),
        "thresholds": {"p95_ms": 3500, "error_rate_percent": 2},
        "validations": validations2
    },
    "logs": [
        f"[K6] Script: perf_s6_002.js — 5 VUs / 20s",
        f"[K6] Total requisicoes: {reqs2}",
        f"[K6] p95: {p95_2:.0f}ms (threshold: 3500ms) {'OK' if p95_2 < 3500 else 'FAIL'}",
        f"[K6] Taxa de erro: {err_rate_2:.2f}% (threshold: 2%) {'OK' if err_rate_2 < 2 else 'FAIL'}",
        f"[K6] NOTA: Open Trivia DB pode limitar rate de requisicoes — respostas podem retornar response_code != 0",
        f"-> STATUS: {status2.upper()}"
    ],
    "error": None if passed2 else f"Taxa de erro {err_rate_2:.1f}% excede threshold de 2%. API pode aplicar rate limit."
})

passed = sum(1 for r in results if r["status"] == "passed")
failed = sum(1 for r in results if r["status"] == "failed")

summary = {"total": 2, "passed": passed, "failed": failed, "skipped": 0, "credentials_failed": False}
output = {
    "executor": "performance",
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
