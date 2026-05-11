# Suite 6 — Casos de Teste Gherkin (2 por agente)

> Ambientes distintos das Suites 1 a 5.
> Lição do MDN aplicada: acessibilidade apenas em páginas WAI "after" do W3C — criadas
> especificamente para demonstrar conformidade WCAG, não apenas organizações que apoiam
> acessibilidade.
> Banco: SQLite :memory: como primário em todos os TCs.
> Performance: insecureSkipTLSVerify presente em todos os scripts k6.

---

## Feature: API — Exchange Rate + Sunrise/Sunset (executor: http / tipo: integração)

```gherkin
Feature: Consulta em APIs públicas de dados em tempo real

  Background:
    And o Content-Type das requisições é "application/json"
    And nenhuma autenticação é necessária

  Scenario: TC-API-S6-001 — Consultar taxa de câmbio atual do USD via ExchangeRate API
    Given a URL base da API é "https://open.er-api.com/v6"
    And o endpoint é "GET /latest/USD"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "result" igual a "success"
    And a resposta deve conter o campo "base_code" igual a "USD"
    And a resposta deve conter o campo "rates.BRL" com valor numérico maior que 0
    And a resposta deve conter o campo "rates.EUR" com valor numérico maior que 0
    And o tempo de resposta deve ser inferior a 4000ms

  Scenario: TC-API-S6-002 — Consultar horário de nascer e pôr do sol em Brasília
    Given a URL base da API é "https://api.sunrise-sunset.org"
    And o endpoint é "GET /json?lat=-15.77&lng=-47.92&date=today&formatted=0"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "status" igual a "OK"
    And a resposta deve conter o campo "results.sunrise" com valor de data/hora válido
    And a resposta deve conter o campo "results.sunset" com valor de data/hora válido
    And a resposta deve conter o campo "results.day_length" com valor numérico positivo
    And o tempo de resposta deve ser inferior a 4000ms
```

---

## Feature: Browser — Demoblaze + Practice Software Testing (executor: magnitude / tipo: e2e)

```gherkin
Feature: Navegação e fluxo de compra em lojas demo

  Background:
    And o ambiente pertence ao grupo DEMO_HOSTS

  Scenario: TC-BROWSER-S6-001 — Navegar até categoria Laptops e verificar listagem no Demoblaze
    Given a URL base da aplicação é "https://www.demoblaze.com"
    And nenhuma autenticação é necessária para navegação
    When o usuário acessa a página "/"
    And a página é aguardada até a lista de categorias estar visível
    And a categoria "Laptops" é clicada
    Then a lista de produtos da categoria "Laptops" deve ser exibida
    And ao menos um produto deve estar visível com nome e preço
    And o título da página ou cabeçalho deve refletir a categoria selecionada

  Scenario: TC-BROWSER-S6-002 — Adicionar produto ao carrinho no Practice Software Testing
    Given a URL base da aplicação é "https://practicesoftwaretesting.com"
    And o usuário está autenticado com "customer@practicesoftwaretesting.com" e senha "welcome01"
    When o usuário acessa a listagem de produtos
    And o primeiro produto disponível é clicado
    And o botão "Add to cart" é clicado
    Then uma confirmação de adição ao carrinho deve ser exibida
    And o contador do carrinho deve ser incrementado em 1
    And o produto adicionado deve estar visível no carrinho
```

---

## Feature: Performance — Advice Slip + Open Trivia DB (executor: k6 / tipo: performance e carga)

```gherkin
Feature: Teste de performance em APIs públicas de conteúdo

  Background:
    And a opção "insecureSkipTLSVerify" deve ser definida como "true" no script k6
    And nenhuma autenticação é necessária

  Scenario: TC-PERF-S6-001 — Carga em GET /advice da Advice Slip API (8 VUs / 25s)
    Given a URL base é "https://api.adviceslip.com"
    And o endpoint alvo é "GET /advice"
    And a configuração de carga é:
      | parâmetro | valor |
      | vus       | 8     |
      | duration  | 25s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de carga é executado
    Then a taxa de erros deve ser inferior a 2%
    And o p95 do tempo de resposta deve ser inferior a 3000ms
    And cada resposta deve conter o campo "slip.advice" com texto não vazio

  Scenario: TC-PERF-S6-002 — Performance em GET /api.php da Open Trivia DB (5 VUs / 20s)
    Given a URL base é "https://opentdb.com"
    And o endpoint alvo é "GET /api.php?amount=5&type=boolean"
    And a configuração de performance é:
      | parâmetro | valor |
      | vus       | 5     |
      | duration  | 20s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de performance é executado
    Then o status HTTP de todas as requisições deve ser 200
    And o p95 do tempo de resposta deve ser inferior a 3500ms
    And a taxa de erros deve ser inferior a 2%
    And cada resposta deve conter o campo "response_code" igual a 0
```

---

## Feature: Visual — WebAIM Contrast + PokéAPI Docs (executor: playwright-visual / tipo: visual)

```gherkin
Feature: Regressão visual em páginas de documentação estáveis

  Background:
    And o threshold de diferença aceitável é 2%
    And nenhuma autenticação é necessária

  Scenario: TC-VISUAL-S6-001 — Regressão visual do artigo de contraste de cores do WebAIM
    Given o usuário acessa a URL "https://webaim.org/articles/contrast/"
    And a página é aguardada até o elemento "main" ou "article" estar visível
    And elementos dinâmicos (banners de cookie, contadores) são ocultados antes do screenshot
    When o screenshot da área de conteúdo principal é capturado com nome "webaim-contrast.png"
    Then a diferença em relação ao baseline não deve exceder 2% dos pixels
    And se não houver baseline, ele deve ser criado e marcado para validação manual

  Scenario: TC-VISUAL-S6-002 — Regressão visual da homepage da documentação PokéAPI
    Given o usuário acessa a URL "https://pokeapi.co"
    And a página é aguardada até o elemento "main" ou ".landing" estar visível
    When o screenshot da área acima da dobra é capturado com nome "pokeapi-home.png"
    Then a diferença em relação ao baseline não deve exceder 2% dos pixels
    And se não houver baseline, ele deve ser criado e marcado para validação manual
```

---

## Feature: Acessibilidade — W3C WAI Demo "After" (executor: axe-core / tipo: acessibilidade)

```gherkin
Feature: Conformidade WCAG 2.1 AA nas páginas WAI demo acessíveis do W3C

  Background:
    And o nível WCAG alvo é "WCAG 2.1 AA"
    And nenhuma autenticação é necessária
    And os ambientes são páginas "after" do demo W3C BAD — criadas especificamente
      para demonstrar conformidade WCAG, garantidamente acessíveis por design

  Scenario: TC-A11Y-S6-001 — Conformidade WCAG 2.1 AA na homepage acessível do W3C BAD demo
    Given o usuário acessa a URL "https://www.w3.org/WAI/demos/bad/after/home.html"
    And a página é aguardada até o elemento "main" ou "body" estar visível
    When a análise axe-core é executada com as tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações com impacto "critical"
    And não deve haver violações com impacto "serious"
    And o campo "deploy_blocked" deve ser "false"

  Scenario: TC-A11Y-S6-002 — Conformidade WCAG 2.1 AA na página de survey acessível do W3C BAD demo
    Given o usuário acessa a URL "https://www.w3.org/WAI/demos/bad/after/survey.html"
    And a página é aguardada até o formulário estar visível
    When a análise axe-core é executada com as tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações com impacto "critical"
    And não deve haver violações com impacto "serious"
    And violações com impacto "moderate" ou "minor" devem ser reportadas apenas como avisos
    And o campo "deploy_blocked" deve ser "false"
```

---

## Feature: Segurança — Advice Slip + Open Trivia DB (executor: zap / tipo: segurança)

```gherkin
Feature: Verificação de headers de segurança em APIs públicas de conteúdo

  Background:
    And nenhuma credencial de autenticação é necessária
    And a análise deve ser não invasiva

  Scenario: TC-SEC-S6-001 — Headers de segurança e exposição de dados na Advice Slip API
    Given a URL base é "https://api.adviceslip.com"
    And os endpoints a verificar são: "/advice", "/advice/search/work"
    When os headers de resposta HTTP são inspecionados
    Then o header "Content-Type" deve conter "application/json"
    And o header "Server" não deve expor nome e versão do software subjacente
    And ausência de headers opcionais (HSTS, CSP, X-Frame-Options) deve ser registrada
      como aviso, não como falha bloqueante
    And nenhuma informação de stack trace deve aparecer em respostas de erro

  Scenario: TC-SEC-S6-002 — Headers de segurança e endpoint de token na Open Trivia DB
    Given a URL base é "https://opentdb.com"
    And os endpoints a verificar são: "/api.php?amount=1", "/api_token.php?command=request"
    When os headers de resposta HTTP são inspecionados
    Then o status HTTP dos endpoints deve ser 200
    And o header "Content-Type" deve conter "application/json"
    And o header "Server" não deve expor versão do software
    And o endpoint de token não deve retornar tokens de outros usuários em requisições anônimas
    And ausência de headers de segurança opcionais deve ser registrada como aviso
```

---

## Feature: Banco — SQLite :memory: como primário (executor: db / tipo: banco)

```gherkin
Feature: Integridade de schemas de e-learning e saúde em SQLite em memória

  Background:
    And o ambiente de banco de dados primário é "sqlite://:memory:"
    And nenhuma conexão TCP externa é necessária
    And o campo "mode" no resultado deve ser "simulated"

  Scenario: TC-DB-S6-001 — Integridade do schema de e-learning (courses, students, enrollments)
    Given a connection string é "sqlite://:memory:"
    And o schema a criar contém as tabelas:
      | tabela      | colunas principais                                              |
      | courses     | id, title, instructor_name, duration_hours, max_students       |
      | students    | id, name, email, enrollment_date                               |
      | enrollments | id, course_id, student_id, progress_percent, completed_at      |
    And os dados de teste a inserir são:
      | tabela  | title              | instructor_name | duration_hours | max_students |
      | courses | QA Fundamentals    | Jane Doe        | 40             | 30           |
    When o banco SQLite é inicializado e o schema é criado
    Then as tabelas "courses", "students" e "enrollments" devem ser criadas com sucesso
    And a coluna "duration_hours" de "courses" deve ter restrição CHECK duration_hours > 0
    And a coluna "max_students" deve ter restrição CHECK max_students > 0
    And a coluna "progress_percent" de "enrollments" deve ter restrição CHECK entre 0 e 100
    And "course_id" e "student_id" de "enrollments" devem ser chaves estrangeiras válidas
    And uma matrícula com "course_id" inexistente deve falhar com erro de FK
    And o curso inserido deve ser recuperável via SELECT com os mesmos valores

  Scenario: TC-DB-S6-002 — Integridade do schema de saúde (patients, doctors, appointments)
    Given a connection string é "sqlite://:memory:"
    And o schema a criar contém as tabelas:
      | tabela       | colunas principais                                                    |
      | doctors      | id, name, specialty, crm                                              |
      | patients     | id, name, cpf, birth_date                                             |
      | appointments | id, doctor_id, patient_id, scheduled_at, status, notes               |
    And os dados de teste a inserir são:
      | tabela  | name        | specialty    | crm        |
      | doctors | Dr. QA Test | Cardiologia  | CRM-123456 |
    When o banco SQLite é inicializado e o schema é criado
    Then as tabelas "doctors", "patients" e "appointments" devem ser criadas com sucesso
    And a coluna "crm" de "doctors" deve ter restrição UNIQUE
    And a coluna "cpf" de "patients" deve ter restrição UNIQUE
    And a coluna "status" de "appointments" deve aceitar apenas "scheduled", "completed" ou "cancelled"
    And "doctor_id" e "patient_id" de "appointments" devem ser chaves estrangeiras válidas
    And uma consulta com "patient_id" inexistente deve falhar com erro de FK
    And o médico inserido deve ser recuperável via SELECT com os mesmos valores
```
