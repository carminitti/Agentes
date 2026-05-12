# Suite Master — 74 Casos de Teste Gherkin
# Cobertura completa de todas as funcionalidades dos agentes

> **APIs públicas:** PokéAPI, JSONPlaceholder, Countries REST, Dog CEO, Chuck Norris,
> Open Notify, Advice Slip, Open Trivia DB
> **APIs privadas (credenciais incluídas):**
> - NASA APOD → api_key: `DEMO_KEY`
> - Restful-Booker → admin / password123
> - DummyJSON → kminchelle / 0lelplR
> **Tipos cobertos:** integração, smoke, sanity, regressão, e2e, cross-browser,
> performance, carga, stress, soak, visual, acessibilidade, segurança, banco
> **Executores cobertos:** http, magnitude, k6, playwright-visual, axe-core, zap, db

---

## Feature: API Pública — PokéAPI (executor: http / tipo: integração)

```gherkin
Feature: Integração com PokéAPI — consultas e validações de estrutura

  Background:
    Given a URL base da API é "https://pokeapi.co/api/v2"
    And o Content-Type das requisições é "application/json"
    And nenhuma autenticação é necessária

  Scenario: TC-API-M01 — Consultar Pokémon por nome e validar campos obrigatórios
    Given o endpoint é "GET /pokemon/charizard"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "id" com valor numérico positivo
    And a resposta deve conter o campo "name" igual a "charizard"
    And a resposta deve conter o array "abilities" com ao menos 1 item
    And a resposta deve conter o array "types" com ao menos 1 item
    And o tempo de resposta deve ser inferior a 4000ms

  Scenario: TC-API-M02 — Listar Pokémons com paginação e validar estrutura
    Given o endpoint é "GET /pokemon?limit=10&offset=0"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "count" com valor maior que 1000
    And a resposta deve conter o array "results" com exatamente 10 itens
    And cada item de "results" deve conter os campos "name" e "url"
    And o campo "next" deve conter uma URL válida de próxima página

  Scenario: TC-API-M03 — Consultar habilidade por ID e validar descrição
    Given o endpoint é "GET /ability/1"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "name" não vazio
    And a resposta deve conter o array "pokemon" com ao menos 1 item
    And a resposta deve conter o array "effect_entries" com ao menos 1 item

  Scenario: TC-API-M04 — Consultar tipo Fogo e validar relações de dano
    Given o endpoint é "GET /type/fire"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "name" igual a "fire"
    And a resposta deve conter o objeto "damage_relations"
    And o array "damage_relations.double_damage_to" deve ter ao menos 1 item

  Scenario: TC-API-M05 — Consultar Pokémon inexistente e validar 404
    Given o endpoint é "GET /pokemon/pokemon-que-nao-existe-99999"
    When a requisição é enviada
    Then o status HTTP deve ser 404
    And o tempo de resposta deve ser inferior a 4000ms
```

---

## Feature: API Privada — NASA APOD (executor: http / tipo: integração)

```gherkin
Feature: Integração com NASA APOD — autenticação por API key

  Background:
    Given a URL base da API é "https://api.nasa.gov"
    And o Content-Type das requisições é "application/json"
    And a API key de acesso é "DEMO_KEY"

  Scenario: TC-API-M06 — Consultar imagem astronômica do dia com DEMO_KEY
    Given o endpoint é "GET /planetary/apod?api_key=DEMO_KEY"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "title" não vazio
    And a resposta deve conter o campo "date" com formato de data YYYY-MM-DD
    And a resposta deve conter o campo "media_type" com valor "image" ou "video"
    And a resposta deve conter o campo "url" com URL válida

  Scenario: TC-API-M07 — Consultar imagem de data específica com DEMO_KEY
    Given o endpoint é "GET /planetary/apod?api_key=DEMO_KEY&date=2024-01-15"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "date" igual a "2024-01-15"
    And a resposta deve conter o campo "explanation" não vazio

  Scenario: TC-API-M08 — Consultar múltiplas imagens com count e DEMO_KEY
    Given o endpoint é "GET /planetary/apod?api_key=DEMO_KEY&count=3"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve ser um array com exatamente 3 itens
    And cada item deve conter os campos "title", "date" e "url"

  Scenario: TC-API-M09 — Rejeitar requisição com API key inválida
    Given o endpoint é "GET /planetary/apod?api_key=CHAVE_INVALIDA_TESTE"
    When a requisição é enviada
    Then o status HTTP deve ser 403
    And a resposta deve conter mensagem de erro indicando chave inválida

  Scenario: TC-API-M10 — Rejeitar requisição sem API key
    Given o endpoint é "GET /planetary/apod"
    When a requisição é enviada sem parâmetro api_key
    Then o status HTTP deve ser 403
    And a resposta não deve conter dados astronômicos
```

---

## Feature: API Privada — Restful-Booker (executor: http / tipo: integração)

```gherkin
Feature: Integração com Restful-Booker — autenticação e CRUD de reservas

  Background:
    Given a URL base da API é "https://restful-booker.herokuapp.com"
    And o Content-Type das requisições é "application/json"
    And as credenciais de administrador são username "admin" e password "password123"

  Scenario: TC-API-M11 — Gerar token de autenticação com credenciais válidas
    Given o endpoint é "POST /auth"
    And o corpo da requisição contém username "admin" e password "password123"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "token" com valor não vazio
    And o token deve ter comprimento maior que 8 caracteres

  Scenario: TC-API-M12 — Criar nova reserva e validar campos retornados
    Given o endpoint é "POST /booking"
    And o corpo da requisição contém:
      | campo           | valor       |
      | firstname       | QA          |
      | lastname        | Tester      |
      | totalprice      | 250         |
      | depositpaid     | true        |
      | checkin         | 2026-06-01  |
      | checkout        | 2026-06-05  |
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "bookingid" com valor numérico positivo
    And a resposta deve conter o campo "booking.firstname" igual a "QA"

  Scenario: TC-API-M13 — Listar todas as reservas e validar estrutura
    Given o endpoint é "GET /booking"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve ser um array com ao menos 1 item
    And cada item deve conter o campo "bookingid" com valor numérico

  Scenario: TC-API-M14 — Consultar reserva por ID e validar dados
    Given uma reserva foi criada anteriormente via POST /booking com firstname "QA"
    And o endpoint é "GET /booking/{bookingid}"
    When a requisição é enviada com o ID da reserva criada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "firstname" igual a "QA"
    And a resposta deve conter o campo "lastname" igual a "Tester"

  Scenario: TC-API-M15 — Atualizar reserva existente com token de autorização
    Given o token de autenticação foi obtido via POST /auth com admin/password123
    And uma reserva existente foi identificada por ID
    And o endpoint é "PUT /booking/{bookingid}"
    And o header "Cookie" contém "token={token_obtido}"
    And o corpo da requisição contém firstname "QA-Updated" e totalprice 300
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "firstname" igual a "QA-Updated"
    And a resposta deve conter o campo "totalprice" igual a 300
```

---

## Feature: Browser — SauceDemo — Smoke Tests (executor: magnitude / tipo: smoke)

```gherkin
Feature: Smoke tests de saúde básica no SauceDemo

  Background:
    Given a URL base da aplicação é "https://www.saucedemo.com"
    And o ambiente pertence ao grupo DEMO_HOSTS

  Scenario: TC-BROWSER-M01 — Smoke: sistema sobe e login está disponível
    Given o usuário acessa a página "/"
    Then a página de login deve ser exibida
    And o campo "username" deve estar visível
    And o campo "password" deve estar visível
    And o botão "LOGIN" deve estar presente e habilitado

  Scenario: TC-BROWSER-M02 — Smoke: login com credenciais válidas retorna catálogo
    Given o usuário acessa a página "/"
    When o campo "username" é preenchido com "standard_user"
    And o campo "password" é preenchido com "secret_sauce"
    And o botão "LOGIN" é clicado
    Then a página de inventário deve ser exibida
    And ao menos um produto deve estar visível
    And o título "Swag Labs" deve estar presente no cabeçalho
```

---

## Feature: Browser — OrangeHRM — Sanity Tests (executor: magnitude / tipo: sanity)

```gherkin
Feature: Sanity tests após deploy no OrangeHRM

  Background:
    Given a URL base da aplicação é "https://opensource-demo.orangehrmlive.com"
    And o ambiente pertence ao grupo DEMO_HOSTS

  Scenario: TC-BROWSER-M03 — Sanity: módulos principais acessíveis após login
    Given o usuário acessa "/web/index.php/auth/login"
    When o campo "Username" é preenchido com "Admin"
    And o campo "Password" é preenchido com "admin123"
    And o botão "Login" é clicado
    Then o dashboard deve carregar sem erros
    And o menu lateral deve conter os itens "PIM", "Leave" e "Admin"
    And nenhuma mensagem de erro deve estar visível na tela

  Scenario: TC-BROWSER-M04 — Sanity: módulo Admin carrega corretamente
    Given o usuário está autenticado com "Admin" e senha "admin123"
    When o item "Admin" do menu lateral é clicado
    Then a página "User Management" deve ser exibida
    And a tabela de usuários deve estar visível
    And o botão "Add" deve estar disponível
```

---

## Feature: Browser — Practice Software Testing — Regressão (executor: magnitude / tipo: regressão)

```gherkin
Feature: Testes de regressão no Practice Software Testing

  Background:
    Given a URL base da aplicação é "https://practicesoftwaretesting.com"
    And o usuário está autenticado com "customer@practicesoftwaretesting.com" e senha "welcome01"
    And o ambiente pertence ao grupo DEMO_HOSTS

  Scenario: TC-BROWSER-M05 — Regressão: listagem de produtos continua funcionando
    Given o usuário acessa a página de catálogo de produtos
    Then ao menos 6 produtos devem estar visíveis
    And cada produto deve exibir nome, preço e imagem
    And o comportamento anterior de exibição de produtos não deve ter mudado

  Scenario: TC-BROWSER-M06 — Regressão: busca por termo retorna resultados filtrados
    Given o usuário está na página de catálogo
    When o campo de busca é preenchido com "Hammer"
    And a busca é executada
    Then os resultados devem conter apenas produtos com "Hammer" no nome
    And o número de resultados deve ser menor que o total de produtos

  Scenario: TC-BROWSER-M07 — Regressão: adicionar ao carrinho atualiza contador
    Given o catálogo de produtos está visível
    When o primeiro produto disponível é clicado
    And o botão "Add to cart" é clicado
    Then o contador do carrinho no cabeçalho deve ser incrementado em 1
    And o comportamento de adição ao carrinho não deve ter regredido
```

---

## Feature: Browser — Demoblaze — E2E (executor: magnitude / tipo: e2e)

```gherkin
Feature: Fluxo completo de compra no Demoblaze

  Background:
    Given a URL base da aplicação é "https://www.demoblaze.com"
    And o ambiente pertence ao grupo DEMO_HOSTS

  Scenario: TC-BROWSER-M08 — E2E: fluxo completo — navegar, selecionar e adicionar ao carrinho
    Given o usuário acessa a página "/"
    When a categoria "Phones" é clicada
    And o primeiro produto da listagem é selecionado
    And o botão "Add to cart" é clicado
    Then um alerta de confirmação de adição deve aparecer
    And o produto deve estar disponível no carrinho

  Scenario: TC-BROWSER-M09 — E2E: navegação entre categorias exibe produtos diferentes
    Given o usuário está na página inicial
    When a categoria "Laptops" é selecionada
    Then produtos da categoria Laptops devem ser exibidos
    When a categoria "Monitors" é selecionada
    Then produtos da categoria Monitors devem ser exibidos
    And os produtos de Monitors devem ser diferentes dos de Laptops

  Scenario: TC-BROWSER-M10 — E2E: formulário de contato pode ser submetido
    Given o usuário acessa a página inicial
    When o link "Contact" no menu de navegação é clicado
    And o modal de contato é exibido
    And o campo "Contact Email" é preenchido com "qa@test.com"
    And o campo "Message" é preenchido com "Teste de contato E2E"
    And o botão "Send message" é clicado
    Then uma confirmação de envio deve ser exibida
```

---

## Feature: Browser — Buggy Cars — E2E com Autenticação (executor: magnitude / tipo: e2e)

```gherkin
Feature: Fluxo de avaliação de carros no Buggy Cars Rating

  Background:
    Given a URL base da aplicação é "https://buggy.justtestit.org"
    And o usuário de acesso é "user01"
    And a senha de acesso é "User0001!"
    And o ambiente pertence ao grupo DEMO_HOSTS

  Scenario: TC-BROWSER-M11 — E2E: login e verificação de painel autenticado
    Given o usuário acessa a página "/"
    When o campo "Login" é preenchido com "user01"
    And o campo "Password" é preenchido com "User0001!"
    And o botão de login é clicado
    Then o usuário deve ser autenticado com sucesso
    And a saudação ou nome do usuário deve estar visível

  Scenario: TC-BROWSER-M12 — E2E: navegar até detalhe de modelo e visualizar rating
    Given o usuário está autenticado com "user01" e senha "User0001!"
    When a lista de modelos disponíveis é acessada
    And o primeiro modelo é clicado
    Then a página de detalhe do modelo deve carregar
    And a seção de avaliação (Overall Rating) deve estar visível
    And o campo de comentário deve estar disponível

  Scenario: TC-BROWSER-M13 — E2E: logout redireciona para página de login
    Given o usuário está autenticado com "user01" e senha "User0001!"
    When o botão ou link de logout é clicado
    Then o usuário deve ser redirecionado para a página de login
    And o formulário de login deve estar visível novamente
```

---

## Feature: Browser — Cross-Browser — The Internet (executor: magnitude / tipo: cross-browser)

```gherkin
Feature: Compatibilidade cross-browser em The Internet Herokuapp

  Background:
    Given a URL base da aplicação é "https://the-internet.herokuapp.com"
    And os navegadores a testar são: Chromium, Firefox, WebKit
    And os binários dos navegadores devem estar instalados:
      "npx playwright install chromium firefox webkit"

  Scenario: TC-BROWSER-M14 — Cross-browser: página de checkboxes funciona em múltiplos navegadores
    Given o usuário acessa "/checkboxes" em cada navegador configurado
    When o primeiro checkbox é clicado em cada navegador
    Then o estado do checkbox deve alternar em todos os navegadores
    And o comportamento deve ser consistente entre Chromium, Firefox e WebKit

  Scenario: TC-BROWSER-M15 — Cross-browser: dropdown funciona em múltiplos navegadores
    Given o usuário acessa "/dropdown" em cada navegador configurado
    When a opção "Option 1" é selecionada no dropdown em cada navegador
    Then o dropdown deve exibir "Option 1" como selecionado em todos os navegadores
    And o comportamento deve ser idêntico entre Chromium, Firefox e WebKit
```

---

## Feature: Performance — JSONPlaceholder (executor: k6 / tipo: performance e carga)

```gherkin
Feature: Testes de performance e carga no JSONPlaceholder

  Background:
    And a opção "insecureSkipTLSVerify" deve ser definida como "true" no script k6
    And nenhuma autenticação é necessária

  Scenario: TC-PERF-M01 — Performance: GET /posts sob carga moderada (10 VUs / 30s)
    Given a URL base é "https://jsonplaceholder.typicode.com"
    And o endpoint alvo é "GET /posts"
    And a configuração de performance é:
      | parâmetro | valor |
      | vus       | 10    |
      | duration  | 30s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de performance é executado
    Then a taxa de erros deve ser inferior a 1%
    And o p95 do tempo de resposta deve ser inferior a 2000ms
    And o throughput mínimo deve ser de 5 requisições por segundo

  Scenario: TC-PERF-M02 — Carga: GET /users com volume alto (30 VUs / 60s)
    Given a URL base é "https://jsonplaceholder.typicode.com"
    And o endpoint alvo é "GET /users"
    And a configuração de carga é:
      | parâmetro | valor |
      | vus       | 30    |
      | duration  | 60s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de carga é executado
    Then a taxa de erros deve ser inferior a 2%
    And o p95 do tempo de resposta deve ser inferior a 3000ms
    And o sistema deve manter throughput estável durante toda a duração
```

---

## Feature: Performance — Dog CEO API (executor: k6 / tipo: stress)

```gherkin
Feature: Testes de stress na Dog CEO API

  Background:
    And a opção "insecureSkipTLSVerify" deve ser definida como "true" no script k6
    And nenhuma autenticação é necessária

  Scenario: TC-PERF-M03 — Stress: ramp up até 100 VUs em 2 minutos
    Given a URL base é "https://dog.ceo/api"
    And o endpoint alvo é "GET /breeds/image/random"
    And a configuração de stress usa ramp up:
      | etapa  | target | duration |
      | 1      | 0      | 0s       |
      | 2      | 50     | 30s      |
      | 3      | 100    | 60s      |
      | 4      | 100    | 30s      |
      | 5      | 0      | 10s      |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de stress é executado
    Then a taxa de erros no pico não deve exceder 10%
    And o sistema deve se recuperar ao reduzir carga (error rate < 2% no ramp-down)
    And o ponto de degradação deve ser identificado no relatório

  Scenario: TC-PERF-M04 — Stress: carga além do esperado em /breeds/list/all (50 VUs / 60s)
    Given a URL base é "https://dog.ceo/api"
    And o endpoint alvo é "GET /breeds/list/all"
    And a configuração de stress é:
      | parâmetro | valor |
      | vus       | 50    |
      | duration  | 60s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de stress é executado
    Then a taxa de erros deve ser inferior a 5%
    And a resposta deve sempre conter o campo "status" igual a "success"
```

---

## Feature: Performance — Advice Slip + Open Trivia (executor: k6 / tipo: soak)

```gherkin
Feature: Testes de soak para estabilidade de longa duração

  Background:
    And a opção "insecureSkipTLSVerify" deve ser definida como "true" no script k6
    And nenhuma autenticação é necessária
    And testes de soak usam vus e duration — nunca stages

  Scenario: TC-PERF-M05 — Soak: Advice Slip estável por 10 minutos (20 VUs)
    Given a URL base é "https://api.adviceslip.com"
    And o endpoint alvo é "GET /advice"
    And a configuração de soak é:
      | parâmetro | valor |
      | vus       | 20    |
      | duration  | 10m   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de soak é executado
    Then a taxa de erros deve ser inferior a 1% durante todo o período
    And não deve haver aumento progressivo do tempo de resposta (indício de memory leak)
    And o p95 ao final deve ser similar ao p95 do início (variação < 20%)

  Scenario: TC-PERF-M06 — Soak: Open Trivia DB estável por 10 minutos (10 VUs)
    Given a URL base é "https://opentdb.com"
    And o endpoint alvo é "GET /api.php?amount=1&type=boolean"
    And a configuração de soak é:
      | parâmetro | valor |
      | vus       | 10    |
      | duration  | 10m   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de soak é executado
    Then a taxa de erros deve ser inferior a 2% durante todo o período
    And o sistema não deve apresentar degradação progressiva de latência
```

---

## Feature: Performance — Chuck Norris API (executor: k6 / tipo: carga)

```gherkin
Feature: Testes de carga na Chuck Norris API

  Background:
    And a opção "insecureSkipTLSVerify" deve ser definida como "true" no script k6
    And nenhuma autenticação é necessária

  Scenario: TC-PERF-M07 — Carga: pico de acessos em /jokes/random (40 VUs / 45s)
    Given a URL base é "https://api.chucknorris.io"
    And o endpoint alvo é "GET /jokes/random"
    And a configuração de carga é:
      | parâmetro | valor |
      | vus       | 40    |
      | duration  | 45s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de carga é executado
    Then a taxa de erros deve ser inferior a 2%
    And o p95 do tempo de resposta deve ser inferior a 2500ms
    And o throughput deve ser de ao menos 10 requisições por segundo

  Scenario: TC-PERF-M08 — Performance: tempo de resposta de /jokes/categories (8 VUs / 30s)
    Given a URL base é "https://api.chucknorris.io"
    And o endpoint alvo é "GET /jokes/categories"
    And a configuração de performance é:
      | parâmetro | valor |
      | vus       | 8     |
      | duration  | 30s   |
    And a opção "insecureSkipTLSVerify" é "true"
    When o teste de performance é executado
    Then o p95 do tempo de resposta deve ser inferior a 1500ms
    And a taxa de erros deve ser inferior a 1%
    And cada resposta deve ser um array de strings
```

---

## Feature: Visual — A11Y Project (executor: playwright-visual / tipo: visual)

```gherkin
Feature: Regressão visual em páginas do A11Y Project

  Background:
    And o threshold de diferença aceitável é 2%
    And nenhuma autenticação é necessária

  Scenario: TC-VISUAL-M01 — Homepage do A11Y Project sem regressão visual
    Given o usuário acessa "https://www.a11yproject.com"
    And a página é aguardada até o elemento "main" estar visível
    And elementos dinâmicos são ocultados antes do screenshot
    When o screenshot é capturado com nome "a11y-home.png"
    Then a diferença não deve exceder 2%

  Scenario: TC-VISUAL-M02 — Checklist do A11Y Project sem regressão visual
    Given o usuário acessa "https://www.a11yproject.com/checklist/"
    And a página é aguardada até o elemento "main" estar visível
    When o screenshot é capturado com nome "a11y-checklist.png"
    Then a diferença não deve exceder 2%

  Scenario: TC-VISUAL-M03 — Página de recursos do A11Y Project sem regressão visual
    Given o usuário acessa "https://www.a11yproject.com/resources/"
    And a página é aguardada até o elemento "main" estar visível
    When o screenshot é capturado com nome "a11y-resources.png"
    Then a diferença não deve exceder 2%
```

---

## Feature: Visual — WebAIM (executor: playwright-visual / tipo: visual)

```gherkin
Feature: Regressão visual em páginas do WebAIM

  Background:
    And o threshold de diferença aceitável é 2%
    And nenhuma autenticação é necessária

  Scenario: TC-VISUAL-M04 — Homepage do WebAIM sem regressão visual
    Given o usuário acessa "https://webaim.org"
    And a página é aguardada até o elemento "main" estar visível
    When o screenshot é capturado com nome "webaim-home.png"
    Then a diferença não deve exceder 2%

  Scenario: TC-VISUAL-M05 — Artigo de contraste do WebAIM sem regressão visual
    Given o usuário acessa "https://webaim.org/articles/contrast/"
    And a página é aguardada até o conteúdo principal estar visível
    When o screenshot da área de conteúdo é capturado com nome "webaim-contrast.png"
    Then a diferença não deve exceder 2%

  Scenario: TC-VISUAL-M06 — Página de introdução do WebAIM sem regressão visual
    Given o usuário acessa "https://webaim.org/intro/"
    And a página é aguardada até o elemento "article" estar visível
    When o screenshot é capturado com nome "webaim-intro.png"
    Then a diferença não deve exceder 2%
```

---

## Feature: Visual — W3C WAI (executor: playwright-visual / tipo: visual)

```gherkin
Feature: Regressão visual em páginas W3C WAI

  Background:
    And o threshold de diferença aceitável é 2%
    And nenhuma autenticação é necessária

  Scenario: TC-VISUAL-M07 — Página WAI do W3C sem regressão visual
    Given o usuário acessa "https://www.w3.org/WAI/"
    And a página é aguardada até o elemento "main" estar visível
    When o screenshot é capturado com nome "w3c-wai-home.png"
    Then a diferença não deve exceder 2%

  Scenario: TC-VISUAL-M08 — Demo acessível W3C BAD "after" sem regressão visual
    Given o usuário acessa "https://www.w3.org/WAI/demos/bad/after/home.html"
    And a página é aguardada até o conteúdo carregar
    When o screenshot é capturado com nome "w3c-bad-after-home.png"
    Then a diferença não deve exceder 2%
```

---

## Feature: Acessibilidade — W3C WAI Demos "After" (executor: axe-core / tipo: acessibilidade)

```gherkin
Feature: Conformidade WCAG 2.1 AA nas páginas demo acessíveis do W3C BAD

  Background:
    And o nível WCAG alvo é "WCAG 2.1 AA"
    And os ambientes são páginas "after" do W3C BAD — criadas para demonstrar conformidade
    And nenhuma autenticação é necessária

  Scenario: TC-A11Y-M01 — WCAG 2.1 AA na homepage acessível W3C BAD
    Given o usuário acessa "https://www.w3.org/WAI/demos/bad/after/home.html"
    And a página aguarda o carregamento do "body"
    When a análise axe-core é executada com tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações "critical" ou "serious"
    And deploy_blocked deve ser false

  Scenario: TC-A11Y-M02 — WCAG 2.1 AA no formulário de survey acessível W3C BAD
    Given o usuário acessa "https://www.w3.org/WAI/demos/bad/after/survey.html"
    And a página aguarda o formulário estar visível
    When a análise axe-core é executada com tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações "critical" ou "serious"
    And violações "moderate" ou "minor" devem ser reportadas como avisos

  Scenario: TC-A11Y-M03 — WCAG 2.1 AA na página de notícias acessível W3C BAD
    Given o usuário acessa "https://www.w3.org/WAI/demos/bad/after/news.html"
    And a página aguarda o elemento "main" ou "body"
    When a análise axe-core é executada com tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações "critical" ou "serious"

  Scenario: TC-A11Y-M04 — WCAG 2.1 AA na página de loja acessível W3C BAD
    Given o usuário acessa "https://www.w3.org/WAI/demos/bad/after/shop.html"
    And a página aguarda o conteúdo de produtos carregar
    When a análise axe-core é executada com tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações "critical" ou "serious"
    And deploy_blocked deve ser false
```

---

## Feature: Acessibilidade — W3C WAI Tutorials (executor: axe-core / tipo: acessibilidade)

```gherkin
Feature: Conformidade WCAG 2.1 AA nas páginas de tutoriais W3C WAI

  Background:
    And o nível WCAG alvo é "WCAG 2.1 AA"
    And nenhuma autenticação é necessária

  Scenario: TC-A11Y-M05 — WCAG 2.1 AA no tutorial de estrutura de página W3C
    Given o usuário acessa "https://www.w3.org/WAI/tutorials/page-structure/"
    And a página aguarda o elemento "main"
    When a análise axe-core é executada com tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações "critical" ou "serious"

  Scenario: TC-A11Y-M06 — WCAG 2.1 AA no tutorial de formulários W3C
    Given o usuário acessa "https://www.w3.org/WAI/tutorials/forms/"
    And a página aguarda o elemento "main"
    When a análise axe-core é executada com tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações "critical" ou "serious"

  Scenario: TC-A11Y-M07 — WCAG 2.1 AA no tutorial de imagens W3C
    Given o usuário acessa "https://www.w3.org/WAI/tutorials/images/"
    And a página aguarda o elemento "main"
    When a análise axe-core é executada com tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações "critical" ou "serious"

  Scenario: TC-A11Y-M08 — WCAG 2.1 AA no tutorial de tabelas W3C
    Given o usuário acessa "https://www.w3.org/WAI/tutorials/tables/"
    And a página aguarda o elemento "main"
    When a análise axe-core é executada com tags "wcag2a, wcag2aa, wcag21aa"
    Then não deve haver violações "critical" ou "serious"
    And deploy_blocked deve ser false
```

---

## Feature: Segurança — APIs Públicas Grupo 1 (executor: zap / tipo: segurança)

```gherkin
Feature: Verificação de headers e CORS em APIs públicas — grupo 1

  Background:
    And nenhuma autenticação é necessária
    And análise não invasiva apenas

  Scenario: TC-SEC-M01 — Headers de segurança na PokéAPI
    Given a URL base é "https://pokeapi.co/api/v2"
    And os endpoints são "/pokemon/1" e "/type/1"
    When os headers HTTP são inspecionados
    Then o header "Content-Type" deve conter "application/json"
    And o header "Server" não deve expor versão
    And ausências de headers opcionais devem ser avisos, não falhas

  Scenario: TC-SEC-M02 — Headers e endpoints sensíveis no JSONPlaceholder
    Given a URL base é "https://jsonplaceholder.typicode.com"
    And os endpoints são "/posts", "/users" e "/todos"
    When os headers e endpoints são inspecionados
    Then o status dos endpoints deve ser 200
    And nenhum endpoint de administração deve estar exposto sem auth
    And headers de segurança ausentes devem gerar avisos

  Scenario: TC-SEC-M03 — Headers de segurança na Countries REST API
    Given a URL base é "https://restcountries.com/v3.1"
    And os endpoints são "/name/brazil" e "/all?fields=name"
    When os headers HTTP são inspecionados
    Then o header "Content-Type" deve conter "application/json"
    And o header "Server" não deve expor versão do software
    And headers opcionais ausentes devem ser registrados como avisos

  Scenario: TC-SEC-M04 — Headers e CORS na Dog CEO API
    Given a URL base é "https://dog.ceo/api"
    And os endpoints são "/breeds/list/all" e "/breeds/image/random"
    When os headers e CORS são inspecionados
    Then o status dos endpoints deve ser 200
    And requisições CORS arbitrárias não devem expor dados privados
    And o header "Server" não deve expor informações sensíveis
```

---

## Feature: Segurança — APIs com Autenticação (executor: zap / tipo: segurança)

```gherkin
Feature: Verificação de segurança em endpoints autenticados

  Background:
    And análise não invasiva apenas

  Scenario: TC-SEC-M05 — Headers de segurança na Chuck Norris API
    Given a URL base é "https://api.chucknorris.io"
    And os endpoints são "/jokes/random" e "/jokes/categories"
    When os headers HTTP são inspecionados
    Then o header "Content-Type" deve conter "application/json"
    And nenhum stack trace deve aparecer em respostas de erro
    And headers opcionais ausentes são avisos não bloqueantes

  Scenario: TC-SEC-M06 — Headers na Open Notify API
    Given a URL base é "http://api.open-notify.org"
    And o endpoint é "/iss-now.json"
    When os headers HTTP são inspecionados
    Then o status deve ser 200
    And o header "Content-Type" deve conter "application/json"
    And ausência de HTTPS deve ser registrada como aviso de segurança

  Scenario: TC-SEC-M07 — Proteção de endpoints autenticados no Restful-Booker
    Given a URL base é "https://restful-booker.herokuapp.com"
    And os endpoints são "/booking" (GET público) e "/booking/{id}" (PUT protegido)
    When requisições sem token são feitas aos endpoints protegidos
    Then o endpoint GET /booking deve retornar 200 (público)
    And o endpoint PUT /booking/{id} sem token deve retornar 403 ou 401
    And nenhuma informação de booking privado deve vazar sem autenticação

  Scenario: TC-SEC-M08 — Proteção por API key na NASA APOD
    Given a URL base é "https://api.nasa.gov"
    And o endpoint é "/planetary/apod"
    When requisições sem api_key e com api_key inválida são enviadas
    Then requisições sem key devem retornar 403
    And requisições com key inválida devem retornar 403
    And nenhuma imagem ou dado astronômico deve ser retornado sem autenticação válida

  Scenario: TC-SEC-M09 — CORS e headers na Advice Slip API
    Given a URL base é "https://api.adviceslip.com"
    And o endpoint é "/advice"
    When os headers e CORS são inspecionados
    Then o status deve ser 200
    And o header "Content-Type" deve conter "application/json"
    And headers de segurança ausentes devem ser registrados como avisos

  Scenario: TC-SEC-M10 — Headers e token na Open Trivia DB
    Given a URL base é "https://opentdb.com"
    And os endpoints são "/api.php?amount=1" e "/api_token.php?command=request"
    When os headers são inspecionados
    Then o status deve ser 200
    And o endpoint de token não deve expor tokens de outros usuários
    And headers de segurança ausentes devem ser avisos não bloqueantes
```

---

## Feature: Banco — Schema E-commerce (executor: db / tipo: banco)

```gherkin
Feature: Integridade do schema de e-commerce em SQLite :memory:

  Background:
    Given a connection string é "sqlite://:memory:"
    And o campo "mode" no resultado deve ser "simulated"

  Scenario: TC-DB-M01 — Criar schema e validar tabelas de e-commerce
    Given o schema contém as tabelas:
      | tabela     | colunas principais                                    |
      | categories | id, name, slug, active                                |
      | products   | id, name, category_id, price, stock, active           |
      | cart_items | id, product_id, session_id, quantity, added_at        |
    And os dados de teste incluem uma categoria "Eletrônicos" com slug "eletronicos"
    When o banco é inicializado com o schema
    Then as três tabelas devem ser criadas com sucesso
    And o registro de categoria deve ser recuperável via SELECT

  Scenario: TC-DB-M02 — Validar constraints de integridade no schema de e-commerce
    Given o schema de e-commerce foi criado via "sqlite://:memory:"
    When tentativas de violação de constraints são executadas
    Then a coluna "price" com CHECK price > 0 deve rejeitar valores negativos
    And a coluna "stock" com CHECK stock >= 0 deve rejeitar valores negativos
    And "category_id" em products deve ser FK válida para categories.id
    And inserção de product com category_id inexistente deve falhar com erro de FK
```

---

## Feature: Banco — Schema RH (executor: db / tipo: banco)

```gherkin
Feature: Integridade do schema de RH em SQLite :memory:

  Background:
    Given a connection string é "sqlite://:memory:"
    And o campo "mode" no resultado deve ser "simulated"

  Scenario: TC-DB-M03 — Criar schema de RH e validar tabelas
    Given o schema contém as tabelas:
      | tabela      | colunas principais                                        |
      | departments | id, name, cost_center, budget                             |
      | employees   | id, name, email, department_id, salary, hire_date, active |
      | salaries    | id, employee_id, amount, effective_date, end_date         |
    And os dados de teste incluem um departamento "Engenharia" com budget 500000
    When o banco é inicializado com o schema
    Then as três tabelas devem ser criadas
    And o departamento deve ser recuperável via SELECT

  Scenario: TC-DB-M04 — Validar constraints do schema de RH
    Given o schema de RH foi criado via "sqlite://:memory:"
    When tentativas de violação são executadas
    Then "salary" com CHECK salary > 0 deve rejeitar zero e negativos
    And "email" de employees deve ter restrição UNIQUE
    And "department_id" deve ser FK válida para departments.id
    And inserção de employee com department_id inexistente deve falhar
```

---

## Feature: Banco — Schema Financeiro (executor: db / tipo: banco)

```gherkin
Feature: Integridade do schema financeiro em SQLite :memory:

  Background:
    Given a connection string é "sqlite://:memory:"
    And o campo "mode" no resultado deve ser "simulated"

  Scenario: TC-DB-M05 — Criar schema financeiro e validar tabelas
    Given o schema contém as tabelas:
      | tabela       | colunas principais                                                |
      | accounts     | id, owner_name, type, balance, created_at                        |
      | transactions | id, from_account_id, to_account_id, amount, status, created_at   |
    And os dados de teste incluem uma conta "QA Account" do tipo "checking" com balance 1000
    When o banco é inicializado
    Then as tabelas devem ser criadas e o registro recuperável

  Scenario: TC-DB-M06 — Validar constraints do schema financeiro
    Given o schema financeiro foi criado via "sqlite://:memory:"
    When tentativas de violação são executadas
    Then "balance" com CHECK balance >= 0 deve rejeitar negativos
    And "amount" em transactions com CHECK amount > 0 deve rejeitar zero
    And "from_account_id" e "to_account_id" devem ser FKs válidas
    And transação com account inexistente deve falhar com erro de FK
```

---

## Feature: Banco — Schema Biblioteca (executor: db / tipo: banco)

```gherkin
Feature: Integridade do schema de biblioteca em SQLite :memory:

  Background:
    Given a connection string é "sqlite://:memory:"
    And o campo "mode" no resultado deve ser "simulated"

  Scenario: TC-DB-M07 — Criar schema de biblioteca e validar tabelas
    Given o schema contém as tabelas:
      | tabela  | colunas principais                                  |
      | authors | id, name, nationality, birth_year                   |
      | books   | id, title, author_id, isbn, published_year, copies  |
      | loans   | id, book_id, borrower_name, loan_date, return_date  |
    And os dados de teste incluem o autor "Robert C. Martin" com nationality "American"
    When o banco é inicializado
    Then as tabelas devem ser criadas e o registro recuperável

  Scenario: TC-DB-M08 — Validar constraints do schema de biblioteca
    Given o schema de biblioteca foi criado via "sqlite://:memory:"
    When tentativas de violação são executadas
    Then "isbn" de books deve ter restrição UNIQUE
    And "author_id" deve ser FK para authors.id
    And "copies" com CHECK copies >= 0 deve rejeitar negativos
    And "book_id" em loans deve ser FK para books.id
```

---

## Feature: Banco — Schema E-learning (executor: db / tipo: banco)

```gherkin
Feature: Integridade do schema de e-learning em SQLite :memory:

  Background:
    Given a connection string é "sqlite://:memory:"
    And o campo "mode" no resultado deve ser "simulated"

  Scenario: TC-DB-M09 — Criar schema de e-learning e validar tabelas
    Given o schema contém as tabelas:
      | tabela      | colunas principais                                          |
      | courses     | id, title, instructor, duration_hours, max_students         |
      | students    | id, name, email, enrolled_at                                |
      | enrollments | id, course_id, student_id, progress_percent, completed_at   |
    And os dados de teste incluem o curso "QA Avançado" com 40 horas e max_students 30
    When o banco é inicializado
    Then as tabelas devem ser criadas e o curso recuperável

  Scenario: TC-DB-M10 — Validar constraints do schema de e-learning
    Given o schema de e-learning foi criado via "sqlite://:memory:"
    When tentativas de violação são executadas
    Then "progress_percent" com CHECK entre 0 e 100 deve rejeitar 101 e valores negativos
    And "duration_hours" com CHECK > 0 deve rejeitar zero
    And "email" de students deve ter restrição UNIQUE
    And FKs de course_id e student_id em enrollments devem ser validadas
```

---

# Resumo da Suite Master

| Executor | Tipos cobertos | TCs |
|---|---|---|
| executor-api (http) | integração, autenticação por key, autenticação JWT, CRUD | 15 |
| executor-browser (magnitude) | smoke, sanity, regressão, e2e, cross-browser | 15 |
| executor-performance (k6) | performance, carga, stress, soak | 8 |
| executor-visual (playwright-visual) | visual regression, baseline | 8 |
| executor-acessibilidade (axe-core) | WCAG 2.1 AA, deploy_blocked | 8 |
| executor-seguranca (zap) | headers, CORS, auth bypass, info leakage | 10 |
| executor-banco (db) | schema, constraints, FK, UNIQUE | 10 |
| **TOTAL** | | **74** |
