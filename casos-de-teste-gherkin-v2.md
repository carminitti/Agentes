# Suite de Casos de Teste Gherkin — v2 — 102 Cenários
# Cobertura completa de todos os executores e funcionalidades do QA Squad

## Aplicações e Credenciais

| Aplicação | URL Base | Credenciais |
|---|---|---|
| **reqres.in** | `https://reqres.in/api` | `eve.holt@reqres.in` / `cityslicka` · token: `QpwL5tpe83ilfN2` |
| **Restful-Booker** | `https://restful-booker.herokuapp.com` | `admin` / `password123` |
| **DummyJSON** | `https://dummyjson.com` | `kminchelle` / `0lelplR` |
| **Sauce Demo** | `https://www.saucedemo.com` | `standard_user` / `secret_sauce` |
| **OrangeHRM** | `https://opensource-demo.orangehrmlive.com` | `Admin` / `admin123` |
| **Practice Software Testing** | `https://practicesoftwaretesting.com` | `admin@practicesoftwaretesting.com` / `welcome01` |
| **Buggy Cars** | `https://buggy.justtestit.org` | `user01` / `User0001!` |
| **JSONPlaceholder** | `https://jsonplaceholder.typicode.com` | sem autenticação |
| **The Internet** | `https://the-internet.herokuapp.com` | `admin` / `admin` (Basic Auth) |

---

## Feature: Smoke — Disponibilidade de Ambiente (executores: magnitude [TC-SMOKE-02,03,04] / http [TC-SMOKE-01,05] / tipo: smoke)

```gherkin
Feature: Smoke — sistemas respondendo antes de executar qualquer suite

  Scenario: TC-SMOKE-01 — reqres.in está respondendo
    Given a URL base é "https://reqres.in/api"
    When uma requisição GET é enviada para "/users?page=1"
    Then o status HTTP deve ser 200
    And o tempo de resposta deve ser inferior a 3000ms

  Scenario: TC-SMOKE-02 — Sauce Demo carrega a tela de login
    Given a URL "https://www.saucedemo.com" é aberta no navegador
    When a página termina de carregar
    Then o elemento com id "user-name" deve estar visível
    And o elemento com id "password" deve estar visível
    And o botão de login deve estar visível

  Scenario: TC-SMOKE-03 — OrangeHRM carrega a tela de login
    Given a URL "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login" é aberta no navegador
    When a página termina de carregar
    Then o título da página deve conter "OrangeHRM"
    And o campo de usuário deve estar visível na tela

  Scenario: TC-SMOKE-04 — Practice Software Testing responde com catálogo
    Given a URL "https://practicesoftwaretesting.com" é aberta no navegador
    When a página termina de carregar
    Then a grade de produtos deve estar visível
    And ao menos um produto deve estar listado na página

  Scenario: TC-SMOKE-05 — Restful-Booker healthcheck retorna created
    Given a URL base é "https://restful-booker.herokuapp.com"
    When uma requisição GET é enviada para "/ping"
    Then o status HTTP deve ser 201
    And o tempo de resposta deve ser inferior a 3000ms
```

---

## Feature: Sanity — Funcionalidades Críticas Após Deploy (executores: magnitude [TC-SANITY-01,02,05] / http [TC-SANITY-03,04] / tipo: sanity)

```gherkin
Feature: Sanity — validação de funcionalidades core em todos os sistemas

  Scenario: TC-SANITY-01 — Login funcional no Sauce Demo
    Given a URL "https://www.saucedemo.com" está aberta no navegador
    When o campo "user-name" é preenchido com "standard_user"
    And o campo "password" é preenchido com "secret_sauce"
    And o botão "Login" é clicado
    Then a URL atual deve conter "/inventory.html"
    And o título "Products" deve estar visível na página

  Scenario: TC-SANITY-02 — Login funcional no OrangeHRM
    Given a URL "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login" está aberta
    When o campo de username é preenchido com "Admin"
    And o campo de password é preenchido com "admin123"
    And o botão "Login" é clicado
    Then o dashboard do OrangeHRM deve estar visível
    And o menu de navegação lateral deve estar presente

  Scenario: TC-SANITY-03 — Autenticação JWT no DummyJSON retorna token válido
    Given a URL base é "https://dummyjson.com"
    When uma requisição POST é enviada para "/auth/login" com body:
      """json
      { "username": "kminchelle", "password": "0lelplR" }
      """
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "token" não vazio
    And a resposta deve conter o campo "id" com valor numérico

  Scenario: TC-SANITY-04 — Autenticação no reqres.in retorna token
    Given a URL base é "https://reqres.in/api"
    When uma requisição POST é enviada para "/login" com body:
      """json
      { "email": "eve.holt@reqres.in", "password": "cityslicka" }
      """
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "token" com valor "QpwL5tpe83ilfN2"

  Scenario: TC-SANITY-05 — Catálogo de produtos acessível no Practice Software Testing
    Given o usuário está autenticado em "https://practicesoftwaretesting.com" com "admin@practicesoftwaretesting.com" / "welcome01"
    When a página do catálogo é acessada
    Then ao menos 9 produtos devem estar listados
    And cada produto deve exibir nome, preço e botão de adicionar ao carrinho
```

---

## Feature: Integração — reqres.in — CRUD Completo (executor: http / tipo: integração)

```gherkin
Feature: Integração com reqres.in — operações CRUD e autenticação

  Background:
    Given a URL base da API é "https://reqres.in/api"
    And o Content-Type das requisições é "application/json"

  Scenario: TC-API-01 — Listar usuários da página 1 e validar estrutura
    Given o endpoint é "GET /users?page=1"
    When a requisição é enviada sem autenticação
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "page" igual a 1
    And a resposta deve conter o campo "per_page" com valor numérico
    And a resposta deve conter o array "data" com ao menos 1 item
    And cada item de "data" deve conter os campos "id", "email", "first_name", "last_name", "avatar"

  Scenario: TC-API-02 — Listar usuários da página 2 e validar paginação
    Given o endpoint é "GET /users?page=2"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "page" igual a 2
    And a resposta deve conter o campo "total_pages" com valor maior que 1
    And o array "data" deve conter ao menos 1 usuário

  Scenario: TC-API-03 — Consultar usuário por ID existente
    Given o endpoint é "GET /users/2"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o objeto "data" com campo "id" igual a 2
    And o campo "data.email" deve ser "janet.weaver@reqres.in"
    And o campo "data.first_name" deve ser "Janet"

  Scenario: TC-API-04 — Consultar usuário por ID inexistente retorna 404
    Given o endpoint é "GET /users/999"
    When a requisição é enviada
    Then o status HTTP deve ser 404
    And o corpo da resposta deve ser um objeto vazio "{}"

  Scenario: TC-API-05 — Criar novo usuário com nome e cargo
    Given o endpoint é "POST /users"
    And o body da requisição é:
      """json
      { "name": "Gabriel Carminitti", "job": "QA Engineer" }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 201
    And a resposta deve conter o campo "name" igual a "Gabriel Carminitti"
    And a resposta deve conter o campo "job" igual a "QA Engineer"
    And a resposta deve conter o campo "id" não vazio
    And a resposta deve conter o campo "createdAt" no formato ISO 8601

  Scenario: TC-API-06 — Atualizar usuário com PUT substituindo todos os campos
    Given o endpoint é "PUT /users/2"
    And o body da requisição é:
      """json
      { "name": "Janet Updated", "job": "Senior QA" }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "name" igual a "Janet Updated"
    And a resposta deve conter o campo "job" igual a "Senior QA"
    And a resposta deve conter o campo "updatedAt" no formato ISO 8601

  Scenario: TC-API-07 — Atualizar usuário com PATCH atualizando apenas o cargo
    Given o endpoint é "PATCH /users/2"
    And o body da requisição é:
      """json
      { "job": "Lead QA Analyst" }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "job" igual a "Lead QA Analyst"
    And a resposta deve conter o campo "updatedAt" no formato ISO 8601

  Scenario: TC-API-08 — Deletar usuário existente retorna 204
    Given o endpoint é "DELETE /users/2"
    When a requisição é enviada
    Then o status HTTP deve ser 204
    And o corpo da resposta deve estar vazio

  Scenario: TC-API-09 — Registrar usuário com credenciais válidas
    Given o endpoint é "POST /register"
    And o body da requisição é:
      """json
      { "email": "eve.holt@reqres.in", "password": "pistol" }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "id" com valor numérico
    And a resposta deve conter o campo "token" não vazio

  Scenario: TC-API-10 — Registrar usuário sem senha retorna erro 400
    Given o endpoint é "POST /register"
    And o body da requisição é:
      """json
      { "email": "sydney@fife" }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 400
    And a resposta deve conter o campo "error" igual a "Missing password"

  Scenario: TC-API-11 — Login com credenciais válidas retorna token
    Given o endpoint é "POST /login"
    And o body da requisição é:
      """json
      { "email": "eve.holt@reqres.in", "password": "cityslicka" }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "token" com valor "QpwL5tpe83ilfN2"

  Scenario: TC-API-12 — Login sem senha retorna erro 400
    Given o endpoint é "POST /login"
    And o body da requisição é:
      """json
      { "email": "peter@klaven" }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 400
    And a resposta deve conter o campo "error" igual a "Missing password"

  Scenario: TC-API-13 — Listar recursos desconhecidos e validar estrutura
    Given o endpoint é "GET /unknown"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And o array "data" deve conter ao menos 1 item
    And cada item deve conter os campos "id", "name", "year", "color", "pantone_value"

  Scenario: TC-API-14 — Consultar recurso desconhecido por ID existente
    Given o endpoint é "GET /unknown/2"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o objeto "data" com campo "id" igual a 2
    And o campo "data.name" deve ser "fuchsia rose"

  Scenario: TC-API-15 — Consultar recurso desconhecido por ID inexistente retorna 404
    Given o endpoint é "GET /unknown/999"
    When a requisição é enviada
    Then o status HTTP deve ser 404
    And o corpo da resposta deve ser um objeto vazio "{}"
```

---

## Feature: Integração — Restful-Booker — Reservas com Autenticação (executor: http / tipo: integração)

```gherkin
Feature: Integração com Restful-Booker — CRUD completo com token de autorização

  Background:
    Given a URL base da API é "https://restful-booker.herokuapp.com"
    And o Content-Type das requisições é "application/json"
    And o token de autenticação foi gerado via POST /auth com "admin" / "password123"

  Scenario: TC-BOOKER-01 — Gerar token de autenticação com credenciais corretas
    Given o endpoint é "POST /auth"
    And o body da requisição é:
      """json
      { "username": "admin", "password": "password123" }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "token" com tamanho maior que 5 caracteres

  Scenario: TC-BOOKER-02 — Criar reserva e validar resposta completa
    Given o endpoint é "POST /booking"
    And o body da requisição é:
      """json
      {
        "firstname": "Gabriel",
        "lastname": "Carminitti",
        "totalprice": 250,
        "depositpaid": true,
        "bookingdates": { "checkin": "2026-06-01", "checkout": "2026-06-07" },
        "additionalneeds": "Breakfast"
      }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And a resposta deve conter o campo "bookingid" com valor numérico
    And o campo "booking.firstname" deve ser "Gabriel"
    And o campo "booking.depositpaid" deve ser true

  Scenario: TC-BOOKER-03 — Listar todos os IDs de reservas
    Given o endpoint é "GET /booking"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And o corpo da resposta deve ser um array
    And cada item do array deve conter o campo "bookingid"

  Scenario: TC-BOOKER-04 — Filtrar reservas por nome do hóspede
    Given o endpoint é "GET /booking?firstname=Gabriel"
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And o corpo da resposta deve ser um array

  Scenario: TC-BOOKER-05 — Consultar reserva criada pelo ID retornado
    Given uma reserva foi criada via POST /booking e o "bookingid" foi capturado
    When uma requisição GET é enviada para "/booking/{bookingid}"
    Then o status HTTP deve ser 200
    And o campo "firstname" deve ser "Gabriel"
    And o campo "totalprice" deve ser 250

  Scenario: TC-BOOKER-06 — Atualizar reserva com PUT usando token de autorização
    Given o endpoint é "PUT /booking/{bookingid}"
    And o header "Cookie" contém "token={auth_token}"
    And o body da requisição é:
      """json
      {
        "firstname": "Gabriel",
        "lastname": "Carminitti Updated",
        "totalprice": 300,
        "depositpaid": true,
        "bookingdates": { "checkin": "2026-06-01", "checkout": "2026-06-10" },
        "additionalneeds": "Breakfast and dinner"
      }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And o campo "lastname" deve ser "Carminitti Updated"
    And o campo "totalprice" deve ser 300

  Scenario: TC-BOOKER-07 — Atualizar parcialmente reserva com PATCH e token
    Given o endpoint é "PATCH /booking/{bookingid}"
    And o header "Cookie" contém "token={auth_token}"
    And o body da requisição é:
      """json
      { "totalprice": 350 }
      """
    When a requisição é enviada
    Then o status HTTP deve ser 200
    And o campo "totalprice" deve ser 350

  Scenario: TC-BOOKER-08 — Deletar reserva com token e validar 201
    Given o endpoint é "DELETE /booking/{bookingid}"
    And o header "Cookie" contém "token={auth_token}"
    When a requisição é enviada
    Then o status HTTP deve ser 201
    And uma requisição GET subsequente para "/booking/{bookingid}" deve retornar 404
```

---

## Feature: E2E — Sauce Demo — Fluxo Completo de Compra (executor: magnitude / tipo: e2e)

```gherkin
Feature: E2E — Sauce Demo — ciclo completo de compra com diferentes perfis de usuário

  Background:
    Given a URL base é "https://www.saucedemo.com"

  Scenario: TC-E2E-01 — Login com standard_user e visualizar catálogo
    Given a página de login está aberta
    When o campo username é preenchido com "standard_user"
    And o campo password é preenchido com "secret_sauce"
    And o botão "Login" é clicado
    Then a URL deve conter "/inventory.html"
    And o título "Products" deve estar visível
    And ao menos 6 produtos devem estar listados

  Scenario: TC-E2E-02 — Adicionar produto ao carrinho e verificar contador
    Given o usuário "standard_user" está autenticado com senha "secret_sauce"
    When o botão "Add to cart" do primeiro produto é clicado
    Then o ícone do carrinho deve exibir o contador "1"
    And o botão do produto deve mudar para "Remove"

  Scenario: TC-E2E-03 — Adicionar múltiplos produtos e verificar quantidade no carrinho
    Given o usuário "standard_user" está autenticado com senha "secret_sauce"
    When o botão "Add to cart" é clicado para os 3 primeiros produtos
    Then o ícone do carrinho deve exibir o contador "3"

  Scenario: TC-E2E-04 — Navegar ao carrinho e verificar produtos adicionados
    Given o usuário "standard_user" está autenticado e adicionou 2 produtos ao carrinho
    When o ícone do carrinho é clicado
    Then a URL deve conter "/cart.html"
    And 2 itens devem estar listados no carrinho
    And cada item deve exibir nome, descrição e preço

  Scenario: TC-E2E-05 — Completar fluxo de checkout do início ao fim
    Given o usuário "standard_user" está autenticado e tem 1 produto no carrinho
    When o ícone do carrinho é clicado
    And o botão "Checkout" é clicado
    And o campo "First Name" é preenchido com "Gabriel"
    And o campo "Last Name" é preenchido com "Carminitti"
    And o campo "Zip/Postal Code" é preenchido com "13000-000"
    And o botão "Continue" é clicado
    Then a página de resumo do pedido deve estar visível
    And o subtotal deve ser calculado corretamente
    When o botão "Finish" é clicado
    Then a mensagem "Thank you for your order!" deve estar visível

  Scenario: TC-E2E-06 — Ordenar produtos por preço crescente
    Given o usuário "standard_user" está autenticado com senha "secret_sauce"
    When o dropdown de ordenação é selecionado com a opção "Price (low to high)"
    Then os produtos devem estar listados em ordem crescente de preço
    And o primeiro produto deve ter o menor preço da lista

  Scenario: TC-E2E-07 — Remover produto do carrinho via página de detalhes
    Given o usuário "standard_user" adicionou o produto "Sauce Labs Backpack" ao carrinho
    When a página de detalhes do produto "Sauce Labs Backpack" é acessada
    And o botão "Remove" é clicado na página de detalhes
    Then o contador do carrinho deve ser removido ou exibir "0"

  Scenario: TC-E2E-08 — Logout redireciona para a tela de login
    Given o usuário "standard_user" está autenticado com senha "secret_sauce"
    When o menu hamburguer é clicado
    And o item "Logout" é clicado
    Then a URL deve ser "https://www.saucedemo.com/"
    And o campo de username deve estar visível

  Scenario: TC-E2E-09 — Login com locked_out_user exibe mensagem de erro
    Given a página de login está aberta
    When o campo username é preenchido com "locked_out_user"
    And o campo password é preenchido com "secret_sauce"
    And o botão "Login" é clicado
    Then a mensagem de erro "Epic sadface: Sorry, this user has been locked out." deve estar visível
    And a URL deve permanecer em "https://www.saucedemo.com/"

  Scenario: TC-E2E-10 — Acessar página do produto e verificar detalhes
    Given o usuário "standard_user" está autenticado com senha "secret_sauce"
    When o produto "Sauce Labs Fleece Jacket" é clicado
    Then a página de detalhes deve estar visível
    And o nome "Sauce Labs Fleece Jacket" deve estar na página
    And o preço deve estar visível
    And o botão "Add to cart" deve estar disponível

  Scenario: TC-E2E-11 — Parâmetro redirect=URL_externa é ignorado após login (proteção open redirect)
    Given a URL "https://www.saucedemo.com/?redirect=https://evil.com" está aberta no navegador
    When o campo username é preenchido com "standard_user"
    And o campo password é preenchido com "secret_sauce"
    And o botão "Login" é clicado
    Then a URL atual deve conter "/inventory.html" ou outra rota interna do Sauce Demo
    And a URL atual não deve conter "evil.com"
    And o catálogo de produtos deve estar visível (sem redirecionamento externo)
```

---

## Feature: E2E — OrangeHRM — Gestão de Recursos Humanos (executor: magnitude / tipo: e2e)

```gherkin
Feature: E2E — OrangeHRM — operações de RH com perfil Admin

  Background:
    Given a URL base é "https://opensource-demo.orangehrmlive.com"
    And o usuário Admin está autenticado com senha "admin123"

  Scenario: TC-OHR-01 — Dashboard exibe todos os módulos principais
    Given o usuário está no dashboard principal
    Then os módulos "Admin", "PIM", "Leave", "Time", "Recruitment" devem estar no menu
    And o painel de métricas deve estar visível

  Scenario: TC-OHR-02 — Buscar funcionário por nome no módulo PIM
    Given o módulo "PIM" está aberto
    When o campo de busca por nome é preenchido com "Admin"
    And o botão "Search" é clicado
    Then a lista de resultados deve exibir ao menos um funcionário
    And os campos "First Name", "Last Name" e "Employee Id" devem estar visíveis

  Scenario: TC-OHR-03 — Navegar para o módulo Admin e verificar User Management
    Given o usuário está no dashboard
    When o menu "Admin" é clicado
    And o item "User Management" → "Users" é acessado
    Then a lista de usuários do sistema deve estar visível
    And ao menos o usuário "Admin" deve estar listado

  Scenario: TC-OHR-04 — Módulo Leave exibe políticas de licença disponíveis
    Given o módulo "Leave" está aberto
    When o item "Configure" → "Leave Types" é acessado
    Then a lista de tipos de licença deve estar visível
    And ao menos 5 tipos de licença devem estar listados

  Scenario: TC-OHR-05 — Módulo Recruitment exibe vagas abertas
    Given o módulo "Recruitment" está aberto
    And o item "Vacancies" é acessado
    Then a lista de vagas deve estar visível ou a mensagem "No Records Found" deve ser exibida

  Scenario: TC-OHR-06 — Perfil do usuário Admin está acessível
    Given o usuário está autenticado
    When o ícone de perfil no canto superior direito é clicado
    And "My Info" é selecionado
    Then a página de informações pessoais do Admin deve estar visível
    And o campo de "First Name" deve estar preenchido
```

---

## Feature: Regressão — Practice Software Testing — Loja Virtual (executor: magnitude / tipo: regressão)

```gherkin
Feature: Regressão — Practice Software Testing — integridade do fluxo de compra

  Background:
    Given a URL base é "https://practicesoftwaretesting.com"

  Scenario: TC-REG-01 — Catálogo principal exibe produtos sem erros de layout
    Given a página inicial está aberta
    When os produtos são carregados
    Then a grade de produtos deve exibir ao menos 9 itens
    And cada produto deve ter imagem, nome e preço visíveis
    And nenhum erro de console crítico deve estar presente

  Scenario: TC-REG-02 — Filtro por categoria "Hand Tools" retorna produtos corretos
    Given a página inicial está aberta
    When a categoria "Hand Tools" é selecionada no filtro lateral
    Then apenas produtos da categoria "Hand Tools" devem ser exibidos
    And o contador de resultados deve ser atualizado

  Scenario: TC-REG-03 — Busca por "Hammer" retorna produtos relevantes
    Given a página inicial está aberta
    When o campo de busca é preenchido com "Hammer"
    And a busca é submetida
    Then os resultados devem conter ao menos 1 produto com "Hammer" no nome

  Scenario: TC-REG-04 — Login de admin e acesso ao painel administrativo
    Given a URL "https://practicesoftwaretesting.com/#/auth/login" está aberta
    When o campo email é preenchido com "admin@practicesoftwaretesting.com"
    And o campo senha é preenchido com "welcome01"
    And o botão "Login" é clicado
    Then o dashboard administrativo deve estar visível
    And o menu de administração deve conter itens de gerenciamento

  Scenario: TC-REG-05 — Página de detalhes do produto exibe informações completas
    Given a página inicial está aberta
    When o primeiro produto listado é clicado
    Then a página de detalhes deve exibir nome, preço, descrição e imagem
    And o botão "Add to cart" deve estar presente e habilitado
```

---

## Feature: Performance — reqres.in sob Diferentes Cargas (executor: k6 / tipo: performance e carga)

```gherkin
Feature: Performance — reqres.in — validação de SLAs sob carga

  Background:
    Given a URL base da API é "https://reqres.in/api"

  Scenario: TC-PERF-01 — Performance baseline: GET /users com 5 VUs por 30s
    Given o número de usuários virtuais é 5
    And a duração do teste é 30 segundos
    When requisições GET são enviadas continuamente para "/users?page=1"
    Then o percentil p95 de tempo de resposta deve ser inferior a 2000ms
    And a taxa de erro deve ser inferior a 1%
    And o throughput mínimo deve ser 5 req/s

  Scenario: TC-PERF-02 — Carga moderada: POST /users com 20 VUs por 60s
    Given o número de usuários virtuais é 20
    And a duração do teste é 60 segundos
    When requisições POST são enviadas para "/users" com body '{"name":"LoadUser","job":"tester"}'
    Then o percentil p95 de tempo de resposta deve ser inferior a 3000ms
    And a taxa de erro deve ser inferior a 2%

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

  Scenario: TC-PERF-04 — Stress: ramp up de 1 a 100 VUs em 2 minutos
    Given o teste começa com 1 VU e cresce até 100 VUs em 2 minutos
    When requisições GET são enviadas para "/users?page=1" durante o ramp up
    Then o sistema deve continuar respondendo mesmo no pico de 100 VUs
    And a taxa de erro no pico não deve superar 10%

  Scenario: TC-PERF-05 — Soak: GET /users com 10 VUs por 3 minutos (estabilidade)
    Given o número de usuários virtuais é 10
    And a duração do teste é 3 minutos
    When requisições GET são enviadas continuamente para "/users?page=1"
    Then o p95 não deve degradar mais que 20% ao longo do teste
    And não deve haver vazamento de memória indicado por degradação progressiva

  Scenario: TC-PERF-06 — Performance: autenticação POST /login com 10 VUs por 30s
    Given o número de usuários virtuais é 10
    And a duração do teste é 30 segundos
    When requisições POST são enviadas para "/login" com '{"email":"eve.holt@reqres.in","password":"cityslicka"}'
    Then o percentil p95 de tempo de resposta deve ser inferior a 2000ms
    And todos os tokens retornados devem ser não vazios

  Scenario: TC-PERF-07 — Carga: JSONPlaceholder GET /posts com 30 VUs por 60s
    Given a URL base é "https://jsonplaceholder.typicode.com"
    And o número de usuários virtuais é 30
    And a duração do teste é 60 segundos
    When requisições GET são enviadas para "/posts"
    Then o percentil p95 de tempo de resposta deve ser inferior a 3000ms
    And a taxa de erro deve ser 0%

  Scenario: TC-PERF-08 — Stress: JSONPlaceholder ramp up até 80 VUs em 90s
    Given a URL base é "https://jsonplaceholder.typicode.com"
    Given o teste começa com 5 VUs e cresce até 80 VUs em 90 segundos
    When requisições GET são enviadas para "/posts/1" durante o ramp up
    Then o status HTTP deve ser 200 em ao menos 95% das requisições
    And nenhuma requisição deve retornar status 500
```

---

## Feature: Segurança — reqres.in e APIs Autenticadas (executor: zap / tipo: segurança)

```gherkin
Feature: Segurança — verificação de headers, CORS e endpoints sensíveis

  Background:
    Given as verificações são não-invasivas (sem SQL injection, sem fuzzing)

  Scenario: TC-SEC-01 — Headers de segurança obrigatórios no reqres.in
    Given a URL base é "https://reqres.in"
    When uma requisição GET é enviada para "/api/users"
    Then a resposta deve conter o header "X-Content-Type-Options" com valor "nosniff"
    And a resposta deve conter o header "X-Frame-Options" ou "Content-Security-Policy"
    And o header "Server" não deve expor versão do servidor

  Scenario: TC-SEC-02 — Endpoint de login no reqres.in rejeita credenciais inválidas
    Given a URL base é "https://reqres.in/api"
    When uma requisição POST é enviada para "/login" com body '{"email":"hacker@evil.com","password":"wrongpass"}'
    Then o status HTTP deve ser 400
    And a resposta deve conter o campo "error"
    And nenhum token ou dado sensível deve ser retornado

  Scenario: TC-SEC-03 — reqres.in não expõe endpoints administrativos
    Given a URL base é "https://reqres.in"
    When as seguintes URLs são acessadas via GET:
      | /admin          |
      | /api/admin      |
      | /.env           |
      | /config         |
      | /api/v1/secret  |
    Then todas as respostas devem retornar 404 ou 403
    And nenhuma deve retornar 200 com dados sensíveis

  Scenario: TC-SEC-04 — CORS configurado corretamente no reqres.in
    Given a URL base é "https://reqres.in"
    When uma requisição OPTIONS é enviada para "/api/users" com header "Origin: https://evil.com"
    Then o header "Access-Control-Allow-Origin" não deve conter "https://evil.com" ou ser curinga irrestrito com credenciais

  Scenario: TC-SEC-05 — Restful-Booker rejeita operações destrutivas sem autenticação
    Given a URL base é "https://restful-booker.herokuapp.com"
    When uma requisição DELETE é enviada para "/booking/1" sem header de autorização
    Then o status HTTP deve ser 403
    And nenhum dado deve ser removido

  Scenario: TC-SEC-06 — Restful-Booker não expõe dados de outros usuários sem autenticação
    Given a URL base é "https://restful-booker.herokuapp.com"
    When uma requisição GET é enviada para "/booking/1" sem autenticação
    Then o status HTTP deve ser 200 ou 404 (reserva pública)
    And nenhum dado de cartão de crédito ou senha deve estar presente na resposta

  Scenario: TC-SEC-07 — Headers de segurança no Sauce Demo
    Given a URL "https://www.saucedemo.com" é acessada
    When os headers de resposta HTTP são inspecionados
    Then a resposta deve conter o header "Strict-Transport-Security"
    And o protocolo HTTPS deve ser obrigatório

  Scenario: TC-SEC-08 — DummyJSON rejeita token expirado ou inválido
    Given a URL base é "https://dummyjson.com"
    When uma requisição GET é enviada para "/auth/me" com header "Authorization: Bearer token_invalido_123"
    Then o status HTTP deve ser 401
    And a resposta deve conter campo de erro indicando token inválido

  Scenario: TC-SEC-09 — JSONPlaceholder não expõe endpoints de admin
    Given a URL base é "https://jsonplaceholder.typicode.com"
    When as seguintes URLs são acessadas:
      | /.env       |
      | /admin      |
      | /config.js  |
    Then todas devem retornar 404 ou 403

  Scenario: TC-SEC-10 — JSONPlaceholder não aceita métodos não permitidos em recursos read-only
    Given a URL base é "https://jsonplaceholder.typicode.com"
    When uma requisição DELETE é enviada para "/posts/1" (recurso simulado)
    Then o status HTTP deve ser 200 (JSONPlaceholder simula deleção mas não persiste) ou 405
    And o corpo da resposta não deve conter dados de outros posts
    And o header "Content-Type" deve estar presente na resposta
```

---

## Feature: Acessibilidade — WCAG 2.1 AA em Aplicações Demo (executor: axe-core / tipo: acessibilidade)

```gherkin
Feature: Acessibilidade — conformidade WCAG 2.1 AA em aplicações de teste

  Scenario: TC-A11Y-01 — Tela de login do Sauce Demo sem violações críticas
    Given a URL "https://www.saucedemo.com" é aberta
    When a análise de acessibilidade axe-core é executada com nível WCAG 2.1 AA
    Then não deve haver violações de impacto "critical"
    And violações de impacto "serious" devem ser documentadas com seletor e descrição

  Scenario: TC-A11Y-02 — Catálogo de produtos do Sauce Demo acessível após login
    Given o usuário "standard_user" está autenticado em "https://www.saucedemo.com"
    When a análise axe-core é executada na página "/inventory.html"
    Then imagens de produto devem ter atributo "alt" não vazio
    And os botões "Add to cart" devem ter texto acessível
    And o contraste de cores deve estar dentro do mínimo WCAG AA (4.5:1)

  Scenario: TC-A11Y-03 — Formulário de checkout do Sauce Demo acessível
    Given o usuário "standard_user" está autenticado e na página de checkout "/checkout-step-one.html"
    When a análise axe-core é executada
    Then todos os campos de formulário devem ter labels associados
    And os campos obrigatórios devem indicar obrigatoriedade de forma acessível
    And a navegação por teclado deve ser funcional (foco visível)

  Scenario: TC-A11Y-04 — Homepage do OrangeHRM acessível após login
    Given o usuário "Admin" está autenticado em "https://opensource-demo.orangehrmlive.com"
    When a análise axe-core é executada no dashboard
    Then não deve haver violações de impacto "critical"
    And o menu de navegação deve ter landmarks ARIA corretos

  Scenario: TC-A11Y-05 — Formulário de login do OrangeHRM acessível
    Given a URL "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login" é aberta
    When a análise axe-core é executada
    Then o formulário de login deve ter role="form" ou estar dentro de um elemento semântico
    And os campos de entrada devem ter labels associados via "for" ou "aria-label"
    And o botão de submit deve ter texto acessível

  Scenario: TC-A11Y-06 — Practice Software Testing sem violações críticas
    Given a URL "https://practicesoftwaretesting.com" é aberta
    When a análise axe-core é executada na página inicial
    Then não deve haver violações de impacto "critical"
    And as imagens de produto devem ter texto alternativo

  Scenario: TC-A11Y-07 — Formulário de login do Practice Software Testing acessível
    Given a URL "https://practicesoftwaretesting.com/#/auth/login" é aberta
    When a análise axe-core é executada
    Then todos os campos de formulário devem ter labels associados
    And mensagens de erro devem ser anunciadas via aria-live ou role="alert"

  Scenario: TC-A11Y-08 — The Internet — página de formulários acessível
    Given a URL "https://the-internet.herokuapp.com/login" é aberta
    When a análise axe-core é executada
    Then não deve haver violações de impacto "critical"
    And o formulário deve usar elementos semânticos HTML corretos
```

---

## Feature: Regressão Visual — Estabilidade de Interface (executor: playwright-visual / tipo: visual)

```gherkin
Feature: Regressão Visual — detecção de alterações não intencionais de layout

  Scenario: TC-VIS-01 — Tela de login do Sauce Demo sem regressão visual
    Given a URL "https://www.saucedemo.com" é aberta no Chromium
    When um screenshot é capturado após a página carregar completamente
    Then o screenshot deve estar dentro do threshold de 0.2% de diferença em relação ao baseline
    And os elementos "username", "password" e botão Login devem estar nas posições esperadas

  Scenario: TC-VIS-02 — Catálogo de produtos do Sauce Demo sem regressão visual
    Given o usuário "standard_user" está autenticado em "https://www.saucedemo.com"
    When um screenshot da página "/inventory.html" é capturado
    Then o layout de 3 colunas de produtos deve estar preservado
    And o screenshot deve estar dentro do threshold de 0.2%

  Scenario: TC-VIS-03 — Homepage do Practice Software Testing sem regressão visual
    Given a URL "https://practicesoftwaretesting.com" é aberta
    When um screenshot é capturado após os produtos carregarem
    Then o layout da grade de produtos deve estar dentro do threshold de 0.2%
    And o header e footer devem estar nas posições corretas

  Scenario: TC-VIS-04 — Tela de login do OrangeHRM sem regressão visual
    Given a URL "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login" é aberta
    When um screenshot é capturado
    Then o screenshot deve estar dentro do threshold de 0.2% de diferença
    And a imagem da marca OrangeHRM deve estar visível

  Scenario: TC-VIS-05 — Dashboard do OrangeHRM após login sem regressão visual
    Given o usuário "Admin" está autenticado no OrangeHRM
    When um screenshot do dashboard é capturado
    Then o layout do menu lateral deve estar preservado
    And os widgets do dashboard devem estar dentro do threshold de 0.5%

  Scenario: TC-VIS-06 — Página de checkout step 1 do Sauce Demo sem regressão visual
    Given o usuário "standard_user" está autenticado e na página de checkout
    When um screenshot da página "/checkout-step-one.html" é capturado
    Then o formulário de informações pessoais deve estar na posição correta
    And o screenshot deve estar dentro do threshold de 0.2%

  Scenario: TC-VIS-07 — Homepage do Buggy Cars sem regressão visual
    Given a URL "https://buggy.justtestit.org" é aberta
    When um screenshot é capturado após carregar
    Then o layout dos modelos de carros deve estar preservado
    And o screenshot deve estar dentro do threshold de 0.2%

  Scenario: TC-VIS-08 — Tela de login do Buggy Cars sem regressão visual
    Given a URL "https://buggy.justtestit.org/signin" é aberta
    When um screenshot é capturado
    Then o formulário de login deve estar centralizado e dentro do threshold de 0.2%
```

---

## Feature: Cross-Browser — Compatibilidade Multi-Navegador (executor: magnitude / tipo: cross-browser)

```gherkin
Feature: Cross-Browser — funcionalidades críticas em Chromium, Firefox e WebKit

  Scenario: TC-XBROW-01 — Login do Sauce Demo funciona em Chromium, Firefox e WebKit
    Given a URL "https://www.saucedemo.com" é aberta em cada navegador: Chromium, Firefox, WebKit
    When o login é realizado com "standard_user" / "secret_sauce" em cada navegador
    Then o catálogo deve ser exibido corretamente em todos os navegadores
    And o título "Products" deve estar visível em todos

  Scenario: TC-XBROW-02 — Formulário de checkout funciona em todos os navegadores
    Given o usuário "standard_user" tem 1 item no carrinho no Sauce Demo
    When o fluxo de checkout é executado em Chromium, Firefox e WebKit
    Then a mensagem "Thank you for your order!" deve aparecer em todos os navegadores
    And nenhum erro de JavaScript deve ser registrado no console

  Scenario: TC-XBROW-03 — reqres.in responde corretamente via fetch em todos os navegadores
    Given a URL "https://reqres.in" é acessada em Chromium, Firefox e WebKit
    When uma requisição GET para "/api/users" é feita via JavaScript fetch
    Then os dados devem ser retornados com status 200 em todos os navegadores

  Scenario: TC-XBROW-04 — The Internet checkboxes funcionam em múltiplos navegadores
    Given a URL "https://the-internet.herokuapp.com/checkboxes" é aberta nos 3 navegadores
    When o estado de cada checkbox é alternado em cada navegador
    Then o estado deve persistir corretamente em Chromium, Firefox e WebKit
```

---

## Feature: Mobile Web — Responsividade em Dispositivos (executor: magnitude / tipo: mobile)

```gherkin
Feature: Mobile Web — validação de responsividade com emulação de dispositivo

  Scenario: TC-MOB-01 — Login do Sauce Demo funcional em iPhone 13 (viewport 390x844)
    Given o navegador está configurado para emular "iPhone 13"
    And a URL "https://www.saucedemo.com" é aberta
    When o login é realizado com "standard_user" / "secret_sauce"
    Then o catálogo deve ser exibido em layout de coluna única ou responsivo
    And todos os elementos devem estar visíveis sem overflow horizontal

  Scenario: TC-MOB-02 — Sauce Demo catálogo navegável em Pixel 5 (viewport 393x851)
    Given o navegador está configurado para emular "Pixel 5"
    And o usuário "standard_user" está autenticado em "https://www.saucedemo.com"
    When a lista de produtos é exibida
    Then os produtos devem ser navegáveis por scroll vertical
    And os botões "Add to cart" devem ter tamanho de toque mínimo de 44x44px

  Scenario: TC-MOB-03 — Practice Software Testing responsivo em Galaxy S21 (viewport 360x800)
    Given o navegador está configurado para emular "Galaxy S21"
    And a URL "https://practicesoftwaretesting.com" é aberta
    When a página inicial carrega
    Then o menu deve estar colapsado em hamburguer ou adaptado para mobile
    And os produtos devem estar em grade responsiva
    And o conteúdo não deve ter scroll horizontal

  Scenario: TC-MOB-04 — Formulário de checkout do Sauce Demo funcional em iPhone SE (viewport 375x667)
    Given o navegador está configurado para emular "iPhone SE"
    And o usuário "standard_user" tem 1 item no carrinho
    When o fluxo de checkout é iniciado
    Then os campos do formulário devem ser clicáveis e preenchíveis sem zoom forçado
    And o botão "Continue" deve estar visível e acessível
```

---

## Feature: Banco — Integridade de Dados com SQLite em Memória (executor: db / tipo: banco)

```gherkin
Feature: Banco — validações de integridade e constraints em esquemas relacionais

  Background:
    Given o banco de dados de teste é SQLite em memória (sem DB_CONNECTION_STRING externo)
    And o script de criação de schema é executado antes de cada cenário

  Scenario: TC-DB-01 — Tabela de usuários existe com todas as constraints de integridade
    Given o schema do banco está disponível
    And a tabela "users" foi provisionada com colunas: id (PK AUTOINCREMENT), email (UNIQUE NOT NULL), name (NOT NULL), created_at (DEFAULT CURRENT_TIMESTAMP)
    When o schema da tabela "users" é consultado via PRAGMA ou information_schema
    Then a tabela "users" deve existir no banco
    And a coluna "id" deve ser identificada como PRIMARY KEY
    And a coluna "email" deve ter as constraints UNIQUE e NOT NULL
    And a coluna "name" deve ter a constraint NOT NULL

  Scenario: TC-DB-02 — Usuário inserido pela aplicação persiste corretamente no banco
    Given a aplicação registrou o usuário com email "gabriel@venturus.org.br" e nome "Gabriel Carminitti"
    When a tabela "users" é consultada com SELECT * FROM users WHERE email = 'gabriel@venturus.org.br'
    Then o resultado deve retornar exatamente 1 registro
    And o campo "email" do registro deve ser "gabriel@venturus.org.br"
    And o campo "name" do registro deve ser "Gabriel Carminitti"
    And o campo "created_at" deve estar preenchido com um timestamp válido

  Scenario: TC-DB-03 — Constraint UNIQUE impede email duplicado
    Given a tabela "users" existe com 1 registro com email "gabriel@venturus.org.br"
    When um INSERT com o mesmo email é tentado
    Then deve ser lançado um erro de violação de constraint UNIQUE
    And SELECT COUNT(*) FROM users deve continuar retornando 1

  Scenario: TC-DB-04 — Schema de pedidos com FK para usuários funciona corretamente
    Given as tabelas "users" e "orders" foram criadas com FK entre elas
    When um pedido é inserido com um user_id válido
    Then o pedido deve ser criado com sucesso
    When um pedido é inserido com user_id inexistente (999)
    Then deve ser lançado um erro de violação de FK

  Scenario: TC-DB-05 — Rollback de transação mantém integridade dos dados
    Given a tabela "users" tem 2 registros
    When uma transação BEGIN → INSERT → ROLLBACK é executada
    Then SELECT COUNT(*) FROM users deve continuar retornando 2
    And nenhum dado da transação abortada deve persistir

  Scenario: TC-DB-06 — Schema financeiro: cálculo de saldo com triggers ou constraints
    Given as tabelas "accounts" e "transactions" foram criadas com colunas de saldo
    When transações de débito e crédito são inseridas
    Then o saldo calculado via SELECT SUM deve ser matematicamente correto
    And tentativa de saldo negativo deve ser rejeitada se constraint CHECK estiver definida

  Scenario: TC-DB-07 — Índices melhoram performance em tabelas grandes
    Given a tabela "logs" é criada e populada com 10.000 registros
    When um SELECT com WHERE na coluna indexada é executado
    Then o EXPLAIN QUERY PLAN deve indicar uso do índice
    And o tempo de execução deve ser inferior a 100ms

  Scenario: TC-DB-08 — NULL constraint valida campos obrigatórios
    Given a tabela "products" tem a coluna "price" com constraint NOT NULL
    When um INSERT sem o campo "price" é tentado
    Then deve ser lançado um erro de violação de NOT NULL
    And a tabela deve permanecer consistente
```

---

## Resumo de Cobertura

| Tipo | Executor | Quantidade |
|---|---|---|
| smoke | magnitude | 5 |
| sanity | magnitude / http | 5 |
| integração (reqres.in) | http | 15 |
| integração (Restful-Booker) | http | 8 |
| e2e (Sauce Demo) | magnitude | 11 |
| e2e (OrangeHRM) | magnitude | 6 |
| regressão (Practice) | magnitude | 5 |
| performance / carga / stress / soak | k6 | 8 |
| segurança | zap | 10 | ← TC-SEC-10 substituído por verificação de método HTTP |
| acessibilidade | axe-core | 8 |
| visual | playwright-visual | 8 |
| cross-browser | magnitude | 4 |
| mobile web | magnitude (device emulation) | 4 |
| banco | db | 8 |
| **Total** | | **105** |
