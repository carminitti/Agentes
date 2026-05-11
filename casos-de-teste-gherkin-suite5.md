# Suite 5 — Casos de Teste Gherkin (2 por agente)

> Ambientes verificados e distintos das Suites 1 a 4.
> Regras aplicadas:
> - APIs: apenas públicas, sem auth, com histórico de estabilidade comprovado
> - Acessibilidade: exclusivamente sites de organizações de referência WCAG
> - Banco: SQLite :memory: como ambiente primário (sem dependência de conexão TCP)
> - Performance: insecureSkipTLSVerify sempre presente
> - Nenhum placeholder em connection strings

---

## Feature: API — Countries REST + ISS Position (executor: http / tipo: integração)

```gherkin
Feature: Consulta em APIs públicas estáveis — Countries REST e Open Notify

  Background:
    And o Content-Type das requisições é "application/json"
    And nenhuma autenticação é necessária

  Scenario: TC-API-S5-001 — Consultar dados do Brasil na Countries REST API
    Given a URL base da API é "https://restcountries.com/v3.1"
    And o endpoint é "GET /name/brazil"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve ser um array com ao menos 1 item
    And o primeiro item deve conter o campo "name.common" igual a "Brazil"
    And o primeiro item deve conter o campo "capital" com valor "Brasília"
    And o primeiro item deve conter o campo "population" com valor numérico maior que 0
    And o primeiro item deve conter o campo "currencies" com a chave "BRL"
    And o tempo de resposta deve ser inferior a 4000ms

  Scenario: TC-API-S5-002 — Consultar posição atual da ISS via Open Notify
    Given a URL base da API é "http://api.open-notify.org"
    And o endpoint é "GET /iss-now.json"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "message" igual a "success"
    And a resposta deve conter o campo "timestamp" com valor numérico positivo
    And a resposta deve conter o campo "iss_position.latitude" com valor numérico
    And a resposta deve conter o campo "iss_position.longitude" com valor numérico
    And o tempo de resposta deve ser inferior a 4000ms
```

---

## Feature: Browser — Practice Software Testing (executor: magnitude / tipo: e2e)

```gherkin
Feature: Login e navegação em e-commerce de prática

  Background:
    Given a URL base da aplicação é "https://practicesoftwaretesting.com"
    And o usuário de acesso é "customer@practicesoftwaretesting.com"
    And a senha de acesso é "welcome01"
    And o ambiente pertence ao grupo DEMO_HOSTS

  Scenario: TC-BROWSER-S5-001 — Login com credenciais válidas e acesso ao catálogo
    Given o usuário acessa a página "/"
    When o menu "Sign in" ou botão de login é clicado
    And o campo de e-mail é preenchido com "customer@practicesoftwaretesting.com"
    And o campo de senha é preenchido com "welcome01"
    And o botão "Login" é clicado
    Then o usuário deve ser redirecionado para a área autenticada
    And o nome do cliente ou saudação de boas-vindas deve estar visível
    And o catálogo de produtos deve estar acessível

  Scenario: TC-BROWSER-S5-002 — Buscar produto por categoria e verificar listagem
    Given o usuário está autenticado com "customer@practicesoftwaretesting.com" e senha "welcome01"
    When o usuário acessa a seção de categorias de produtos
    And a primeira categoria disponível é selecionada
    Then a lista de produtos da categoria deve ser exibida
    And ao menos um produto deve estar visível com nome e preço
    And o botão de adicionar ao carrinho deve estar presente para ao menos um produto
```

---

## Feature: Performance — Dog CEO API + Countries REST (executor: k6 / tipo: performance e carga)

```gherkin
Feature: Teste de performance em APIs públicas de baixa latência

  Background:
    And a opção "insecureSkipTLSVerify" deve ser definida como "true" no script k6
    And nenhuma autenticação é necessária

  Scenario: TC-PERF-S5-001 — Carga em GET /breeds/image/random da Dog CEO API (6 VUs / 25s)
    Given a URL base é "https://dog.ceo/api"
    And o endpoint alvo é "GET /breeds/image/random"
    And a configuração de carga é:
      | parâmetro | valor |
      | vus       | 6     |
      | duration  | 25s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de carga é executado
    Then a taxa de erros deve ser inferior a 1%
    And o p95 do tempo de resposta deve ser inferior a 2500ms
    And cada resposta deve conter os campos "status" igual a "success" e "message" com URL de imagem

  Scenario: TC-PERF-S5-002 — Performance em GET /v3.1/all da Countries REST (5 VUs / 20s)
    Given a URL base é "https://restcountries.com/v3.1"
    And o endpoint alvo é "GET /all?fields=name,capital,population"
    And a configuração de performance é:
      | parâmetro | valor |
      | vus       | 5     |
      | duration  | 20s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de performance é executado
    Then o status HTTP de todas as requisições deve ser 200
    And o p95 do tempo de resposta deve ser inferior a 4000ms
    And a taxa de erros deve ser inferior a 2%
```

---

## Feature: Visual — A11Y Project + WebAIM (executor: playwright-visual / tipo: visual)

```gherkin
Feature: Regressão visual em páginas de referência de acessibilidade

  Background:
    And o threshold de diferença aceitável é 2%
    And nenhuma autenticação é necessária

  Scenario: TC-VISUAL-S5-001 — Regressão visual da página de checklist do A11Y Project
    Given o usuário acessa a URL "https://www.a11yproject.com/checklist/"
    And a página é aguardada até o elemento "main" estar visível
    And elementos dinâmicos de data ou contador são ocultados antes do screenshot
    When o screenshot da área de conteúdo principal é capturado com nome "a11y-checklist.png"
    Then a diferença em relação ao baseline não deve exceder 2% dos pixels
    And se não houver baseline, ele deve ser criado e marcado para validação manual

  Scenario: TC-VISUAL-S5-002 — Regressão visual da página de recursos do WebAIM
    Given o usuário acessa a URL "https://webaim.org/resources/"
    And a página é aguardada até o elemento "main" ou "article" estar visível
    When o screenshot da página completa é capturado com nome "webaim-resources.png"
    Then a diferença em relação ao baseline não deve exceder 2% dos pixels
    And se não houver baseline, ele deve ser criado e marcado para validação manual
```

---

## Feature: Acessibilidade — W3C WCAG + MDN Accessibility (executor: axe-core / tipo: acessibilidade)

```gherkin
Feature: Conformidade WCAG 2.1 AA em páginas de padrões e documentação oficial

  Background:
    And o nível WCAG alvo é "WCAG 2.1 AA"
    And nenhuma autenticação é necessária

  Scenario: TC-A11Y-S5-001 — Conformidade WCAG 2.1 AA na página de padrões WCAG do W3C
    Given o usuário acessa a URL "https://www.w3.org/WAI/standards-guidelines/wcag/"
    And a página é aguardada até o elemento "main" estar visível
    When a análise axe-core é executada com as tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações com impacto "critical"
    And não deve haver violações com impacto "serious"
    And o campo "deploy_blocked" deve ser "false"

  Scenario: TC-A11Y-S5-002 — Conformidade WCAG 2.1 AA na página de acessibilidade do MDN
    Given o usuário acessa a URL "https://developer.mozilla.org/en-US/docs/Web/Accessibility"
    And a página é aguardada até o elemento "main" estar visível
    When a análise axe-core é executada com as tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações com impacto "critical"
    And não deve haver violações com impacto "serious"
    And violações com impacto "moderate" ou "minor" devem ser reportadas apenas como avisos
```

---

## Feature: Segurança — PokéAPI + Nationalize (executor: zap / tipo: segurança)

```gherkin
Feature: Verificação de headers de segurança em APIs públicas de referência

  Background:
    And nenhuma credencial de autenticação é necessária
    And a análise deve ser não invasiva

  Scenario: TC-SEC-S5-001 — Headers de segurança e exposição de informações na PokéAPI
    Given a URL base é "https://pokeapi.co/api/v2"
    And os endpoints a verificar são: "/pokemon/1", "/type/1", "/ability/1"
    When os headers de resposta HTTP são inspecionados
    Then o header "Content-Type" deve conter "application/json"
    And o header "Server" não deve expor nome e versão do software subjacente
    And ausência de headers opcionais (HSTS, X-Frame-Options, CSP) deve ser registrada como aviso
    And nenhum endpoint de administração deve retornar 200 sem autenticação

  Scenario: TC-SEC-S5-002 — Headers de segurança e CORS na Nationalize API
    Given a URL base é "https://api.nationalize.io"
    And os endpoints a verificar são: "/?name=james", "/?name=maria"
    When os headers de resposta HTTP são inspecionados
    Then o status HTTP dos endpoints deve ser 200
    And o header "Content-Type" deve conter "application/json"
    And o header "Server" não deve expor versão do software
    And requisições CORS de origem arbitrária não devem expor dados de outros usuários
    And ausência de headers de segurança opcionais deve ser registrada como aviso, não falha
```

---

## Feature: Banco — SQLite :memory: como ambiente primário (executor: db / tipo: banco)

```gherkin
Feature: Integridade de schemas financeiro e de biblioteca em SQLite em memória

  Background:
    And o ambiente de banco de dados primário é "SQLite :memory:"
    And nenhuma conexão TCP externa é necessária
    And o campo "mode" no resultado deve ser "simulated"

  Scenario: TC-DB-S5-001 — Integridade do schema financeiro (accounts, transactions, balances)
    Given a connection string é "sqlite://:memory:"
    And o schema a criar contém as tabelas:
      | tabela       | colunas principais                                              |
      | accounts     | id, owner_name, account_type, balance, created_at              |
      | transactions | id, from_account_id, to_account_id, amount, transaction_date   |
      | balances     | id, account_id, computed_balance, computed_at                  |
    And os dados de teste a inserir são:
      | tabela   | owner_name  | account_type | balance  |
      | accounts | QA Tester   | checking     | 1000.00  |
    When o banco SQLite é inicializado e o schema é criado
    Then as tabelas "accounts", "transactions" e "balances" devem ser criadas com sucesso
    And a coluna "balance" de "accounts" deve ter restrição CHECK balance >= 0
    And a coluna "amount" de "transactions" deve ter restrição CHECK amount > 0
    And "from_account_id" e "to_account_id" devem ser chaves estrangeiras para "accounts.id"
    And uma transferência com "from_account_id" inexistente deve falhar com erro de FK
    And o registro de conta inserido deve ser recuperável via SELECT com os mesmos valores

  Scenario: TC-DB-S5-002 — Integridade do schema de biblioteca (books, authors, loans)
    Given a connection string é "sqlite://:memory:"
    And o schema a criar contém as tabelas:
      | tabela  | colunas principais                                        |
      | authors | id, name, nationality, birth_year                         |
      | books   | id, title, author_id, isbn, published_year, available     |
      | loans   | id, book_id, borrower_name, loan_date, return_date        |
    And os dados de teste a inserir são:
      | tabela  | name             | nationality | birth_year |
      | authors | Robert C. Martin | American    | 1952       |
    When o banco SQLite é inicializado e o schema é criado
    Then as tabelas "authors", "books" e "loans" devem ser criadas com sucesso
    And a coluna "author_id" de "books" deve ser chave estrangeira para "authors.id"
    And a coluna "isbn" de "books" deve ter restrição UNIQUE
    And a coluna "available" de "books" deve aceitar apenas os valores 0 e 1
    And a coluna "book_id" de "loans" deve ser chave estrangeira para "books.id"
    And uma inserção de livro com "author_id" inexistente deve falhar com erro de FK
    And o registro de autor inserido deve ser recuperável via SELECT com os mesmos valores
```
