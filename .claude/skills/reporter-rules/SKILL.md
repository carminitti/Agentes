---
name: reporter-rules
description: Regras canônicas de integridade e formato do reporter-qa. Use ao revisar ou manter reporter-qa.md.
---

# Regras do Reporter QA

## Regras de integridade dos dados

**Os dados passados pelos executores são a fonte de verdade.**

- Use exclusivamente os valores presentes nos JSONs recebidos — nunca estime, invente ou reutilize métricas de execuções anteriores.
- Se um campo não estiver presente no JSON, reporte como `"não verificável — dado ausente no resultado"`.
- Para falhas de browser, use a causa raiz exatamente como reportada no campo `error` ou `logs`. Nunca infira — se ausente, escreva `"causa não determinada"`.

## Regra de cobertura total

**Todo test case classificado deve aparecer no relatório — sem exceção.**

Cruze os IDs de `tests[]` do classifier com os IDs nos resultados de todos os executores. Para cada ID ausente, crie entrada com `status: "não executado"` e `motivo` específico.

O **Total classificado** deve bater com `summary.environment_tests` do classifier. Se divergir, sinalize:
> ⚠️ **Divergência de cobertura:** [N] caso(s) não aparecem em nenhum resultado.

## Regras de cálculo de status

| Status | Condição |
|--------|----------|
| Passou | `status == "passed"` (inclui `flaky: true` — conta como passou, exibe badge ⚠️) |
| Falhou | `status == "failed"` |
| Avisos | `status == "warning"` ou `"baseline_created"` |
| Não executado | `status == "skipped"` + tipos pact/appium |
| Suite reprovada | qualquer falha de smoke/sanity/segurança (severity high/medium) ou `deploy_blocked: true` |

**Severidade:** campo `severity` presente → use; senão por tipo: smoke/sanity/segurança = Alta; regressão/e2e/performance = Média; visual/acessibilidade/banco = Baixa.

## Formato de saída

**Resposta COMPLETA = HTML dual-mode.** Nada antes de `<!DOCTYPE html>`, nada depois de `</html>`.

Inclua bloco de resumo como comentário antes de `</body>`:
```
<!-- SUMMARY_TEXT
Suite: [suite_dir]
Ambiente: [URL]
Resultado: [✅ Aprovada | ❌ Reprovada — N falha(s) crítica(s)]
Passed: N | Failed: N | Warnings: N | Skipped: N
-->
```

### Reports separados por domínio

| Report | Conteúdo | Quando gerar |
|--------|----------|--------------|
| `relatorio.html` | Todos os testes EXCETO performance e segurança | Sempre |
| `relatorio-performance.html` | Somente executor `k6` (performance/carga/stress/soak/spike) | Apenas se houver testes de performance |
| `relatorio-seguranca.html` | Somente executor `zap` (segurança) | Apenas se houver testes de segurança |

Ao final da resposta, informe ao orquestrador: `{ "reports_generated": ["relatorio.html", ...] }`.

No relatório principal, onde seriam exibidos testes de performance/segurança, exiba apenas card de referência:
> "🔗 Testes de performance em report separado: `relatorio-performance.html`"
