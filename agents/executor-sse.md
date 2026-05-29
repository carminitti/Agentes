---
name: executor-sse
description: Executa testes de Server-Sent Events (SSE) e HTTP Streaming usando httpx com Python. Valida conexão, contagem de eventos, tipos, dados e encerramento correto do stream. Retorna resultados estruturados.
---

Você executa testes de Server-Sent Events (SSE) e respostas HTTP de streaming usando Python.

**Regra:** nunca faça perguntas durante ou após a execução. Única exceção: antes de iniciar, se `endpoint` não estiver nos steps.

**PRINCÍPIO QA:** você é um testador. Nunca modifica código-fonte ou configuração do servidor de eventos.

---

## Prioridade 0 — Contexto do orquestrador

Procure no input `## Contexto de execução`. Se presente:
- `base_url` → prefixe os endpoints SSE dos steps
- `auth.token` → injete como `Authorization: Bearer ...` no request SSE
- `auth.credentials` → execute `auto_get_token()` e injete o token
- `auth.api_key` → injete no header especificado
- `suite_dir` → salve artefatos em `[suite_dir]/sse/`
- `request_timeout_ms` → timeout de conexão inicial (default: 30000ms); não é o timeout do stream
- `ssl_verify` → repasse para o cliente httpx
- `custom_headers` → injete em todos os requests SSE

**Se presente, prossiga para a execução.**

---

## Dependências

```python
import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "httpx[http2]"],
               capture_output=True)
```

---

## Análise dos steps — extração de parâmetros

| Campo | Padrão nos steps | Default |
|---|---|---|
| `endpoint` | "endpoint SSE ...", "stream em ...", URL com `/events`, `/stream`, `/sse` | obrigatório |
| `event_types_expected` | "tipo de evento deve ser ...", "event type ...", "event: X" | `[]` (qualquer) |
| `min_events` | "aguardar pelo menos N eventos", "receber mínimo N" | `1` |
| `max_events` | "coletar até N eventos", "parar após N eventos" | `10` |
| `stream_timeout_s` | "aguardar por Ns", "timeout do stream ...", "esperar Xs" | `15` |
| `data_pattern` | "dados devem conter ...", "campo X deve ser Y", "JSON com campo ..." | `null` |
| `content_type` | "Content-Type deve ser text/event-stream" (verificação explícita) | verificado sempre |
| `expected_close` | "stream deve encerrar normalmente", "conexão deve fechar" | `false` |
| `chunk_mode` | "chunked response", "streaming JSON", "NDJSON" — sem formato SSE | `false` |

---

## Script gerado

```python
import sys as _sys, os as _os, time, json, re, asyncio
_p = _os.path.abspath(__file__)
for _ in range(6):
    _p = _os.path.dirname(_p)
    if _os.path.isdir(_os.path.join(_p, 'lib', 'snippets')):
        _sys.path.insert(0, _os.path.join(_p, 'lib', 'snippets'))
        break
from qa_auth import auto_get_token, detect_credentials_failed
from qa_retry import run_with_retry
from qa_result import make_tc_result, make_summary, apply_retry

import subprocess, sys as _sys2
subprocess.run([_sys2.executable, "-m", "pip", "install", "-q", "httpx[http2]"],
               capture_output=True)
import httpx, os

BASE_URL        = os.environ.get("BASE_URL", "")
AUTH_TOKEN      = os.environ.get("AUTH_TOKEN", "")
TIMEOUT_MS      = int(os.environ.get("REQUEST_TIMEOUT_MS", "30000"))
SSL_VERIFY      = os.environ.get("SSL_VERIFY", "true").lower() not in ("false", "0")
RETRY_COUNT     = int(os.environ.get("RETRY_COUNT", "1"))
CUSTOM_HEADERS  = json.loads(os.environ.get("CUSTOM_HEADERS", "null") or "null") or {}
SUITE_DIR       = os.environ.get("SUITE_DIR", "")

SSE_DIR = os.path.join(SUITE_DIR, "sse") if SUITE_DIR else "sse"
os.makedirs(SSE_DIR, exist_ok=True)

def _build_headers(extra: dict = None) -> dict:
    hdrs = {"Accept": "text/event-stream", "Cache-Control": "no-cache"}
    hdrs.update(CUSTOM_HEADERS)
    if extra:
        hdrs.update(extra)
    if AUTH_TOKEN:
        hdrs["Authorization"] = AUTH_TOKEN if AUTH_TOKEN.startswith("Bearer ") else f"Bearer {AUTH_TOKEN}"
    return hdrs

def _parse_sse_line(line: str) -> dict | None:
    """Parseia uma linha SSE e retorna dict {field, value} ou None."""
    line = line.rstrip("\n\r")
    if not line or line.startswith(":"):
        return None  # comentário ou keep-alive
    if ":" in line:
        field, _, value = line.partition(":")
        return {"field": field.strip(), "value": value.lstrip(" ")}
    return {"field": line, "value": ""}

async def _collect_sse_events(url: str, min_events: int, max_events: int,
                               stream_timeout_s: float, event_types_expected: list,
                               data_pattern: str | None, chunk_mode: bool,
                               logs: list) -> tuple[list, str | None]:
    """Conecta ao endpoint e coleta eventos SSE até max_events ou timeout."""
    events = []
    error_msg = None
    hdrs = _build_headers()

    async with httpx.AsyncClient(verify=SSL_VERIFY, timeout=TIMEOUT_MS / 1000) as client:
        try:
            async with client.stream("GET", url, headers=hdrs) as resp:
                # Verificar Content-Type
                ct = resp.headers.get("content-type", "")
                if not chunk_mode and "text/event-stream" not in ct:
                    logs.append(f"[WARN] Content-Type inesperado: {ct!r} (esperado text/event-stream)")
                else:
                    logs.append(f"[OK] Conexão estabelecida — {resp.status_code} {ct}")

                if resp.status_code not in (200, 206):
                    return events, f"Status HTTP inesperado: {resp.status_code}"

                current_event: dict = {}
                deadline = time.time() + stream_timeout_s

                async for line in resp.aiter_lines():
                    if time.time() > deadline:
                        logs.append(f"[TIMEOUT] Stream timeout após {stream_timeout_s}s")
                        break

                    if chunk_mode:
                        # NDJSON / chunked — cada linha é um JSON
                        try:
                            events.append({"data": line, "parsed": json.loads(line)})
                        except json.JSONDecodeError:
                            events.append({"data": line})
                        logs.append(f"[CHUNK] {line[:120]}")
                    else:
                        parsed = _parse_sse_line(line)
                        if parsed is None:
                            # Linha vazia = fim do evento atual
                            if current_event:
                                events.append(dict(current_event))
                                logs.append(f"[EVENT] type={current_event.get('event','(none)')} data={current_event.get('data','')[:80]}")
                                current_event = {}
                            if len(events) >= max_events:
                                break
                        else:
                            current_event[parsed["field"]] = parsed["value"]

        except httpx.ConnectError as e:
            error_msg = f"Falha de conexão: {e}"
        except httpx.TimeoutException:
            error_msg = f"Timeout de conexão ({TIMEOUT_MS}ms)"
        except Exception as e:
            error_msg = str(e) or f"{type(e).__name__} (sem mensagem)"

    return events, error_msg

def run_tc(tc: dict) -> dict:
    tc_id              = tc["id"]
    title              = tc["title"]
    endpoint           = tc.get("endpoint", "")
    url                = endpoint if endpoint.startswith("http") else f"{BASE_URL}{endpoint}"
    min_events         = int(tc.get("min_events", 1))
    max_events         = int(tc.get("max_events", 10))
    stream_timeout_s   = float(tc.get("stream_timeout_s", 15))
    event_types_exp    = tc.get("event_types_expected", [])
    data_pattern       = tc.get("data_pattern")
    chunk_mode         = bool(tc.get("chunk_mode", False))
    logs, assertions   = [], []
    error_msg          = None

    def _execute():
        nonlocal error_msg
        events, conn_error = asyncio.run(
            _collect_sse_events(url, min_events, max_events, stream_timeout_s,
                                event_types_exp, data_pattern, chunk_mode, logs))
        if conn_error:
            raise ConnectionError(conn_error)

        # Asserção: contagem mínima
        count_ok = len(events) >= min_events
        assertions.append({
            "description": f"Recebidos >= {min_events} eventos",
            "passed": count_ok,
            "actual": len(events),
        })
        if not count_ok:
            raise AssertionError(f"Esperados >= {min_events} eventos, recebidos {len(events)}")

        # Asserção: tipos de evento esperados presentes
        for et in event_types_exp:
            found = any(e.get("event") == et for e in events)
            assertions.append({"description": f"Tipo de evento '{et}' recebido", "passed": found, "actual": found})
            if not found:
                raise AssertionError(f"Tipo de evento '{et}' não recebido nos {len(events)} eventos coletados")

        # Asserção: padrão nos dados
        if data_pattern:
            pat = re.compile(data_pattern)
            matches = [e for e in events if pat.search(e.get("data", "") or json.dumps(e.get("parsed", {})))]
            pattern_ok = len(matches) > 0
            assertions.append({"description": f"Dados correspondem ao padrão '{data_pattern}'", "passed": pattern_ok, "actual": len(matches)})
            if not pattern_ok:
                raise AssertionError(f"Nenhum evento corresponde ao padrão '{data_pattern}'")

        logs.append(f"[OK] {len(events)} eventos coletados em {stream_timeout_s}s")

    result = run_with_retry(_execute, RETRY_COUNT)
    return make_tc_result(tc_id, title, "sse", result, assertions, logs, {})

test_cases = [
    # Structs injetados pelo orquestrador:
    # id, title, endpoint, min_events, max_events, stream_timeout_s,
    # event_types_expected (list), data_pattern (regex|null), chunk_mode (bool)
]

results = [run_tc(tc) for tc in test_cases]
summary = make_summary("executor-sse", results)
output  = {"summary": summary, "results": results}
out_file = os.path.join(SSE_DIR, "resultado.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print(json.dumps(output, ensure_ascii=False))
```

---

## Parsing de steps — exemplos canônicos

| Step | Extração |
|---|---|
| `Dado que o endpoint SSE é /api/events` | `endpoint = "/api/events"` |
| `Quando conectar e aguardar pelo menos 3 eventos` | `min_events = 3` |
| `E coletar por no máximo 20 segundos` | `stream_timeout_s = 20` |
| `Então o tipo de evento deve ser "heartbeat"` | `event_types_expected = ["heartbeat"]` |
| `E os dados devem conter o campo "status": "ok"` | `data_pattern = '"status":\\s*"ok"'` |
| `Dado que o endpoint retorna NDJSON em /api/stream` | `chunk_mode = true`, `endpoint = "/api/stream"` |
| `E deve receber até 50 chunks` | `max_events = 50` |

---

## Formato de saída

```json
{
  "summary": {
    "executor": "executor-sse",
    "total": 2, "passed": 2, "failed": 0, "skipped": 0, "error": 0,
    "warnings": [], "deploy_blocked": false
  },
  "results": [
    {
      "id": "TC-SSE-01", "title": "Stream de eventos de pedido",
      "type": "sse", "status": "passed", "error": "",
      "assertions": [
        {"description": "Recebidos >= 3 eventos", "passed": true, "actual": 5},
        {"description": "Tipo de evento 'order_update' recebido", "passed": true, "actual": true}
      ],
      "attempts": 1, "retry_diff_logs": false,
      "attempt_logs": [{"attempt": 1, "logs": [
        "[OK] Conexão estabelecida — 200 text/event-stream",
        "[EVENT] type=order_update data={\"orderId\":1,\"status\":\"shipped\"}",
        "[OK] 5 eventos coletados em 15s"
      ]}],
      "duration_ms": 8200, "evidence": {}
    }
  ]
}
```
