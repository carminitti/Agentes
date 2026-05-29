# Diagnóstico de Performance — Squad QA
> Análise estática dos agentes em `agents/` — identificação de causas de lentidão na automação
> Data: 2026-05-20

---

## Resumo executivo

A lentidão do pipeline não tem uma causa única — ela resulta da **acumulação de atritos** em sete camadas distintas. O squad foi projetado com foco em robustez e rastreabilidade, o que é positivo, mas isso gerou decisões arquiteturais que penalizam o tempo total de execução. Os gargalos mais críticos estão no orquestrador (modelo de interação bloqueante), no tamanho dos prompts dos agentes, e na política de retry atual.

---

## 1. Contexto dos arquivos (tamanho dos prompts)

| Arquivo | Tamanho |
|---|---|
| `reporter-qa.md` | **121 KB** |
| `orquestrador-qa.md` | **117 KB** |
| `executor-browser.md` | 55 KB |
| `executor-api.md` | 32 KB |
| `classifier-testes.md` | 25 KB |
| **Total (5 agentes principais)** | **~350 KB** |

**Impacto:** cada invocação desses agentes obriga o modelo de linguagem a processar prompts enormes antes de gerar qualquer saída. O orquestrador (117 KB) e o reporter (121 KB) sozinhos representam mais de dois terços do contexto total. Quanto maior o prompt de sistema, mais tempo o modelo leva para "entrar no contexto" e começar a produzir tokens úteis — isso se soma a cada interação, não apenas na primeira.

**Causa:** evolução incremental sem refatoração. Cada versão adicionou regras novas sem remover as antigas, e o arquivo cresceu sem controle de tamanho.

---

## 2. Pontos de bloqueio no orquestrador (o maior gargalo)

O `orquestrador-qa.md` contém **83 ocorrências** de instruções do tipo `pergunte`, `aguarde` ou variantes. Isso significa 83 potenciais pontos onde o pipeline para e espera resposta humana.

O fluxo passa pelas seguintes etapas obrigatórias antes de executar um único teste:

```
Etapa -1   → Estado do Projeto (menu de modo)
Etapa -1B  → Fast Mode OU Custom Mode (mais perguntas)
Etapa -1C  → Modo Investigação (se aplicável)
Etapa R    → Retest (se aplicável)
Etapa 0    → Modo de execução (perfil, lean_mode, workers)
Etapa 1    → Classificação + confirmação de low_confidence
Etapa 2    → 9+ sub-etapas (URL, auth, timeout, blanket_permission...)
Etapa 3    → Dispatch para executores
Etapa 4    → Geração do relatório
```

**Pior padrão identificado:** mesmo quando um perfil salvo existe e já contém todas as configurações, o orquestrador instrui explicitamente:

> *"todas as perguntas de personalização de ambiente devem ser feitas e confirmadas pelo usuário — nunca pule a pergunta de timeout"*, *"nunca pule a pergunta de URL"*...

Ou seja, **o perfil não elimina nenhuma pergunta** — apenas pré-preenche os campos com valores padrão. O usuário ainda precisa confirmar tudo. Cada confirmação é um round-trip humano que pode durar segundos ou minutos.

**Impacto real:** se cada pergunta leva 10 segundos para ser respondida e há 12-15 perguntas no caminho feliz (Fast Mode + Etapa 2), o overhead de interação antes de rodar um único teste é de **2 a 4 minutos** — antes de qualquer código ser executado.

---

## 3. Política de retry acumulada

A skill `retry-strategy` define os seguintes delays máximos por executor em caso de falha:

| Executor | Retries | Delay máximo acumulado |
|---|---|---|
| executor-email | 3 tentativas | **35 segundos** (5s + 10s + 20s) |
| executor-webhook | 3 tentativas | **14 segundos** (2s + 4s + 8s) |
| executor-browser | 3 tentativas | **7 segundos** (1s + 2s + 4s) |
| executor-mobile | 2 tentativas | **6 segundos** (3s + 3s) |
| executor-websocket | 2 tentativas | **3 segundos** (1s + 2s) |

**Impacto em suites reais:** numa suite com 10 TCs de email que falham na primeira tentativa, o overhead de retry sozinho é de **350 segundos (quase 6 minutos)** — mesmo que todos eventualmente passem. Em suites mistas com muitos executores, isso se multiplica.

**Causa:** os delays foram definidos para acomodar serviços lentos (cold start de email, delay de webhook), o que é correto para ambientes de produção, mas é excessivo para ambientes de staging rápidos.

---

## 4. `lean_mode` não é o padrão

O orquestrador oferece dois modos de execução:

- **`lean_mode: false` (Suite completa):** gera HTML dual-mode com donut charts, syntax highlighting de código, screenshots por TC, logs completos, relatório Allure-style. O reporter tem 121 KB e gera saída potencialmente enorme.
- **`lean_mode: true` (Modo enxuto):** resumo inline, sem reporter, sem retry, sem screenshots extras.

O modo padrão quando o usuário escolhe "Suite completa" é `lean_mode: false`. Para uma execução rápida de validação pós-deploy, isso gera overhead desnecessário — o reporter precisa consolidar todos os JSONs dos executores, gerar HTML com evidências e código gerado, calcular métricas de cobertura etc. Tudo isso é feito ao final, de forma síncrona, bloqueando a entrega do resultado.

**Impacto:** runs de validação rápida (smoke/sanity) demoram quase tanto quanto uma suite completa porque passam pelo mesmo pipeline de relatório pesado.

---

## 5. Complexidade crescente do classifier (v1.43.0)

O `classifier-testes.md` está na versão 1.43.0 e acumulou:

- Carregamento dinâmico de `ProfileLoader` via Python
- Resolução de framework por 4 níveis: config > detecção heurística > fallback > plugin system
- Propagação de `framework_config` para todos os TCs
- Lógica de backward compatibility com versões anteriores
- Tabela com 26 tipos de teste e suas palavras-chave
- 7 regras de desambiguação explícitas
- Sistema de plugins para tipos desconhecidos

Cada TC classificado precisa passar por toda essa cadeia de decisões. Numa suite com 50+ TCs, isso representa processamento não trivial — especialmente a geração do JSON final, que deve ser completo antes de ser retornado.

**Causa:** cada versão adicionou capacidades (suporte a Selenium, JMeter, Gatling, httpx) sem simplificar o núcleo. A versão atual é ~3x mais complexa que uma versão inicial enxuta precisaria ser.

---

## 6. Pipeline `qa-pipeline` cria saltos desnecessários

Quando o usuário usa o `qa-pipeline`, o fluxo completo envolve **5 saltos de agente** antes de executar qualquer teste:

```
Usuário
  → qa-pipeline
    → gerador-criterios-aceite  (gera critérios + plano + mapa mental)
    → [aguarda resposta do usuário sobre formato]
    → gerador-cenarios-teste    (gera cenários a partir dos critérios)
    → [aguarda resposta do usuário sobre próximo formato]
    → classifier-testes         (classifica os cenários gerados)
    → orquestrador-qa           (executa os TCs)
      → executor-X, executor-Y...
```

O `gerador-criterios-aceite` gera três seções (critérios, plano de testes, mapa mental Mermaid), mas o `gerador-cenarios-teste` ignora duas delas. O mapa mental e o plano de testes são gerados, entregues ao usuário, e depois descartados. Isso é processamento desperdiçado — e adiciona tokens de saída que não contribuem para a execução.

Além disso, o `qa-pipeline` tem um **fluxo progressivo de formatos** onde oferece o mesmo conteúdo em Gherkin, depois em passo a passo, depois em CSV — cada um exigindo uma nova invocação do gerador e uma confirmação do usuário.

---

## 7. Verificação de saúde do ambiente (overhead fixo por execução)

A skill `environment-health-check` roda antes de cada suite. O timeout por verificação é de 5 segundos, mas com múltiplos endpoints (HTTP + auth + banco + fila), o overhead pode chegar a **15-20 segundos** por execução — mesmo quando o ambiente está saudável e o check é apenas confirmatório.

Para equipes que executam o pipeline várias vezes ao dia (ex: a cada PR), esse overhead fixo se acumula.

---

## 8. Ausência de CI/CD como execução padrão

Nenhum dos agentes força ou incentiva execução automatizada via CI/CD como padrão. A skill `ci-pipeline-generator` existe mas é opcional e invocada manualmente. O fluxo padrão é **manual** — o usuário precisa invocar o orquestrador, responder às perguntas, aguardar, etc.

Isso significa que cada ciclo de testes depende de disponibilidade humana para iniciar e acompanhar — o que cria latência contextual (esperas por ação humana) além da latência técnica.

---

## Tabela de priorização

| Causa | Impacto | Esforço para corrigir | Prioridade |
|---|---|---|---|
| Muitas confirmações obrigatórias no orquestrador | **Alto** | Médio | 🔴 Alta |
| Tamanho dos prompts (117-121 KB) | **Alto** | Alto | 🔴 Alta |
| `lean_mode` não padrão para smoke/sanity | **Médio** | Baixo | 🟡 Média |
| Retry delays longos (email: 35s) | **Médio** | Baixo | 🟡 Média |
| Perfil carregado mas confirmações não puladas | **Médio** | Baixo | 🟡 Média |
| Classifier sobrecarregado (v1.43.0) | **Médio** | Alto | 🟡 Média |
| Mapa mental Mermaid gerado mas descartado | **Baixo** | Baixo | 🟢 Baixa |
| Health-check fixo por execução | **Baixo** | Baixo | 🟢 Baixa |
| Ausência de CI/CD como padrão | **Alto** | Médio | 🔴 Alta |

---

## Recomendações

### Imediatas (baixo esforço)

**1. Criar modo `--autopilot` no orquestrador**
Quando o usuário passa `--autopilot`, o perfil carregado elimina todas as perguntas não obrigatórias. Apenas token/senha (dados sensíveis) são solicitados se ausentes. Reduz o fluxo de 15 perguntas para 1-2.

**2. Tornar `lean_mode` padrão para execuções com `< 10 TCs` ou tipo smoke/sanity**
Smoke e sanity não precisam de relatório HTML completo. Detectar automaticamente o tipo dominante e ajustar o modo.

**3. Reduzir delays de retry em ambientes de staging**
Expor parâmetro `retry_backoff_multiplier: 0.1` para staging. Um retry de email com 0.5s + 1s + 2s (total 3.5s) já é suficiente para ambientes rápidos.

**4. Remover geração do mapa mental Mermaid do `gerador-criterios-aceite`**
O mapa mental é explicitamente ignorado pelo `gerador-cenarios-teste` e só adiciona tokens de saída sem benefício no pipeline de execução.

### Médio prazo (esforço moderado)

**5. Dividir o `orquestrador-qa.md` em módulos**
Separar as etapas de coleta de informações (Etapas -1 a 2) de um módulo de execução puro (Etapas 3 e 4). O módulo de execução seria invocado diretamente pelo CI/CD, sem as etapas interativas.

**6. Habilitar CI/CD como fluxo padrão recomendado**
Fazer o `ci-pipeline-generator` ser sugerido proativamente ao final de toda primeira execução bem-sucedida, não apenas quando explicitamente solicitado.

**7. Simplificar o classifier para o núcleo essencial**
Remover backward compat com nomes legados (`magnitude`, `k6` como nome de executor) e o plugin system para tipos desconhecidos — esses raramente são usados e adicionam complexidade sem benefício frequente.

### Longo prazo (esforço alto)

**8. Refatorar os prompts grandes em prompts menores e compostos**
O orquestrador de 117 KB poderia ser dividido em: (a) prompt de coleta de informações, (b) prompt de dispatch, (c) prompt de consolidação. Cada um seria invocado em seu momento, reduzindo o contexto processado por invocação.

**9. Cache de tokens e sessões entre execuções**
Implementar verificação antes de re-autenticar: se o token salvo no `.env` ainda é válido (via endpoint `/me` ou `/auth/verify`), reutilizá-lo sem refazer o fluxo de login.
