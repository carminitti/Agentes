# Prompt de Correção — orquestrador-qa.md — Suporte a Múltiplas URLs (multi-domínio)

## Contexto do problema

O orquestrador coleta uma única `base_url` na **Etapa 2a** e a propaga para todos os executores via `## Contexto de execução`. Quando uma suite contém testes que apontam para domínios diferentes (ex: reqres.in, restful-booker.herokuapp.com, saucedemo.com), o executor-api recebe a `base_url` do contexto e ignora a URL do próprio step — fazendo chamadas para o domínio errado.

**Exemplo do problema:**
- Usuário responde `base_url = https://reqres.in/api` na Etapa 2a
- TC-BOOKER-02 tem steps com `https://restful-booker.herokuapp.com`
- executor-api usa o contexto → chama `https://reqres.in/api/booking` → 404

---

## Correção a aplicar no arquivo `agents/orquestrador-qa.md`

### 1 — Etapa 2a: detectar múltiplas URLs antes de perguntar

**Localizar este trecho em `## Etapa 2 — Coleta de informações obrigatórias`:**

```markdown
### 2a — URL do ambiente

Extraia a URL base do input do usuário ou dos steps dos testes. Se não for possível determinar com certeza, inclua na pergunta:

> "Qual é a URL base do ambiente a ser testado? (ex: `https://staging.app.com`)"
```

**Substituir por:**

```markdown
### 2a — URL do ambiente

Antes de formular a pergunta, analise todos os steps dos testes classificados e extraia todas as URLs base distintas presentes (padrão: `https://` ou `http://` seguido de domínio).

**Caso A — URL única ou nenhuma URL nos steps:**
Extraia a URL base do input do usuário ou dos steps dos testes. Se não for possível determinar com certeza, inclua na pergunta:
> "Qual é a URL base do ambiente a ser testado? (ex: `https://staging.app.com`)"
Armazene como `base_url` (string única). Registre `multi_url: false`.

**Caso B — Múltiplas URLs base distintas nos steps:**
Não pergunte `base_url` como campo único. Em vez disso, inclua na pergunta ao usuário:
> "Os testes cobrem múltiplos domínios diferentes. Confirme ou corrija as URLs detectadas para cada grupo de testes:
> - **Testes de integração/API** ([IDs]): `[URL detectada nos steps]`
> - **Testes de browser/E2E** ([IDs]): `[URL detectada nos steps]`
> - **Testes de performance** ([IDs]): `[URL detectada nos steps]`
> *(Deixe em branco para confirmar a URL detectada, ou informe a URL correta para o grupo)*"

Armazene o resultado como `url_map`:
```json
{
  "url_map": {
    "TC-API-01": "https://reqres.in/api",
    "TC-BOOKER-01": "https://restful-booker.herokuapp.com",
    "TC-E2E-01": "https://www.saucedemo.com"
  },
  "base_url": null
}
```
Registre `multi_url: true`. O campo `base_url` fica `null` neste caso.
```

---

### 2 — Contexto de execução: adicionar `url_map` e `multi_url`

**Localizar o bloco de definição do contexto** (após "monte o **contexto de execução**"):

```
contexto = {
  base_url: "https://staging.app.com",
```

**Substituir por:**

```
contexto = {
  base_url: "https://staging.app.com" | null,   // null quando multi_url: true
  multi_url: false | true,
  url_map: null | { "TC-XXX": "https://dominio-a.com", "TC-YYY": "https://dominio-b.com" },
```

---

### 3 — Etapa 2.9 (health check): adaptar para multi-url

**Localizar:**

```python
resp = requests.head(base_url, timeout=5, verify=False, allow_redirects=True)
env_reachable = resp.status_code < 500
```

**Substituir por:**

```python
# Determina quais URLs verificar
if multi_url:
    urls_to_check = list(set(url_map.values()))  # URLs únicas do mapa
else:
    urls_to_check = [base_url]

env_reachable = True
env_errors = []
for url in urls_to_check:
    try:
        resp = requests.head(url, timeout=5, verify=False, allow_redirects=True)
        if resp.status_code >= 500:
            env_reachable = False
            env_errors.append(f"{url} → HTTP {resp.status_code}")
    except Exception as e:
        env_reachable = False
        env_errors.append(f"{url} → {str(e)}")
```

E logo abaixo, ajustar a mensagem de erro:

**Localizar:**
```
> ⚠️ O ambiente `[base_url]` não respondeu (`[env_error]`).
```

**Substituir por:**
```
> ⚠️ Um ou mais ambientes não responderam:
> [para cada entrada em env_errors]: `[url]` — `[erro]`
> Verifique a URL, VPN ou certificado e confirme para continuar — ou cancele.
```

---

### 4 — Etapa 3: dispatch para executores com URL correta por TC

**Localizar a seção de montagem da mensagem para cada executor** (onde o orquestrador monta o `## Contexto de execução` antes de despachar). O trecho contém algo como:

```
## Contexto de execução
{
  "base_url": "[base_url]",
  ...
}
```

**Adicionar, logo após a construção do contexto por executor, a seguinte lógica antes do dispatch:**

```python
# Resolve a URL correta para cada TC deste executor
def resolve_url_for_tc(tc_id, contexto):
    if not contexto.get("multi_url"):
        return contexto["base_url"]
    return contexto["url_map"].get(tc_id, contexto["base_url"])

# Ao montar os TCs para o executor, anote a URL resolvida em cada TC:
for tc in tcs_deste_executor:
    tc["resolved_base_url"] = resolve_url_for_tc(tc["id"], contexto)

# No ## Contexto de execução enviado ao executor, use a URL do primeiro TC como base_url
# (os executores que lidam com URLs diferentes por TC devem ler `resolved_base_url` de cada TC)
base_url_executor = tcs_deste_executor[0]["resolved_base_url"] if tcs_deste_executor else contexto.get("base_url")
```

E incluir no bloco `## Contexto de execução` enviado ao subagente:

```json
{
  "base_url": "[base_url_executor]",
  "multi_url": true | false,
  "url_map": { "TC-XXX": "https://..." } | null,
  ...
}
```

---

### 5 — Instrução para os executores lerem `resolved_base_url`

Adicionar ao final da seção **Etapa 3**, como nota geral aplicada a todos os executores:

```markdown
> **Nota multi-URL:** quando o contexto contiver `"multi_url": true`, cada TC pode ter uma URL base diferente. Os executores devem ler o campo `resolved_base_url` do TC (quando presente) no lugar de `base_url` do contexto ao construir a URL de cada requisição ou navegação. Se `resolved_base_url` não estiver presente no TC, usar `base_url` do contexto como fallback.
```

---

## Verificação pós-correção

Após aplicar as alterações, confirme:

1. A Etapa 2a menciona "Caso A" e "Caso B" com detecção de múltiplas URLs
2. O schema do contexto contém os campos `multi_url` e `url_map`
3. O health check itera sobre `urls_to_check` (lista) em vez de `base_url` (string única)
4. O dispatch injeta `resolved_base_url` em cada TC antes de enviar ao executor
5. A nota "multi-URL" aparece na Etapa 3 orientando os executores
