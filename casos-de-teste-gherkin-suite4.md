# Suite 4 — Casos de Teste Gherkin (2 por agente)

> Ambientes distintos das Suites 1, 2 e 3.
> Credenciais embutidas diretamente nos steps.
> Fixes consolidados: `insecureSkipTLSVerify` no performance, fallback automático no banco.

---

## Feature: API — Random User + Open Library (executor: http / tipo: integração)

```gherkin
Feature: Consulta em APIs públicas — Random User e Open Library

  Background:
    And o Content-Type das requisições é "application/json"
    And nenhuma autenticação é necessária

  Scenario: TC-API-S4-001 — Gerar 5 usuários aleatórios e validar estrutura
    Given a URL base da API é "https://randomuser.me"
    And o endpoint é "GET /api/?results=5&seed=qa-suite4"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o array "results" com exatamente 5 itens
    And cada item deve conter os campos: "gender", "name", "email", "phone", "nat"
    And o campo "name" de cada item deve conter "first" e "last" não vazios
    And o tempo de resposta deve ser inferior a 3000ms

  Scenario: TC-API-S4-002 — Buscar livros sobre "Clean Code" na Open Library
    Given a URL base da API é "https://openlibrary.org"
    And o endpoint é "GET /search.json?q=clean+code&limit=5"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "numFound" com valor maior que 0
    And a resposta deve conter o array "docs" com ao menos 1 item
    And cada item do array "docs" deve conter os campos "title" e "key"
    And o tempo de resposta deve ser inferior a 5000ms
```

---

## Feature: Browser — Buggy Cars Rating (executor: magnitude / tipo: e2e)

```gherkin
Feature: Login e avaliação de carro no Buggy Cars Rating

  Background:
    Given a URL base da aplicação é "https://buggy.justtestit.org"
    And o usuário de acesso é "user01"
    And a senha de acesso é "User0001!"
    And o ambiente pertence ao grupo DEMO_HOSTS

  Scenario: TC-BROWSER-S4-001 — Login com credenciais válidas e verificação do painel
    Given o usuário acessa a página "/"
    When o campo "Login" é preenchido com "user01"
    And o campo "Password" é preenchido com "User0001!"
    And o botão de login é clicado
    Then o usuário deve ser redirecionado para a página principal autenticada
    And o nome "user01" ou mensagem de boas-vindas deve estar visível na página
    And o menu de navegação deve estar disponível

  Scenario: TC-BROWSER-S4-002 — Navegar até lista de carros e acessar detalhe
    Given o usuário está autenticado com "user01" e senha "User0001!"
    When o usuário acessa a lista de modelos disponíveis
    And o primeiro modelo da lista é clicado
    Then a página de detalhe do modelo deve ser exibida
    And o campo de avaliação (rating) deve estar visível
    And o botão de submissão do voto deve estar presente na página
```

---

## Feature: Performance — Chuck Norris API + Agify (executor: k6 / tipo: performance e carga)

```gherkin
Feature: Teste de performance em APIs públicas leves

  Background:
    And a opção "insecureSkipTLSVerify" deve ser definida como "true" no script k6
    And nenhuma autenticação é necessária

  Scenario: TC-PERF-S4-001 — Carga em GET /jokes/random da Chuck Norris API (8 VUs / 30s)
    Given a URL base é "https://api.chucknorris.io"
    And o endpoint alvo é "GET /jokes/random"
    And a configuração de carga é:
      | parâmetro | valor |
      | vus       | 8     |
      | duration  | 30s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de carga é executado
    Then a taxa de erros deve ser inferior a 1%
    And o p95 do tempo de resposta deve ser inferior a 2000ms
    And cada resposta deve conter os campos "id", "value" e "url"

  Scenario: TC-PERF-S4-002 — Performance em GET /?name=test da Agify API (5 VUs / 20s)
    Given a URL base é "https://api.agify.io"
    And o endpoint alvo é "GET /?name=test"
    And a configuração de performance é:
      | parâmetro | valor |
      | vus       | 5     |
      | duration  | 20s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de performance é executado
    Then o status HTTP de todas as requisições deve ser 200
    And o p95 do tempo de resposta deve ser inferior a 2500ms
    And a taxa de erros deve ser inferior a 2%
```

---

## Feature: Visual — The Internet Herokuapp (executor: playwright-visual / tipo: visual)

```gherkin
Feature: Regressão visual em sub-páginas do The Internet Herokuapp

  Background:
    Given a URL base é "https://the-internet.herokuapp.com"
    And o threshold de diferença aceitável é 2%
    And nenhuma autenticação é necessária

  Scenario: TC-VISUAL-S4-001 — Regressão visual da página de checkboxes
    Given o usuário acessa a página "/checkboxes"
    And a página é aguardada até o elemento "form#checkboxes" estar visível
    When o screenshot da área de conteúdo principal é capturado com nome "internet-checkboxes.png"
    Then a diferença em relação ao baseline não deve exceder 2% dos pixels
    And se não houver baseline, ele deve ser criado e marcado para validação manual

  Scenario: TC-VISUAL-S4-002 — Regressão visual da página de dropdown
    Given o usuário acessa a página "/dropdown"
    And a página é aguardada até o elemento "select#dropdown" estar visível
    When o screenshot da página completa é capturado com nome "internet-dropdown.png"
    Then a diferença em relação ao baseline não deve exceder 2% dos pixels
    And se não houver baseline, ele deve ser criado e marcado para validação manual
```

---

## Feature: Acessibilidade — A11Y Project + WebAIM (executor: axe-core / tipo: acessibilidade)

```gherkin
Feature: Conformidade WCAG 2.1 AA em sites referência de acessibilidade

  Background:
    And o nível WCAG alvo é "WCAG 2.1 AA"
    And nenhuma autenticação é necessária

  Scenario: TC-A11Y-S4-001 — Conformidade WCAG 2.1 AA na página inicial do A11Y Project
    Given o usuário acessa a URL "https://www.a11yproject.com"
    And a página é aguardada até o elemento "main" estar visível
    When a análise axe-core é executada com as tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações com impacto "critical"
    And não deve haver violações com impacto "serious"
    And o campo "deploy_blocked" deve ser "false"

  Scenario: TC-A11Y-S4-002 — Conformidade WCAG 2.1 AA na introdução do WebAIM
    Given o usuário acessa a URL "https://webaim.org/intro/"
    And a página é aguardada até o elemento "main" ou "article" estar visível
    When a análise axe-core é executada com as tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações com impacto "critical"
    And não deve haver violações com impacto "serious"
    And violações com impacto "moderate" ou "minor" devem ser reportadas apenas como avisos
```

---

## Feature: Segurança — Chuck Norris API + Dog CEO API (executor: zap / tipo: segurança)

```gherkin
Feature: Verificação de headers e CORS em APIs públicas leves

  Background:
    And nenhuma credencial de autenticação é necessária
    And a análise deve ser não invasiva

  Scenario: TC-SEC-S4-001 — Headers de segurança e CORS na Chuck Norris API
    Given a URL base é "https://api.chucknorris.io"
    And os endpoints a verificar são: "/jokes/random", "/jokes/categories"
    When os headers de resposta HTTP são inspecionados
    Then os seguintes headers devem estar presentes ou ausência deve ser registrada como aviso:
      | header                    |
      | X-Content-Type-Options    |
      | X-Frame-Options           |
      | Strict-Transport-Security |
    And o header "Server" não deve expor nome e versão do software subjacente
    And requisições CORS de origem arbitrária não devem retornar dados sensíveis

  Scenario: TC-SEC-S4-002 — Headers de segurança e endpoint de listagem na Dog CEO API
    Given a URL base é "https://dog.ceo/api"
    And os endpoints a verificar são: "/breeds/list/all", "/breeds/image/random"
    When os headers de resposta HTTP são inspecionados
    Then o status HTTP dos endpoints deve ser 200
    And o header "Content-Type" deve ser "application/json"
    And o header "Server" não deve expor versão do software
    And nenhum endpoint de administração deve estar acessível sem autenticação
    And ausência de headers de segurança opcionais deve ser reportada como aviso, não falha
```

---

## Feature: Banco — Fallback SQLite (executor: db / tipo: banco)

```gherkin
Feature: Integridade de schemas de estoque e eventos com fallback automático

  Background:
    And se a conexão TCP falhar em até 5 segundos o executor ativa fallback para SQLite :memory: automaticamente
    And o campo "mode" no resultado deve ser "simulated_fallback" quando o fallback for ativado
    And nenhum teste deve ser marcado como "failed" por falha de infraestrutura de rede

  Scenario: TC-DB-S4-001 — Integridade do schema de inventário — MySQL com fallback
    Given a connection string primária é "mysql://qa_inv:QAInventory2024@db.qa-suite4.com:3306/inventory_db"
    And o schema esperado contém as tabelas:
      | tabela           | colunas principais                                         |
      | categories       | id, name, description                                      |
      | products         | id, name, category_id, unit_price, stock_quantity          |
      | stock_movements  | id, product_id, movement_type, quantity, moved_at          |
    And os dados de teste a inserir são:
      | tabela     | name        | description        |
      | categories | Eletrônicos | Produtos eletrônicos |
    When a conexão é estabelecida (real ou via fallback SQLite)
    Then as tabelas "categories", "products" e "stock_movements" devem existir ou ser criadas
    And a coluna "unit_price" de "products" deve ter restrição CHECK unit_price > 0
    And a coluna "category_id" de "products" deve ser chave estrangeira para "categories.id"
    And a coluna "movement_type" de "stock_movements" deve aceitar apenas "in" ou "out"
    And o registro de categoria inserido deve ser recuperável via SELECT com os mesmos valores

  Scenario: TC-DB-S4-002 — Integridade do schema de eventos — PostgreSQL com fallback
    Given a connection string primária é "postgresql://qa_evt:QAEvents2024@ep-placeholder.us-east-2.aws.neon.tech:5432/events_db"
    And o schema esperado contém as tabelas:
      | tabela        | colunas principais                                      |
      | events        | id, title, start_date, end_date, max_capacity           |
      | registrations | id, event_id, attendee_name, attendee_email, registered_at |
    And os dados de teste a inserir são:
      | tabela | title         | max_capacity |
      | events | QA Conference | 200          |
    When a conexão é estabelecida (real ou via fallback SQLite)
    Then as tabelas "events" e "registrations" devem existir ou ser criadas
    And a coluna "max_capacity" de "events" deve ter restrição CHECK max_capacity > 0
    And a coluna "end_date" deve ser maior ou igual a "start_date" (constraint de integridade)
    And a coluna "event_id" de "registrations" deve ser chave estrangeira para "events.id"
    And uma inserção de registration com "event_id" inexistente deve falhar com erro de FK
    And o registro de evento inserido deve ser recuperável via SELECT com os mesmos valores
```
