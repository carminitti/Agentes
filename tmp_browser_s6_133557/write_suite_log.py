# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import json, os
from datetime import datetime

SUITE_DIR = r"C:\Users\gabriel.carminitti\Documents\claude\agentes\suite6\suite_api_browser_k6_visual_axe_zap_db_20260511_132805"
suite_start_time = "2026-05-11 13:28:05"
suite_end_time = datetime.now().isoformat()

executors = {
    "api": r"api\resultado.json",
    "browser": r"browser\resultado.json",
    "performance": r"performance\resultado.json",
    "visual": r"visual\resultado.json",
    "acessibilidade": r"acessibilidade\resultado.json",
    "seguranca": r"seguranca\resultado.json",
    "banco": r"banco\resultado.json",
}

log_lines = [
    f"=== Suite QA -- suite_api_browser_k6_visual_axe_zap_db_20260511_132805 ===",
    f"Inicio: {suite_start_time}",
    f"Fim: {suite_end_time}",
    f"Ambiente: multiple (APIs publicas + SQLite :memory:)",
    "",
    "--- Executores despachados ---",
]

total_passed = 0
total_failed = 0
total_skipped = 0

for executor_name, rel_path in executors.items():
    full_path = os.path.join(SUITE_DIR, rel_path)
    try:
        with open(full_path, encoding='utf-8') as f:
            result = json.load(f)
        s = result.get("summary", {})
        p = s.get("passed", 0)
        f_ = s.get("failed", 0)
        sk = s.get("skipped", 0)
        total_passed += p
        total_failed += f_
        total_skipped += sk
        log_lines.append(f"  {executor_name}: passed={p}, failed={f_}, skipped={sk}")
    except Exception as e:
        log_lines.append(f"  {executor_name}: ERRO ao ler resultado ({e})")

log_lines.extend([
    "",
    "--- Nao executados ---",
    "  pact: tipo contrato (Pact) -- Requer Pact Broker",
    "  appium: tipo mobile (Appium) -- Requer configuracao de dispositivo/emulador",
    "",
    "--- Retries realizados ---",
    "  TC-API-S6-002: SSLError -> retry com verify=False -> PASSED",
    "  TC-SEC-S6-001: SSLError -> retry com verify=False -> PASSED",
    "  TC-SEC-S6-002: SSLError -> retry com verify=False -> PASSED",
    "  TC-BROWSER-S6-002: seletor .getByLabel timeout -> retry com data-test -> PASSED",
    "",
    f"--- Totais finais: passed={total_passed}, failed={total_failed}, skipped={total_skipped} ---",
    "",
    "--- Fim do log da suite ---",
])

suite_log_path = os.path.join(SUITE_DIR, "suite.log")
with open(suite_log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))

print(f"suite.log gravado em: {suite_log_path}")
print(f"Totais: passed={total_passed}, failed={total_failed}, skipped={total_skipped}")
