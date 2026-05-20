---
name: flaky-test-detector
description: Detecta testes flaky com base no histórico de execuções (.qa_history.json) e no padrão de resultados da suite atual. Classifica flakiness por causa provável e recomenda ação.
---

## O que é um teste flaky

Um teste flaky passa em algumas execuções e falha em outras sem que o código tenha mudado. São mais perigosos que falhas consistentes porque mascaram problemas reais e geram falsa confiança.

## Critérios de detecção

### 1. Flaky confirmado (histórico)

Consulte `.qa_history.json` no `suite_dir` (últimas 10 execuções):

```python
import json, os

def detect_flaky_from_history(suite_dir, current_results):
    history_path = os.path.join(suite_dir or ".", ".qa_history.json")
    if not os.path.exists(history_path):
        return {}

    try:
        with open(history_path) as f:
            history = json.load(f)
    except Exception:
        return {}

    # Para cada TC: conta passadas e falhas nas últimas execuções
    tc_stats = {}
    for run in history[-5:]:  # últimas 5 execuções
        for r in run.get("results", []):
            tc_id = r.get("id")
            if not tc_id:
                continue
            if tc_id not in tc_stats:
                tc_stats[tc_id] = {"passed": 0, "failed": 0}
            if r.get("status") == "passed":
                tc_stats[tc_id]["passed"] += 1
            elif r.get("status") == "failed":
                tc_stats[tc_id]["failed"] += 1

    flaky = {}
    for tc_id, stats in tc_stats.items():
        total = stats["passed"] + stats["failed"]
        if total >= 2 and stats["passed"] > 0 and stats["failed"] > 0:
            flaky_rate = stats["failed"] / total
            flaky[tc_id] = {
                "flaky_rate": round(flaky_rate, 2),
                "runs_analyzed": total,
                "confirmed": flaky_rate >= 0.2  # falhou em ≥ 20% das execuções
            }
    return flaky
```

### 2. Flaky suspeito (suite atual)

Dentro da suite atual, marque como suspeito quando:
- `attempts > 1` e `status == "passed"` — passou somente após retry
- `retry_diff_logs: true` — logs diferentes entre tentativas (comportamento não-determinístico)

### 3. Flaky por padrão de erro

Classifique pelo padrão de erro quando o histórico confirma flakiness:

| Padrão de erro | Causa provável | Ação recomendada |
|---|---|---|
| `TimeoutError`, `Navigation timeout` | Timing / ambiente lento | Aumentar `timeout_ms`; adicionar `waitForLoadState('networkidle')` |
| `ElementNotFound`, `locator.click` | Race condition / animação | Adicionar `waitFor` antes da ação; usar `waitForSelector` |
| `net::ERR_CONNECTION_REFUSED` | Serviço intermitente | Verificar estabilidade do ambiente; adicionar retry no executor |
| `AssertionError` intermitente em API | Dado de estado compartilhado | Isolar dados de teste; usar fixtures por TC |
| `StaleElementReferenceException` | Re-render do DOM | Rebuscar o elemento após ação que cause re-render |
| Erro diferente a cada tentativa | Flakiness ambiental | Investigar logs de infraestrutura; isolar o TC |

## Output esperado

Para cada TC flaky detectado, produza:

```json
{
  "id": "TC-042",
  "title": "Login com SSO",
  "flaky": true,
  "flaky_confirmed": true,
  "flaky_rate": 0.4,
  "runs_analyzed": 5,
  "suspected_cause": "TimeoutError na navegação OAuth2",
  "cause_category": "timing",
  "recommended_action": "Aumentar timeout_ms para 30000 e adicionar waitForURL após redirect",
  "retry_divergence": true
}
```

## Integração com o reporter-qa

O reporter usa o campo `flaky: true` nos resultados do executor. Esta skill é usada pelo orquestrador para:
1. Detectar flakiness antes de chamar o reporter
2. Enriquecer os resultados com `flaky: true`, `flaky_rate` e `suspected_cause`
3. Decidir se recomenda re-run automático ao fim da suite
