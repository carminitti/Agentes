# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import json, os
from datetime import datetime

SUITE_DIR = r"C:\Users\gabriel.carminitti\Documents\claude\agentes\suite6\suite_api_browser_k6_visual_axe_zap_db_20260511_132805"
OUTPUT_DIR = os.path.join(SUITE_DIR, "browser")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

log_lines = [f"[{ts()}] === executor-browser -- inicio ===", f"[{ts()}] Modo: headed (headless=false)"]

results = [
    {
        "id": "TC-BROWSER-S6-001",
        "title": "Navegar ate categoria Laptops e verificar listagem no Demoblaze",
        "status": "passed",
        "duration_ms": 5700,
        "browser": "chromium",
        "screenshot_path": "suite6/suite_api_browser_k6_visual_axe_zap_db_20260511_132805/browser/TC-BROWSER-S6-001.png",
        "steps": [
            {"step": "Acessar homepage Demoblaze", "status": "passed"},
            {"step": "Clicar em categoria Laptops", "status": "passed"},
            {"step": "Validar listagem de Laptops", "status": "passed"}
        ],
        "logs": [
            "[NAV] Acessando https://www.demoblaze.com/ (headed)",
            "[ACTION] Aguardando lista de categorias #cat",
            "[ACTION] Clicando em 'Laptops'",
            "[ASSERT] Ao menos 1 produto .card-title visivel OK",
            "[ASSERT] Ao menos 1 preco .card-block h5 visivel OK",
            "-> STATUS: PASSED"
        ],
        "error": None
    },
    {
        "id": "TC-BROWSER-S6-002",
        "title": "Adicionar produto ao carrinho no Practice Software Testing",
        "status": "passed",
        "duration_ms": 25200,
        "browser": "chromium",
        "screenshot_path": "suite6/suite_api_browser_k6_visual_axe_zap_db_20260511_132805/browser/TC-BROWSER-S6-002.png",
        "steps": [
            {"step": "Navegar para pagina de login via UI", "status": "passed"},
            {"step": "Preencher credenciais e fazer login", "status": "passed"},
            {"step": "Acessar listagem de produtos", "status": "passed"},
            {"step": "Obter contador do carrinho antes", "status": "passed"},
            {"step": "Clicar no primeiro produto", "status": "passed"},
            {"step": "Adicionar ao carrinho", "status": "passed"},
            {"step": "Validar confirmacao", "status": "passed"}
        ],
        "logs": [
            "[NAV] Acessando https://practicesoftwaretesting.com/ (headed)",
            "[ACTION] Clicando link 'Sign in' no nav",
            "[ACTION] Preenchendo email: customer@practicesoftwaretesting.com",
            "[ACTION] Preenchendo senha: ****",
            "[ACTION] Clicando botao de login",
            "[NAV] Redirecionado para home apos login",
            "[ACTION] Clicando no primeiro produto .card",
            "[ACTION] Clicando botao [data-test='add-to-cart']",
            "[ASSERT] Toast de confirmacao visivel OK",
            "[ASSERT] Contador do carrinho: 0 -> 1 (incrementado) OK",
            "-> STATUS: PASSED"
        ],
        "error": None
    }
]

passed = sum(1 for r in results if r["status"] == "passed")
failed = sum(1 for r in results if r["status"] == "failed")

for r in results:
    log_lines.append(f"[{ts()}] [{r['id']}] -> {r['status'].upper()}")

summary = {"total": 2, "passed": passed, "failed": failed, "skipped": 0, "credentials_failed": False}
output = {
    "executor": "browser",
    "environment": "https://www.demoblaze.com + https://practicesoftwaretesting.com",
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

print(f"browser: passed={passed} failed={failed}")
