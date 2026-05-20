from mcp.server.fastmcp import FastMCP
import subprocess
import sys
import os
import json
import tempfile

import argparse as _argparse

_parser = _argparse.ArgumentParser(add_help=False)
_parser.add_argument("--host", default="0.0.0.0")
_parser.add_argument("--port", type=int, default=8000)
_known, _ = _parser.parse_known_args()

mcp = FastMCP("qa-squad", host=_known.host, port=_known.port)


# ── helpers de execução ────────────────────────────────────────────────────────

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


# ── ferramentas de baixo nível (Claude gera o script, MCP executa) ─────────────

@mcp.tool()
def execute_python(code: str) -> str:
    """Executa código Python e retorna stdout/stderr. Use para testes de API e segurança."""
    return _run_python(code)


@mcp.tool()
def execute_k6(script: str) -> str:
    """Executa script k6 para testes de performance/carga e retorna métricas."""
    return _run_k6(script)


@mcp.tool()
def execute_node(script: str) -> str:
    """Executa script Node.js (Playwright, axe-core) e retorna output."""
    return _run_node(script)


# ── ferramentas de alto nível ──────────────────────────────────────────────────

@mcp.tool()
def run_api_tests(base_url: str, tests_json: str) -> str:
    """
    Executa testes de API REST estruturados.

    tests_json: array JSON com objetos no formato:
      {"name", "method", "path", "expected_status", "body"?, "headers"?, "expected_fields"?}

    Exemplo:
      [{"name":"Lista usuários","method":"GET","path":"/users","expected_status":200}]
    """
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
        resp = requests.request(
            method, url,
            json=t.get("body"),
            headers=t.get("headers", {{}}),
            timeout=10,
        )
        expected = t.get("expected_status", 200)
        ok = resp.status_code == expected

        if ok and t.get("expected_fields"):
            try:
                body = resp.json()
                if isinstance(body, dict):
                    ok = all(f in body for f in t["expected_fields"])
                else:
                    ok = False
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
sys.exit(0 if passed == len(tests) else 1)
"""
    return _run_python(code)


@mcp.tool()
def run_security_checks(base_url: str, extra_endpoints: str = "") -> str:
    """
    Verificações de segurança não invasivas: headers HTTP, auth (401/403), endpoints sensíveis, CORS.
    extra_endpoints: paths adicionais separados por vírgula (ex: /api/users,/api/admin).
    """
    extra = [p.strip() for p in extra_endpoints.split(",") if p.strip()]
    code = f"""
import requests

base_url = {repr(base_url.rstrip("/"))}
extra_paths = {repr(extra)}

SECURITY_HEADERS = [
    "x-frame-options", "x-content-type-options", "strict-transport-security",
    "content-security-policy", "x-xss-protection", "referrer-policy",
]
SENSITIVE_PATHS = [
    "/.env", "/.git", "/config", "/admin", "/api/keys",
    "/swagger", "/swagger-ui.html", "/health", "/metrics", "/actuator",
]

print("=== Headers de Segurança ===")
for path in (["/"] + extra_paths):
    url = base_url + path
    try:
        r = requests.get(url, timeout=8, allow_redirects=False)
        missing = [h for h in SECURITY_HEADERS if h not in r.headers]
        icon = "✓" if not missing else "⚠"
        print(f"  {{icon}} {{path}} [HTTP {{r.status_code}}]")
        if missing:
            print(f"      Ausentes: {{', '.join(missing)}}")
    except Exception as e:
        print(f"  ✗ {{path}} — {{e}}")

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
        print(f"  ⚠ {{path}} exposto (HTTP {{code}})")
else:
    print("  ✓ Nenhum endpoint sensível exposto")

print("\\n=== CORS ===")
try:
    r = requests.options(base_url + "/", headers={{"Origin": "https://evil.com"}}, timeout=8)
    acao = r.headers.get("access-control-allow-origin", "")
    if acao in ("*", "https://evil.com"):
        print(f"  ⚠ CORS permissivo: Access-Control-Allow-Origin: {{acao}}")
    else:
        print(f"  ✓ CORS: {{acao or 'não configurado'}}")
except Exception as e:
    print(f"  ✗ {{e}}")
"""
    return _run_python(code)


@mcp.tool()
def run_performance_test(
    url: str,
    vus: int = 10,
    duration: str = "30s",
    threshold_p95_ms: int = 2000,
) -> str:
    """
    Executa teste de performance com k6.
    url: endpoint GET alvo.
    vus: usuários virtuais simultâneos (default 10).
    duration: duração (ex: 30s, 1m, 5m — default 30s).
    threshold_p95_ms: limite p95 aceitável em ms (default 2000).
    """
    script = f"""
import http from 'k6/http';
import {{ check, sleep }} from 'k6';

export const options = {{
  vus: {vus},
  duration: '{duration}',
  thresholds: {{
    http_req_duration: ['p(95)<{threshold_p95_ms}'],
    http_req_failed: ['rate<0.01'],
  }},
}};

export default function () {{
  const res = http.get({json.dumps(url)});
  check(res, {{
    'status 200': (r) => r.status === 200,
    'dentro do threshold': (r) => r.timings.duration < {threshold_p95_ms},
  }});
  sleep(1);
}}
"""
    return _run_k6(script)


@mcp.tool()
def run_playwright_tests(
    script: str,
    update_snapshots: bool = False,
    browsers: str = "chromium",
    timeout: int = 120,
) -> str:
    """
    Executa testes Playwright (browser, visual, acessibilidade com axe-core).

    script: conteúdo TypeScript do arquivo .spec.ts
    update_snapshots: True para criar/atualizar baseline de screenshots visuais
    browsers: navegadores separados por vírgula — ex: "chromium", "chromium,firefox,webkit"
    timeout: timeout total em segundos (default 120)

    Retorna o JSON do Playwright reporter + stderr em caso de erro.
    """
    import shutil

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".spec.ts", delete=False, encoding="utf-8"
    ) as f:
        spec_path = f.name
        f.write(script)

    try:
        cmd = ["npx", "playwright", "test", spec_path, "--reporter=json"]
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
        return (
            "[ERRO] npx/playwright não encontrado. "
            "Instale com: npm install -D @playwright/test && npx playwright install chromium"
        )
    except subprocess.TimeoutExpired:
        return f"[ERRO] Timeout após {timeout}s"
    finally:
        try:
            os.unlink(spec_path)
        except OSError:
            pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", default="stdio", choices=["stdio", "sse", "streamable-http"])
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    mcp.run(transport=args.transport)
