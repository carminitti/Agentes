---
name: profile-config-loader
description: Carrega o ProfileLoader e expõe o schema completo de profile_config para o classifier-testes e outros agentes que dependem de configuração dinâmica de framework/executor.
---

## Carregamento do ProfileLoader

Antes de classificar, carregue a config do profile ativo:

```python
from config.loader import ProfileLoader
import os

profile_name = os.getenv("QA_PROFILE", "default")
loader = ProfileLoader()
config = loader.load(profile_name)
executor_stack = config["executors"]
```

Agora, em vez de rotear fixo, descubra dinamicamente:
- Qual framework de browser usar: `executor_stack["browser"]["framework"]`
- Qual framework de performance: `executor_stack["performance"]["framework"]`
- Quais executores estão `enabled`/`disabled`

Se o orquestrador fornecer um `profile_config` pronto no contexto (ver estrutura abaixo), use-o diretamente — não chame o loader novamente.

## Estrutura do profile_config

```json
{
  "profile_name": "empresa-startup",
  "profile_config": {
    "executors": {
      "browser":        { "framework": "playwright", "timeout_ms": 15000, "browsers": ["chromium"], "headless": true },
      "api":            { "framework": "requests",   "timeout_ms": 15000, "max_retries": 1 },
      "performance":    { "framework": "k6",         "duration_s": 30, "vus": 5, "threshold_p95_ms": 200 },
      "visual":         { "framework": "playwright", "threshold_pixels": 3 },
      "acessibilidade": { "framework": "axe-core",   "wcag_level": "AA", "impact_filter": "all" },
      "seguranca":      { "method": "passive" },
      "banco":          { "driver": "postgres",      "timeout_s": 15 },
      "grpc":           { "server_reflection": true, "timeout_ms": 30000 },
      "graphql":        { "introspection_enabled": true, "timeout_ms": 30000 },
      "contrato":       { "enabled": false },
      "mobile":         { "enabled": false },
      "datadrive":      { "enabled": false },
      "chaos":          { "enabled": false }
    }
  }
}
```

Se `profile_config` não for fornecido nem carregável, use os fallbacks da tabela de resolução do classifier.

## Regras de backward compatibility

- Se o profile informado não existir, carregue `"default"` sem erro.
- Se `executors.<tipo>` não estiver declarado no default, use os valores hardcoded da tabela de fallback.
- Se a env `QA_PROFILE` não estiver definida, assuma `"default"`.
- Zero breaking changes: output sem `framework_config` é aceito por todos os executores existentes.
