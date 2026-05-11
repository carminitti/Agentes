# Suite 3 — Casos de Teste Gherkin (2 por agente)

> Ambientes distintos das Suites 1 e 2.  
> Credenciais embutidas diretamente nos steps.  
> Fixes aplicados: `insecureSkipTLSVerify` nos TCs de performance; banco com fallback explícito nos steps.

---

## Feature: API — Reqres.in (executor: http / tipo: integração)

```gherkin
Feature: Autenticação e consulta de usuários via Reqres.in

  Background:
    Given a URL base da API é "https://reqres.in/api"
    And o Content-Type das requisições é "application/json"

  Scenario: TC-API-S3-001 — Autenticar usuário válido e receber token
    Given o endpoint de autenticação é "POST /login"
    And o corpo da requisição contém:
      | campo    | valor                  |
      | email    | eve.holt@reqres.in     |
      | password | cityslicka             |
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "token" com valor não vazio
    And o tempo de resposta deve ser inferior a 3000ms

  Scenario: TC-API-S3-002 — Listar usuários da página 2 e validar estrutura
    Given o endpoint é "GET /users?page=2"
    And nenhum header de autenticação é necessário
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "page" igual a 2
    And a resposta deve conter o campo "data" com ao menos 1 item
    And cada item do array "data" deve conter os campos: "id", "email", "first_name", "last_name"
    And o tempo de resposta deve ser inferior a 3000ms
```

---

## Feature: Browser — OrangeHRM Demo (executor: magnitude / tipo: e2e)

```gherkin
Feature: Login e navegação no painel do OrangeHRM

  Background:
    Given a URL base da aplicação é "https://opensource-demo.orangehrmlive.com"
    And o usuário de acesso é "Admin"
    And a senha de acesso é "admin123"
    And o ambiente pertence ao grupo DEMO_HOSTS

  Scenario: TC-BROWSER-S3-001 — Login com credenciais válidas e verificação do dashboard
    Given o usuário acessa a página "/web/index.php/auth/login"
    When o campo "Username" é preenchido com "Admin"
    And o campo "Password" é preenchido com "admin123"
    And o botão "Login" é clicado
    Then o dashboard deve ser exibido com o título "Dashboard"
    And o menu lateral deve conter a opção "PIM"
    And o menu lateral deve conter a opção "Leave"

  Scenario: TC-BROWSER-S3-002 — Navegação até o módulo PIM e listagem de funcionários
    Given o usuário está autenticado com "Admin" e senha "admin123"
    And o usuário está na página do dashboard
    When o menu "PIM" é clicado
    Then a página "Employee List" deve ser exibida
    And a tabela de funcionários deve conter ao menos uma linha de dados
    And o botão "Add Employee" deve estar visível na página
```

---

## Feature: Performance — JSONPlaceholder (executor: k6 / tipo: carga)

```gherkin
Feature: Teste de carga no JSONPlaceholder

  Background:
    Given a URL base é "https://jsonplaceholder.typicode.com"
    And a opção "insecureSkipTLSVerify" deve ser definida como "true" no script k6
    And nenhuma autenticação é necessária

  Scenario: TC-PERF-S3-001 — Carga em GET /posts com 10 VUs por 30 segundos
    Given o endpoint alvo é "GET /posts"
    And a configuração de carga é:
      | parâmetro | valor |
      | vus       | 10    |
      | duration  | 30s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de carga é executado
    Then a taxa de erros deve ser inferior a 1%
    And o p95 do tempo de resposta deve ser inferior a 2000ms
    And o throughput mínimo deve ser de 5 requisições por segundo

  Scenario: TC-PERF-S3-002 — Performance em POST /posts com criação de recursos
    Given o endpoint alvo é "POST /posts"
    And o corpo da requisição é:
      | campo  | valor           |
      | title  | Teste de carga  |
      | body   | Conteúdo gerado |
      | userId | 1               |
    And a configuração de performance é:
      | parâmetro | valor |
      | vus       | 5     |
      | duration  | 20s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de performance é executado
    Then o status HTTP de todas as requisições deve ser 201
    And o p95 do tempo de resposta deve ser inferior a 3000ms
    And a taxa de erros deve ser inferior a 2%
```

---

## Feature: Visual — Quotes to Scrape (executor: playwright-visual / tipo: visual)

```gherkin
Feature: Regressão visual no Quotes to Scrape

  Background:
    Given a URL base é "https://quotes.toscrape.com"
    And o threshold de diferença aceitável é 2%
    And nenhuma autenticação é necessária

  Scenario: TC-VISUAL-S3-001 — Regressão visual da página inicial de citações
    Given o usuário acessa a página "/"
    And a página é aguardada até o elemento "div.quote" estar visível
    When o screenshot da página completa é capturado com nome "quotes-home.png"
    Then a diferença em relação ao baseline não deve exceder 2% dos pixels
    And se não houver baseline, ele deve ser criado e marcado para validação manual

  Scenario: TC-VISUAL-S3-002 — Regressão visual da página de tags populares
    Given o usuário acessa a página "/tag/love/"
    And a página é aguardada até o elemento "div.quote" estar visível
    And elementos dinâmicos de data são ocultados antes do screenshot
    When o screenshot da área principal de conteúdo é capturado com nome "quotes-love-tag.png"
    Then a diferença em relação ao baseline não deve exceder 2% dos pixels
    And se não houver baseline, ele deve ser criado e marcado para validação manual
```

---

## Feature: Acessibilidade — Practice Automation (executor: axe-core / tipo: acessibilidade)

```gherkin
Feature: Conformidade WCAG 2.1 AA no Practice Automation

  Background:
    Given a URL base é "https://practiceautomation.com"
    And o nível WCAG alvo é "WCAG 2.1 AA"
    And nenhuma autenticação é necessária

  Scenario: TC-A11Y-S3-001 — Conformidade WCAG 2.1 AA no formulário de prática
    Given o usuário acessa a página "/practice-form/"
    And a página é aguardada até o formulário estar visível
    When a análise axe-core é executada com as tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações com impacto "critical"
    And não deve haver violações com impacto "serious"
    And violações com impacto "moderate" ou "minor" devem ser reportadas como avisos

  Scenario: TC-A11Y-S3-002 — Conformidade WCAG 2.1 AA na página inicial de citações
    Given o usuário acessa a URL "https://quotes.toscrape.com"
    And a página é aguardada até o elemento "div.quote" estar visível
    When a análise axe-core é executada com as tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações com impacto "critical"
    And não deve haver violações com impacto "serious"
    And o campo "deploy_blocked" deve ser "false" se não houver violações bloqueantes
```

---

## Feature: Segurança — FakeStore API (executor: zap / tipo: segurança)

```gherkin
Feature: Verificação de segurança na FakeStore API e Reqres.in

  Background:
    And nenhuma credencial de autenticação é necessária para os checks de segurança
    And a análise deve ser não invasiva

  Scenario: TC-SEC-S3-001 — Headers de segurança e CORS na FakeStore API
    Given a URL base é "https://fakestoreapi.com"
    And os endpoints a verificar são: "/products", "/products/1", "/users"
    When os headers de resposta são inspecionados
    Then os seguintes headers de segurança devem estar presentes:
      | header                  |
      | X-Content-Type-Options  |
      | X-Frame-Options         |
      | Strict-Transport-Security |
      | Content-Security-Policy |
    And o header "Server" não deve expor versão do software
    And requisições OPTIONS de CORS não devem retornar "Access-Control-Allow-Origin: *" em endpoints autenticados

  Scenario: TC-SEC-S3-002 — Proteção de endpoints autenticados no Reqres.in
    Given a URL base é "https://reqres.in/api"
    And os endpoints protegidos a verificar são: "/users", "/unknown"
    When requisições sem token de autenticação são enviadas aos endpoints
    Then o status HTTP deve ser 200 (API pública — comportamento esperado e documentado)
    And o endpoint "POST /register" sem body deve retornar 400 ou 422
    And o endpoint "POST /login" com credenciais inválidas deve retornar 400
    And nenhum stack trace ou informação interna deve aparecer nas respostas de erro
```

---

## Feature: Banco — Fallback SQLite (executor: db / tipo: banco)

```gherkin
Feature: Integridade de dados com fallback automático para SQLite

  Background:
    And se a conexão TCP falhar em até 5 segundos, o executor deve ativar fallback para SQLite :memory: automaticamente
    And o campo "mode" no resultado deve ser "simulated_fallback" quando o fallback for ativado
    And nenhum teste deve ser marcado como "failed" por falha de infraestrutura de rede

  Scenario: TC-DB-S3-001 — Integridade do schema de pedidos — MySQL com fallback
    Given a connection string primária é "mysql://qa_suite3:QAOrders2024@db.qa-suite3.com:3306/orders_db"
    And o schema esperado contém as tabelas:
      | tabela      | colunas principais                                          |
      | orders      | id, customer_name, total_amount, status, created_at        |
      | order_items | id, order_id, product_name, quantity, unit_price           |
    And os dados de teste a inserir são:
      | tabela  | customer_name | total_amount | status  |
      | orders  | QA Tester     | 150.00       | pending |
    When a conexão é estabelecida (real ou via fallback SQLite)
    Then as tabelas "orders" e "order_items" devem existir ou ser criadas no modo simulado
    And a coluna "customer_name" da tabela "orders" deve ter restrição NOT NULL
    And a coluna "total_amount" deve aceitar apenas valores numéricos positivos
    And a coluna "order_id" da tabela "order_items" deve ser chave estrangeira para "orders.id"
    And o registro inserido deve ser recuperável via SELECT com os mesmos valores

  Scenario: TC-DB-S3-002 — Integridade do schema de funcionários — PostgreSQL com fallback
    Given a connection string primária é "postgresql://qa_emp:QAEmp2024@ep-placeholder.us-east-1.aws.neon.tech:5432/employees_db"
    And o schema esperado contém as tabelas:
      | tabela      | colunas principais                              |
      | departments | id, name, budget                                |
      | employees   | id, name, department_id, salary, hire_date      |
    And os dados de teste a inserir são:
      | tabela      | name        | budget   |
      | departments | Engenharia  | 500000   |
    When a conexão é estabelecida (real ou via fallback SQLite)
    Then as tabelas "departments" e "employees" devem existir ou ser criadas no modo simulado
    And a coluna "salary" da tabela "employees" deve ter restrição CHECK salary > 0
    And a coluna "department_id" deve ser chave estrangeira para "departments.id"
    And uma inserção de funcionário com "department_id" inexistente deve falhar com erro de FK
    And o registro de departamento inserido deve ser recuperável via SELECT com os mesmos valores
```
