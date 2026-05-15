# Prompt de Correção — casos-de-teste-gherkin-v2.md

Aplique as correções abaixo no arquivo `casos-de-teste-gherkin-v2.md`.
Altere apenas os trechos indicados — não modifique nenhum outro cenário.

---

## Correção 1 — Cabeçalhos de Feature com executor errado

### Onde está:
```
## Feature: Smoke — Disponibilidade de Ambiente (executor: magnitude / tipo: smoke)
```

### Substituir por:
```
## Feature: Smoke — Disponibilidade de Ambiente (executores: magnitude [TC-SMOKE-02,03,04] / http [TC-SMOKE-01,05] / tipos: smoke)
```

---

### Onde está:
```
## Feature: Sanity — Funcionalidades Críticas Após Deploy (executor: magnitude / tipo: sanity)
```

### Substituir por:
```
## Feature: Sanity — Funcionalidades Críticas Após Deploy (executores: magnitude [TC-SANITY-01,02,05] / http [TC-SANITY-03,04] / tipo: sanity)
```

---

## Correção 2 — TC-DB-01 e TC-DB-02: incompatíveis com executor-banco

O executor-banco não executa DDL diretamente. Em modo simulado ele **infere** o schema a partir dos steps e cria o SQLite por conta própria. Reescrever os dois cenários como verificações de estado, não como executores de DDL/DML.

### Substituir TC-DB-01 inteiro:

**Onde está:**
```gherkin
  Scenario: TC-DB-01 — Schema de usuários criado corretamente com todas as constraints
    Given o seguinte DDL é executado:
      """sql
      CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      """
    When a estrutura da tabela é inspecionada
    Then a tabela "users" deve existir
    And a coluna "id" deve ser PRIMARY KEY
    And a coluna "email" deve ter constraint UNIQUE e NOT NULL
    And a coluna "name" deve ter constraint NOT NULL
```

**Substituir por:**
```gherkin
  Scenario: TC-DB-01 — Tabela de usuários existe com todas as constraints de integridade
    Given o schema do banco está disponível
    And a tabela "users" foi provisionada com colunas: id (PK AUTOINCREMENT), email (UNIQUE NOT NULL), name (NOT NULL), created_at (DEFAULT CURRENT_TIMESTAMP)
    When o schema da tabela "users" é consultado via PRAGMA ou information_schema
    Then a tabela "users" deve existir no banco
    And a coluna "id" deve ser identificada como PRIMARY KEY
    And a coluna "email" deve ter as constraints UNIQUE e NOT NULL
    And a coluna "name" deve ter a constraint NOT NULL
```

---

### Substituir TC-DB-02 inteiro:

**Onde está:**
```gherkin
  Scenario: TC-DB-02 — Inserção de usuário válido persiste corretamente
    Given a tabela "users" foi criada
    When o seguinte INSERT é executado:
      """sql
      INSERT INTO users (email, name) VALUES ('gabriel@venturus.org.br', 'Gabriel Carminitti');
      """
    Then SELECT COUNT(*) FROM users deve retornar 1
    And o campo "email" do registro deve ser "gabriel@venturus.org.br"
```

**Substituir por:**
```gherkin
  Scenario: TC-DB-02 — Usuário inserido pela aplicação persiste corretamente no banco
    Given a aplicação registrou o usuário com email "gabriel@venturus.org.br" e nome "Gabriel Carminitti"
    When a tabela "users" é consultada com SELECT * FROM users WHERE email = 'gabriel@venturus.org.br'
    Then o resultado deve retornar exatamente 1 registro
    And o campo "email" do registro deve ser "gabriel@venturus.org.br"
    And o campo "name" do registro deve ser "Gabriel Carminitti"
    And o campo "created_at" deve estar preenchido com um timestamp válido
```

---

## Correção 3 — TC-SEC-10: open redirect é SPA, não detectável via Python requests

O Sauce Demo é uma SPA (React). O `?redirect=` seria processado por JavaScript — invisível para o executor-seguranca (Python requests). Este cenário deve ser tipo `e2e` com executor `magnitude` (Playwright), não `segurança`.

### Mover TC-SEC-10 da Feature de Segurança para a Feature de E2E do Sauce Demo

**Remover de `## Feature: Segurança`:**
```gherkin
  Scenario: TC-SEC-10 — Sauce Demo não realiza redirect aberto após login
    Given a URL "https://www.saucedemo.com/?redirect=https://evil.com" é acessada
    When o login é feito com "standard_user" / "secret_sauce"
    Then o redirect deve ser para uma URL interna da aplicação
    And não deve redirecionar para "https://evil.com"
```

**Adicionar no final de `## Feature: E2E — Sauce Demo` (após TC-E2E-10), dentro do bloco gherkin:**
```gherkin
  Scenario: TC-E2E-11 — Parâmetro redirect=URL_externa é ignorado após login (proteção open redirect)
    Given a URL "https://www.saucedemo.com/?redirect=https://evil.com" está aberta no navegador
    When o campo username é preenchido com "standard_user"
    And o campo password é preenchido com "secret_sauce"
    And o botão "Login" é clicado
    Then a URL atual deve conter "/inventory.html" ou outra rota interna do Sauce Demo
    And a URL atual não deve conter "evil.com"
    And o catálogo de produtos deve estar visível (sem redirecionamento externo)
```

**Atualizar o título da Feature E2E do Sauce Demo para refletir o novo total:**
```
## Feature: E2E — Sauce Demo — Fluxo Completo de Compra (executor: magnitude / tipo: e2e)
```
(sem mudança no título, apenas o bloco gherkin passa a ter 11 cenários)

---

## Correção 4 — TC-PERF-03: tabela round-robin em formato não confiável para o executor

Reescrever o step `When` com tabela Gherkin para texto explícito que o executor-performance (k6) interpreta sem ambiguidade.

### Onde está:
```gherkin
  Scenario: TC-PERF-03 — Carga alta: múltiplos endpoints com 50 VUs por 60s
    Given o número de usuários virtuais é 50
    And a duração do teste é 60 segundos
    When os seguintes endpoints são chamados em round-robin:
      | Método | Endpoint          |
      | GET    | /users?page=1     |
      | GET    | /users/2          |
      | POST   | /users            |
    Then o percentil p95 de tempo de resposta deve ser inferior a 4000ms
    And a taxa de erro deve ser inferior a 5%
```

### Substituir por:
```gherkin
  Scenario: TC-PERF-03 — Carga alta: múltiplos endpoints em round-robin com 50 VUs por 60s
    Given o número de usuários virtuais é 50
    And a duração do teste é 60 segundos
    When cada VU alterna ciclicamente entre os endpoints a seguir a cada iteração:
      endpoint 1 — GET /users?page=1 (sem body)
      endpoint 2 — GET /users/2 (sem body)
      endpoint 3 — POST /users com body '{"name":"LoadUser","job":"tester"}'
    Then o percentil p95 de tempo de resposta deve ser inferior a 4000ms
    And a taxa de erro deve ser inferior a 5%
    And os três endpoints devem ser chamados ao longo da execução (distribuição equilibrada)
```

---

## Correção 5 — Atualizar o Resumo de Cobertura ao final do arquivo

### Onde está:
```markdown
| e2e (Sauce Demo)    | magnitude | 10 |
| segurança           | zap       | 10 |
| **Total**           |           | **104** |
```

### Substituir por:
```markdown
| e2e (Sauce Demo)    | magnitude | 11 |
| segurança           | zap       | 9  |
| **Total**           |           | **104** |
```

(o total permanece 104 pois TC-SEC-10 foi movido para e2e como TC-E2E-11, não removido)

---

## Verificação pós-correção

Após aplicar todas as correções, confirme:

1. `grep -c "Scenario:" casos-de-teste-gherkin-v2.md` → deve retornar **104**
2. `grep "TC-SEC-10" casos-de-teste-gherkin-v2.md` → deve retornar **0 resultados** (cenário renomeado para TC-E2E-11)
3. `grep "TC-E2E-11" casos-de-teste-gherkin-v2.md` → deve retornar **1 resultado**
4. `grep "DDL é executado" casos-de-teste-gherkin-v2.md` → deve retornar **0 resultados**
5. `grep "INSERT INTO" casos-de-teste-gherkin-v2.md` → deve retornar **0 resultados**
6. `grep "round-robin:" casos-de-teste-gherkin-v2.md` → deve retornar **0 resultados** (substituído por texto explícito)
