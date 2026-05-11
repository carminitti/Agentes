"""
Executor API - Practice Expand Testing
TC-API-011 a TC-API-016
"""
import requests
import warnings
import json
import time

warnings.filterwarnings('ignore')

BASE = 'https://practice.expandtesting.com/notes/api'
results = []

def run_test(tc_id, title, fn):
    start = time.time()
    try:
        status, details, logs = fn()
        duration = int((time.time() - start) * 1000)
        results.append({
            "id": tc_id,
            "title": title,
            "status": status,
            "duration_ms": duration,
            "details": details,
            "logs": logs,
            "error": None if status == "passed" else details.get("error", "")
        })
    except Exception as e:
        duration = int((time.time() - start) * 1000)
        results.append({
            "id": tc_id,
            "title": title,
            "status": "failed",
            "duration_ms": duration,
            "details": {},
            "logs": [f"[ERROR] {str(e)}"],
            "error": str(e)
        })

# TC-API-011: Health check
def test_011():
    logs = ["[REQUEST] GET " + BASE + "/health-check"]
    r = requests.get(BASE + "/health-check", timeout=10, verify=False)
    logs.append(f"[RESPONSE] {r.status_code} — {r.elapsed.microseconds//1000}ms")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    data = r.json()
    logs.append(f"[ASSERT] status == 200 ✓")
    assert data.get("message") == "Notes API is Running", f"Message wrong: {data.get('message')}"
    logs.append(f"[ASSERT] message == 'Notes API is Running' ✓")
    return "passed", {"status_code": 200, "message": data.get("message")}, logs

run_test("TC-API-011", "Health check da API de notas", test_011)

# TC-API-012: Registrar usuário (já foi criado, aceitar 409)
def test_012():
    logs = ["[REQUEST] POST " + BASE + "/users/register"]
    r = requests.post(BASE + "/users/register",
        json={"name": "QA Agente", "email": "qa_agente_v3@test.com", "password": "Test@1234"},
        timeout=10, verify=False)
    logs.append(f"[RESPONSE] {r.status_code} — {r.elapsed.microseconds//1000}ms")
    # 201 = criado com sucesso; 409 = usuário já existe (aceitável)
    assert r.status_code in [201, 409], f"Expected 201 or 409, got {r.status_code}"
    logs.append(f"[ASSERT] status in [201, 409] ✓ (recebido: {r.status_code})")
    data = r.json()
    if r.status_code == 201:
        assert data["data"]["name"] == "QA Agente"
        assert data["data"]["email"] == "qa_agente_v3@test.com"
        logs.append("[ASSERT] data.name == 'QA Agente' ✓")
        logs.append("[ASSERT] data.email == 'qa_agente_v3@test.com' ✓")
    else:
        logs.append(f"[INFO] Usuário já existia (409) — aceitável")
    return "passed", {"status_code": r.status_code, "note": "Usuário criado ou já existia"}, logs

run_test("TC-API-012", "Registrar usuário no Practice Expand", test_012)

# TC-API-013: Login e obter token
TOKEN = None

def test_013():
    global TOKEN
    logs = ["[REQUEST] POST " + BASE + "/users/login"]
    r = requests.post(BASE + "/users/login",
        json={"email": "qa_agente_v3@test.com", "password": "Test@1234"},
        timeout=10, verify=False)
    logs.append(f"[RESPONSE] {r.status_code} — {r.elapsed.microseconds//1000}ms")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    logs.append("[ASSERT] status == 200 ✓")
    data = r.json()
    token = data.get("data", {}).get("token")
    assert token and len(token) > 0, "Token deve ser não vazio"
    TOKEN = token
    logs.append(f"[ASSERT] data.token não vazio ✓ (token obtido)")
    return "passed", {"status_code": 200, "token_obtained": True}, logs

run_test("TC-API-013", "Login e obter token no Practice Expand", test_013)

# TC-API-014: Criar nota autenticada
NOTE_ID = None

def test_014():
    global NOTE_ID
    # Garantir token
    logs = []
    token = TOKEN
    if not token:
        logs.append("[SETUP] Obtendo token via login...")
        r_login = requests.post(BASE + "/users/login",
            json={"email": "qa_agente_v3@test.com", "password": "Test@1234"},
            timeout=10, verify=False)
        token = r_login.json().get("data", {}).get("token")
    logs.append("[REQUEST] POST " + BASE + "/notes")
    logs.append(f"[HEADER] x-auth-token: {'<token>' if token else 'MISSING'}")
    r = requests.post(BASE + "/notes",
        headers={"x-auth-token": token},
        json={"title": "Nota do QA Agente", "description": "Criada pelo executor-api v3", "category": "Work"},
        timeout=10, verify=False)
    logs.append(f"[RESPONSE] {r.status_code} — {r.elapsed.microseconds//1000}ms")
    assert r.status_code == 200, f"Expected 200, got {r.status_code} — {r.text[:100]}"
    logs.append("[ASSERT] status == 200 ✓")
    data = r.json()
    assert data["data"]["title"] == "Nota do QA Agente"
    logs.append("[ASSERT] data.title == 'Nota do QA Agente' ✓")
    assert data["data"]["category"] == "Work"
    logs.append("[ASSERT] data.category == 'Work' ✓")
    NOTE_ID = data["data"]["id"]
    logs.append(f"[INFO] Note ID salvo: {NOTE_ID}")
    return "passed", {"status_code": 200, "note_id": NOTE_ID}, logs

run_test("TC-API-014", "Criar nota autenticada no Practice Expand", test_014)

# TC-API-015: Listar notas autenticado
def test_015():
    token = TOKEN
    logs = []
    if not token:
        logs.append("[SETUP] Obtendo token via login...")
        r_login = requests.post(BASE + "/users/login",
            json={"email": "qa_agente_v3@test.com", "password": "Test@1234"},
            timeout=10, verify=False)
        token = r_login.json().get("data", {}).get("token")
    logs.append("[REQUEST] GET " + BASE + "/notes")
    r = requests.get(BASE + "/notes",
        headers={"x-auth-token": token},
        timeout=10, verify=False)
    logs.append(f"[RESPONSE] {r.status_code} — {r.elapsed.microseconds//1000}ms")
    assert r.status_code == 200, f"Expected 200, got {r.status_code}"
    logs.append("[ASSERT] status == 200 ✓")
    data = r.json()
    notes = data.get("data", [])
    assert isinstance(notes, list)
    logs.append(f"[ASSERT] resultado é array ✓ ({len(notes)} notas)")
    if notes:
        note = notes[0]
        for field in ["id", "title", "description", "category"]:
            assert field in note, f"Campo '{field}' ausente"
            logs.append(f"[ASSERT] campo '{field}' presente ✓")
    return "passed", {"status_code": 200, "notes_count": len(notes)}, logs

run_test("TC-API-015", "Listar notas autenticado no Practice Expand", test_015)

# TC-API-016: Tentar criar nota sem autenticação → 401
def test_016():
    logs = ["[REQUEST] POST " + BASE + "/notes (sem x-auth-token)"]
    r = requests.post(BASE + "/notes",
        json={"title": "Nota sem auth", "description": "Não deve ser criada", "category": "Home"},
        timeout=10, verify=False)
    logs.append(f"[RESPONSE] {r.status_code} — {r.elapsed.microseconds//1000}ms")
    assert r.status_code == 401, f"Expected 401, got {r.status_code}"
    logs.append("[ASSERT] status == 401 ✓ — endpoint protegido corretamente")
    return "passed", {"status_code": 401, "protected": True}, logs

run_test("TC-API-016", "Tentar criar nota sem autenticação retorna 401", test_016)

# Output
passed = sum(1 for r in results if r["status"] == "passed")
failed = sum(1 for r in results if r["status"] == "failed")

output = {
    "executor": "api",
    "environment": "https://practice.expandtesting.com/notes/api",
    "results": results,
    "summary": {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "skipped": 0
    }
}

import sys
sys.stdout.reconfigure(encoding='utf-8')
print(json.dumps(output, indent=2, ensure_ascii=True))
