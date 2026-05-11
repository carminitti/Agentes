# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests, json, time, os, warnings
from datetime import datetime

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

SUITE_DIR = r"C:\Users\gabriel.carminitti\Documents\claude\agentes\suite6\suite_api_browser_k6_visual_axe_zap_db_20260511_132805"
OUTPUT_DIR = os.path.join(SUITE_DIR, "api")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ok_mark(b): return "OK" if b else "FAIL"

results = []
log_lines = [f"[{ts()}] === executor-api -- inicio ==="]

def test_exchange_rate():
    tc_id = "TC-API-S6-001"
    title = "Consultar taxa de cambio atual do USD via ExchangeRate API"
    url = "https://open.er-api.com/v6/latest/USD"
    logs, validations, status, error = [], [], "passed", None
    resp = None

    logs.append(f"[REQUEST] GET {url}")
    t0 = time.time()
    try:
        resp = requests.get(url, timeout=10, verify=False)
        duration_ms = int((time.time() - t0) * 1000)
        logs.append(f"[RESPONSE] {resp.status_code} -- {duration_ms}ms")

        def chk(label, ok):
            nonlocal status, error
            c = {"check": label, "result": "passed" if ok else "failed"}
            if not ok: status = "failed"; error = error or f"Falha em: {label}"
            validations.append(c); logs.append(f"[ASSERT] {label} {ok_mark(ok)}")

        chk("status == 200", resp.status_code == 200)
        body = resp.json()
        chk("result == 'success'", body.get("result") == "success")
        chk("base_code == 'USD'", body.get("base_code") == "USD")
        rates = body.get("rates", {})
        brl = rates.get("BRL", 0)
        chk(f"rates.BRL={brl} > 0", isinstance(brl, (int, float)) and brl > 0)
        eur = rates.get("EUR", 0)
        chk(f"rates.EUR={eur} > 0", isinstance(eur, (int, float)) and eur > 0)
        chk(f"duration={duration_ms}ms < 4000ms", duration_ms < 4000)

    except Exception as e:
        status = "failed"; error = str(e); duration_ms = int((time.time() - t0) * 1000)
        logs.append(f"[ERROR] {e}"); validations.append({"check": "conexao bem-sucedida", "result": "failed"})

    logs.append(f"-> STATUS: {status.upper()}")
    return {
        "id": tc_id, "title": title, "status": status, "duration_ms": duration_ms,
        "details": {"method": "GET", "url": url,
                    "status_code": resp.status_code if resp is not None else None,
                    "validations": validations},
        "logs": logs, "error": error
    }


def test_sunrise_sunset():
    tc_id = "TC-API-S6-002"
    title = "Consultar horario de nascer e por do sol em Brasilia"
    url = "https://api.sunrise-sunset.org/json?lat=-15.77&lng=-47.92&date=today&formatted=0"
    logs, validations, status, error = [], [], "passed", None
    resp = None

    logs.append(f"[REQUEST] GET {url}")
    t0 = time.time()
    try:
        resp = requests.get(url, timeout=10, verify=False)
        duration_ms = int((time.time() - t0) * 1000)
        logs.append(f"[RESPONSE] {resp.status_code} -- {duration_ms}ms")

        def chk(label, ok):
            nonlocal status, error
            c = {"check": label, "result": "passed" if ok else "failed"}
            if not ok: status = "failed"; error = error or f"Falha em: {label}"
            validations.append(c); logs.append(f"[ASSERT] {label} {ok_mark(ok)}")

        chk("status == 200", resp.status_code == 200)
        body = resp.json()
        chk("status == 'OK'", body.get("status") == "OK")
        res = body.get("results", {})
        sunrise = res.get("sunrise", "")
        chk(f"results.sunrise valido", bool(sunrise) and "T" in str(sunrise))
        sunset = res.get("sunset", "")
        chk(f"results.sunset valido", bool(sunset) and "T" in str(sunset))
        day_len = res.get("day_length", 0)
        chk(f"results.day_length={day_len} > 0", isinstance(day_len, (int, float)) and day_len > 0)
        chk(f"duration={duration_ms}ms < 4000ms", duration_ms < 4000)

    except Exception as e:
        status = "failed"; error = str(e); duration_ms = int((time.time() - t0) * 1000)
        logs.append(f"[ERROR] {e}"); validations.append({"check": "conexao bem-sucedida", "result": "failed"})

    logs.append(f"-> STATUS: {status.upper()}")
    return {
        "id": tc_id, "title": title, "status": status, "duration_ms": duration_ms,
        "details": {"method": "GET", "url": url,
                    "status_code": resp.status_code if resp is not None else None,
                    "validations": validations},
        "logs": logs, "error": error
    }


log_lines.append(f"[{ts()}] Executando TC-API-S6-001...")
r1 = test_exchange_rate()
results.append(r1)
for l in r1["logs"]: log_lines.append(f"[{ts()}]   {l}")
log_lines.append(f"[{ts()}] [TC-API-S6-001] -> {r1['status'].upper()}")

log_lines.append(f"[{ts()}] Executando TC-API-S6-002...")
r2 = test_sunrise_sunset()
results.append(r2)
for l in r2["logs"]: log_lines.append(f"[{ts()}]   {l}")
log_lines.append(f"[{ts()}] [TC-API-S6-002] -> {r2['status'].upper()}")

passed = sum(1 for r in results if r["status"] == "passed")
failed = sum(1 for r in results if r["status"] == "failed")

summary = {"total": 2, "passed": passed, "failed": failed, "skipped": 0, "credentials_failed": False}
output = {
    "executor": "api",
    "environment": "https://open.er-api.com + https://api.sunrise-sunset.org",
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
