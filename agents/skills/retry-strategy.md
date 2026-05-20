---
name: retry-strategy
description: Política canônica de retry unificada para todos os executores do Squad QA. Define tentativas por tipo, backoff exponencial, critério flaky vs falha real e integração com flaky-test-detector. Fonte de verdade — executores devem seguir esta tabela.
tools: ""
---

Tabela canônica de política de retry do Squad QA. Use como referência ao implementar ou auditar retry nos executores.

## Política por executor

| Executor | Retries padrão | Max retries | Backoff | Observação |
|---|---|---|---|---|
| executor-browser | 2 | 3 | exp 1s→2s→4s | Screenshot em cada tentativa; retry no TC inteiro |
| executor-visual | 1 | 2 | fixo 2s | Retry somente se diff > threshold; nunca em baseline criado |
| executor-api | 1 | 2 | exp 0.5s→1s | Retry apenas em 5xx, timeout, ConnectionError — **nunca em 4xx** |
| executor-seguranca | 0 | 1 | fixo 1s | Retry somente em timeout; violação de segurança nunca é flaky |
| executor-banco | 1 | 2 | fixo 1s | Retry em ConnectionError e DeadlockDetected; nunca em AssertionError |
| executor-performance | 0 | 0 | — | k6 não tem retry por TC; ajuste thresholds em vez de retry |
| executor-acessibilidade | 1 | 2 | fixo 1s | Retry se página não carregou; violação WCAG nunca é flaky |
| executor-websocket | 1 | 2 | exp 1s→2s | Retry em falha de conexão; nunca em erro de protocolo/frame |
| executor-grpc | 1 | 2 | exp 0.5s→1s | Retry em UNAVAILABLE/DEADLINE_EXCEEDED; nunca em INVALID_ARGUMENT |
| executor-graphql | 1 | 2 | exp 0.5s→1s | Retry em timeout e network error; nunca em erro de schema |
| executor-email | 2 | 3 | exp 5s→10s→20s | Email pode demorar; janela maior de retry |
| executor-webhook | 2 | 3 | exp 2s→4s→8s | Webhook pode ter delay de entrega |
| executor-queue | 1 | 2 | fixo 2s | Retry em timeout de polling; nunca em erro de schema de mensagem |
| executor-mobile | 1 | 2 | fixo 3s | Apps têm cold start; retry no TC inteiro |
| executor-chaos | 0 | 0 | — | Chaos testa falha — retry mascararia o resultado real |
| executor-datadrive | 0 | 0 | — | Dados determinísticos; retry não muda resultado |
| executor-i18n | 1 | 2 | fixo 1s | Retry se página não carregou; nunca em chave de tradução faltante |
| executor-contrato | 0 | 1 | fixo 1s | Retry somente em falha de conexão ao Pact Broker |

> O campo `retry_count` recebido no contexto do orquestrador **sobrescreve** o padrão da tabela acima.
> Em `lean_mode: true`, `retry_count` é sempre `0` — sem retry.

## Cálculo de backoff exponencial

```python
import time

def retry_with_backoff(func, max_retries: int, base_delay_s: float = 1.0, max_delay_s: float = 30.0):
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            last_error = e
            if attempt == max_retries:
                raise
            delay = min(base_delay_s * (2 ** attempt), max_delay_s)
            time.sleep(delay)
    raise last_error
```

## Classificação: flaky vs falha real

**Flaky (instável)** — TC é marcado como `flaky_suspected: true` quando:
- Passou em ≥1 e falhou em ≥1 das últimas 5 execuções
- Os erros de falha são **diferentes entre tentativas** (`retry_diff_logs: true`)
- Tipo de erro: `timeout`, `ElementNotFound`, `ConnectionError`, `NetworkError`

**Falha real** — TC nunca é marcado como flaky quando:
- Falhou em todas as execuções com o **mesmo erro** consistente
- Tipo de erro: `AssertionError`, `SchemaValidationError`, `HTTP 4xx`, `WCAG violation`, `ContractMismatch`

## Estrutura `attempt_logs` (obrigatória quando retry ocorrer)

```json
{
  "id": "TC-001",
  "status": "passed",
  "attempts": 2,
  "retry_diff_logs": true,
  "flaky_suspected": true,
  "attempt_logs": [
    { "attempt": 1, "status": "failed", "error": "ElementNotFoundError: #submit-btn", "duration_ms": 4200 },
    { "attempt": 2, "status": "passed", "error": null, "duration_ms": 2100 }
  ]
}
```

O `flaky-test-detector` usa `attempt_logs` para detectar padrões de instabilidade ao longo das execuções registradas em `.qa_history.json`.

## Regras absolutas

- **Nunca** aplique retry em erros 4xx — são determinísticos (BadRequest, Unauthorized, Forbidden, NotFound)
- Guarde logs de cada tentativa individualmente em `attempt_logs`
- Se logs de tentativas forem distintos, marque `retry_diff_logs: true` e destaque no relatório
- Após esgotar retries, o TC deve ser marcado como `failed` (não `error`) com `attempts: N` no resultado
