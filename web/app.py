import os
import sys
import json
import subprocess
import tempfile
import asyncio
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
import anthropic

app = FastAPI()

# ── System prompt ──────────────────────────────────────────────────────────────
_raw = (Path(__file__).parent.parent / "claude_ai_project_instructions.md").read_text(encoding="utf-8")
SYSTEM_PROMPT = _raw.split("\n---\n", 1)[1].lstrip("\n") if "\n---\n" in _raw else _raw

# ── Tool implementations ───────────────────────────────────────────────────────
def _run_python(code: str, timeout: int = 60) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        out = r.stdout
        if r.stderr:
            out += f"\n[stderr]\n{r.stderr}"
        return out or "(sem saída)"
    except subprocess.TimeoutExpired:
        return f"[ERRO] Timeout após {timeout}s"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _run_k6(script: str, timeout: int = 180) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(script)
        path = f.name
    try:
        r = subprocess.run(["k6", "run", path], capture_output=True, text=True, timeout=timeout)
        return r.stdout + (f"\n[stderr]\n{r.stderr}" if r.stderr else "")
    except FileNotFoundError:
        return "[ERRO] k6 não encontrado. Instale com: winget install k6"
    except subprocess.TimeoutExpired:
        return f"[ERRO] Timeout após {timeout}s"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _run_node(script: str, timeout: int = 60) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(script)
        path = f.name
    try:
        r = subprocess.run(["node", path], capture_output=True, text=True, timeout=timeout)
        out = r.stdout
        if r.stderr:
            out += f"\n[stderr]\n{r.stderr}"
        return out or "(sem saída)"
    except FileNotFoundError:
        return "[ERRO] Node.js não encontrado"
    except subprocess.TimeoutExpired:
        return f"[ERRO] Timeout após {timeout}s"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def _run_api_tests(base_url: str, tests_json: str) -> str:
    try:
        tests = json.loads(tests_json)
    except json.JSONDecodeError as e:
        return f"[ERRO] tests_json inválido: {e}"
    code = f"""
import requests, sys
base_url = {repr(base_url.rstrip("/"))}
tests = {json.dumps(tests, ensure_ascii=False)}
passed = 0
for t in tests:
    name = t.get("name", t.get("path", "?"))
    try:
        method = t.get("method", "GET").upper()
        url = base_url + "/" + t["path"].lstrip("/")
        resp = requests.request(method, url, json=t.get("body"), headers=t.get("headers", {{}}), timeout=10)
        expected = t.get("expected_status", 200)
        ok = resp.status_code == expected
        if ok and t.get("expected_fields"):
            try:
                body = resp.json()
                ok = all(f in body for f in t["expected_fields"])
            except Exception:
                ok = False
        if ok:
            passed += 1
            print(f"  PASS {{name}} ({{resp.status_code}}, {{int(resp.elapsed.total_seconds()*1000)}}ms)")
        else:
            print(f"  FAIL {{name}} — esperado {{expected}}, recebido {{resp.status_code}}")
    except Exception as e:
        print(f"  ERRO {{name}} — {{e}}")
print(f"\\nResultado: {{passed}}/{{len(tests)}} passaram")
"""
    return _run_python(code)


def _run_security_checks(base_url: str, extra_endpoints: str = "") -> str:
    extra = [p.strip() for p in extra_endpoints.split(",") if p.strip()]
    code = f"""
import requests
base_url = {repr(base_url.rstrip("/"))}
extra_paths = {repr(extra)}
SECURITY_HEADERS = ["x-frame-options","x-content-type-options","strict-transport-security","content-security-policy","x-xss-protection","referrer-policy"]
SENSITIVE_PATHS = ["/.env","/.git","/config","/admin","/api/keys","/swagger","/swagger-ui.html","/health","/metrics","/actuator"]
print("=== Headers de Segurança ===")
for path in (["/"] + extra_paths):
    url = base_url + path
    try:
        r = requests.get(url, timeout=8, allow_redirects=False)
        missing = [h for h in SECURITY_HEADERS if h not in r.headers]
        icon = "OK" if not missing else "AVISO"
        print(f"  {{icon}} {{path}} [HTTP {{r.status_code}}]")
        if missing: print(f"      Ausentes: {{', '.join(missing)}}")
    except Exception as e:
        print(f"  ERRO {{path}} — {{e}}")
print("\\n=== Endpoints Sensíveis ===")
exposed = []
for sp in SENSITIVE_PATHS + extra_paths:
    try:
        r = requests.get(base_url + sp, timeout=5)
        if r.status_code not in (401, 403, 404, 405):
            exposed.append((sp, r.status_code))
    except Exception:
        pass
if exposed:
    for path, code in exposed:
        print(f"  AVISO {{path}} exposto (HTTP {{code}})")
else:
    print("  OK Nenhum endpoint sensível exposto")
print("\\n=== CORS ===")
try:
    r = requests.options(base_url + "/", headers={{"Origin": "https://evil.com"}}, timeout=8)
    acao = r.headers.get("access-control-allow-origin", "")
    if acao in ("*", "https://evil.com"):
        print(f"  AVISO CORS permissivo: {{acao}}")
    else:
        print(f"  OK CORS: {{acao or 'não configurado'}}")
except Exception as e:
    print(f"  ERRO {{e}}")
"""
    return _run_python(code)


def _run_playwright_tests(script: str, update_snapshots: bool = False, browsers: str = "chromium", timeout: int = 120) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".spec.ts", delete=False, encoding="utf-8") as f:
        f.write(script)
        path = f.name
    try:
        cmd = ["npx", "playwright", "test", path, "--reporter=line"]
        if update_snapshots:
            cmd.append("--update-snapshots")
        for browser in [b.strip() for b in browsers.split(",") if b.strip()]:
            cmd += ["--project", browser]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        output = r.stdout
        if r.returncode != 0 and not output.strip():
            output = r.stderr or "(sem saída)"
        elif r.stderr:
            output += f"\n[stderr]\n{r.stderr}"
        return output or "(sem saída)"
    except FileNotFoundError:
        return "[ERRO] npx/playwright não encontrado. Instale com: npm install -D @playwright/test && npx playwright install chromium"
    except subprocess.TimeoutExpired:
        return f"[ERRO] Timeout após {timeout}s"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


TOOL_IMPLS = {
    "execute_python":      lambda i: _run_python(i["code"]),
    "execute_k6":          lambda i: _run_k6(i["script"]),
    "execute_node":        lambda i: _run_node(i["script"]),
    "run_api_tests":       lambda i: _run_api_tests(i["base_url"], i["tests_json"]),
    "run_security_checks": lambda i: _run_security_checks(i["base_url"], i.get("extra_endpoints", "")),
    "run_playwright_tests": lambda i: _run_playwright_tests(
        i["script"], i.get("update_snapshots", False), i.get("browsers", "chromium"), i.get("timeout", 120)
    ),
}

TOOLS = [
    {
        "name": "execute_python",
        "description": "Executa código Python e retorna stdout/stderr. Use para testes de API e segurança.",
        "input_schema": {"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]},
    },
    {
        "name": "execute_k6",
        "description": "Executa script k6 para testes de performance/carga e retorna métricas.",
        "input_schema": {"type": "object", "properties": {"script": {"type": "string"}}, "required": ["script"]},
    },
    {
        "name": "execute_node",
        "description": "Executa script Node.js (Playwright, axe-core) e retorna output.",
        "input_schema": {"type": "object", "properties": {"script": {"type": "string"}}, "required": ["script"]},
    },
    {
        "name": "run_api_tests",
        "description": "Executa testes de API REST estruturados.",
        "input_schema": {
            "type": "object",
            "properties": {"base_url": {"type": "string"}, "tests_json": {"type": "string"}},
            "required": ["base_url", "tests_json"],
        },
    },
    {
        "name": "run_security_checks",
        "description": "Verificações de segurança não invasivas: headers HTTP, auth, endpoints sensíveis, CORS.",
        "input_schema": {
            "type": "object",
            "properties": {"base_url": {"type": "string"}, "extra_endpoints": {"type": "string"}},
            "required": ["base_url"],
        },
    },
    {
        "name": "run_playwright_tests",
        "description": "Executa testes Playwright (browser, visual, acessibilidade com axe-core).",
        "input_schema": {
            "type": "object",
            "properties": {
                "script": {"type": "string"},
                "update_snapshots": {"type": "boolean"},
                "browsers": {"type": "string"},
                "timeout": {"type": "integer"},
            },
            "required": ["script"],
        },
    },
]

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/")
async def index():
    return HTMLResponse((Path(__file__).parent / "index.html").read_text(encoding="utf-8"))


@app.post("/run")
async def run_tests(request: Request):
    body = await request.json()
    test_cases = body.get("test_cases", "").strip()
    if not test_cases:
        async def empty():
            yield f"data: {json.dumps({'type': 'error', 'content': 'Nenhum caso de teste fornecido.'})}\n\n"
        return StreamingResponse(empty(), media_type="text/event-stream")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        async def no_key():
            yield f"data: {json.dumps({'type': 'error', 'content': 'ANTHROPIC_API_KEY não definida. Defina a variável de ambiente antes de iniciar o servidor.'})}\n\n"
        return StreamingResponse(no_key(), media_type="text/event-stream")

    async def event_stream():
        client = anthropic.AsyncAnthropic(api_key=api_key)
        messages = [{"role": "user", "content": test_cases}]

        while True:
            yield f"data: {json.dumps({'type': 'status', 'content': 'Classificando e planejando execução...'})}\n\n"

            response = await client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=8096,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages,
            )

            for block in response.content:
                if block.type == "text" and block.text.strip():
                    yield f"data: {json.dumps({'type': 'text', 'content': block.text})}\n\n"

            if response.stop_reason == "end_turn":
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                break

            if response.stop_reason == "tool_use":
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []

                for block in response.content:
                    if block.type == "tool_use":
                        yield f"data: {json.dumps({'type': 'tool_start', 'name': block.name})}\n\n"

                        if block.name in TOOL_IMPLS:
                            result = await asyncio.to_thread(TOOL_IMPLS[block.name], block.input)
                        else:
                            result = f"[ERRO] Tool desconhecida: {block.name}"

                        yield f"data: {json.dumps({'type': 'tool_result', 'name': block.name, 'content': result})}\n\n"
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

                messages.append({"role": "user", "content": tool_results})
            else:
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                break

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("[AVISO] ANTHROPIC_API_KEY não definida. Defina antes de usar a interface.")

    print(f"\n  QA Squad Web  →  http://localhost:{args.port}")
    print(f"  Rede local    →  http://[seu-ip]:{args.port}\n")
    uvicorn.run(app, host=args.host, port=args.port)
