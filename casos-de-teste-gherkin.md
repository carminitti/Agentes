# Casos de Teste — Squad QA · Ambientes Reais · Formato Gherkin
> Squad v1.19.0 · Gerado em 2026-05-11
> Todas as credenciais necessárias estão embutidas nos próprios steps de cada Feature.

---

## Índice

1. [executor-api · SWAPI — API pública sem autenticação](#1-executor-api--swapi--api-pública-sem-autenticação)
2. [executor-api · NASA APOD — API Key no parâmetro de query](#2-executor-api--nasa-apod--api-key-no-parâmetro-de-query)
3. [executor-api · DummyJSON — Bearer Token gerado a partir de credenciais](#3-executor-api--dummyjson--bearer-token-gerado-a-partir-de-credenciais)
4. [executor-api · Restful-Booker — Token de auth + CRUD completo](#4-executor-api--restful-booker--token-de-auth--crud-completo)
5. [executor-browser · AutomationExercise — Smoke, E2E, Regressão, Cross-Browser](#5-executor-browser--automationexercise--smoke-e2e-regressão-cross-browser)
6. [executor-performance · SWAPI & Restful-Booker — Performance, Carga, Stress, Soak](#6-executor-performance--swapi--restful-booker--performance-carga-stress-soak)
7. [executor-visual · Books to Scrape — Regressão Visual](#7-executor-visual--books-to-scrape--regressão-visual)
8. [executor-acessibilidade · WCAG 2.1 AA](#8-executor-acessibilidade--wcag-21-aa)
9. [executor-seguranca · Headers, Auth, CORS, Endpoints Sensíveis](#9-executor-seguranca--headers-auth-cors-endpoints-sensíveis)
10. [executor-banco · SQLite em Memória (simulado)](#10-executor-banco--sqlite-em-memória-simulado)
11. [executor-banco · MySQL — db4free.net (banco real)](#11-executor-banco--mysql--db4freenet-banco-real)
12. [executor-banco · PostgreSQL — Neon.tech (banco real)](#12-executor-banco--postgresql--neontech-banco-real)

---

## 1 · executor-api · SWAPI · API pública sem autenticação

> **Executor:** `http` | **Tipo:** `integração` | **Ambiente:** `https://swapi.dev/api`
> **Autenticação:** nenhuma — API completamente pública

```gherkin
Feature: SWAPI — Star Wars API pública
  Como membro do squad QA
  Quero validar que a SWAPI retorna dados corretos e dentro do SLA
  Para garantir a integridade de APIs de integração sem autenticação

  Background:
    Given a URL base da API é "https://swapi.dev/api"
    And não há autenticação necessária

  # ── TC-API-001 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-001 — Buscar personagem por ID e validar campos obrigatórios
    When eu envio GET para "/people/1/"
    Then o status code da resposta deve ser 200
    And o campo "name" deve conter o valor "Luke Skywalker"
    And o campo "birth_year" deve conter o valor "19BBY"
    And o campo "gender" deve conter o valor "male"
    And o campo "homeworld" deve ser uma URL não vazia iniciando com "https://"
    And o campo "films" deve ser um array com pelo menos 1 item
    And o tempo de resposta deve ser inferior a 3000ms

  # ── TC-API-002 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-002 — ID inexistente deve retornar 404
    When eu envio GET para "/people/9999/"
    Then o status code da resposta deve ser 404
    And o campo "detail" deve conter o valor "Not found"

  # ── TC-API-003 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-003 — Listar filmes e validar estrutura da coleção
    When eu envio GET para "/films/"
    Then o status code da resposta deve ser 200
    And o campo "count" deve ser maior que 0
    And o campo "results" deve ser um array não vazio
    And cada item de "results" deve conter os campos "title", "episode_id", "director", "release_date" e "opening_crawl"
    And ao menos um item em "results" deve ter o campo "episode_id" igual a 4
    And o tempo de resposta deve ser inferior a 3000ms

  # ── TC-API-004 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-004 — Busca por nome via query string retorna resultado filtrado
    When eu envio GET para "/starships/?search=X-wing"
    Then o status code da resposta deve ser 200
    And o campo "count" deve ser maior que 0
    And o campo "results" deve ser um array não vazio
    And o primeiro item de "results" deve ter o campo "name" contendo "X-wing"
    And o tempo de resposta deve ser inferior a 3000ms

  # ── TC-API-005 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-005 — Busca com termo inexistente retorna coleção vazia
    When eu envio GET para "/starships/?search=TERMOINEXISTENTEXXX"
    Then o status code da resposta deve ser 200
    And o campo "count" deve ser igual a 0
    And o campo "results" deve ser um array vazio

  # ── TC-API-006 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-006 — Buscar planeta por ID e validar campos de clima e terreno
    When eu envio GET para "/planets/1/"
    Then o status code da resposta deve ser 200
    And o campo "name" deve conter o valor "Tatooine"
    And o campo "climate" deve ser uma string não vazia
    And o campo "terrain" deve ser uma string não vazia
    And o campo "population" deve ser uma string não vazia
    And o tempo de resposta deve ser inferior a 3000ms
```

---

## 2 · executor-api · NASA APOD · API Key no parâmetro de query

> **Executor:** `http` | **Tipo:** `integração` | **Ambiente:** `https://api.nasa.gov`
> **Autenticação:** parâmetro de query `api_key=DEMO_KEY`
> **Nota:** `DEMO_KEY` é uma chave pública funcional fornecida pela NASA — limite: 30 req/hora

```gherkin
Feature: NASA APOD API — Autenticação via API Key
  Como membro do squad QA
  Quero validar que a API da NASA responde corretamente quando uma API Key válida é fornecida
  Para garantir que o executor-api processa autenticação por chave de query corretamente

  Background:
    Given a URL base da API é "https://api.nasa.gov"
    And a api_key de acesso é "DEMO_KEY"

  # ── TC-API-007 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-007 — Foto Astronômica do Dia retorna dados completos com DEMO_KEY
    When eu envio GET para "/planetary/apod?api_key=DEMO_KEY"
    Then o status code da resposta deve ser 200
    And o campo "title" deve ser uma string não vazia
    And o campo "url" deve ser uma URL válida iniciando com "http"
    And o campo "date" deve estar no formato "YYYY-MM-DD"
    And o campo "media_type" deve ser "image" ou "video"
    And o campo "explanation" deve ser uma string não vazia
    And o tempo de resposta deve ser inferior a 5000ms

  # ── TC-API-008 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-008 — APOD para data específica retorna dados correspondentes
    When eu envio GET para "/planetary/apod?api_key=DEMO_KEY&date=2024-07-04"
    Then o status code da resposta deve ser 200
    And o campo "date" deve conter o valor "2024-07-04"
    And o campo "title" deve ser uma string não vazia
    And o campo "url" deve ser uma URL válida

  # ── TC-API-009 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-009 — Acesso sem API Key deve ser rejeitado com erro de autenticação
    When eu envio GET para "/planetary/apod" sem nenhuma api_key
    Then o status code da resposta deve ser 403 ou 400
    And o corpo da resposta deve conter a palavra "api_key" ou "API_KEY"

  # ── TC-API-010 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-010 — Near Earth Objects em intervalo de datas retorna estrutura correta
    When eu envio GET para "/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key=DEMO_KEY"
    Then o status code da resposta deve ser 200
    And o campo "element_count" deve ser maior que 0
    And o campo "near_earth_objects" deve ser um objeto não vazio
    And o tempo de resposta deve ser inferior a 8000ms
```

---

## 3 · executor-api · DummyJSON · Bearer Token gerado a partir de credenciais

> **Executor:** `http` | **Tipo:** `integração` | **Ambiente:** `https://dummyjson.com`
> **Autenticação:** credenciais → token gerado automaticamente via `POST /auth/login`
> **Usuário:** `kminchelle` | **Senha:** `0lelplR`

```gherkin
Feature: DummyJSON — Autenticação com Bearer Token e CRUD de Produtos
  Como membro do squad QA
  Quero validar que o executor-api consegue obter token a partir de credenciais
  e acessar rotas protegidas com o token gerado automaticamente

  Background:
    Given a URL base da API é "https://dummyjson.com"
    And as credenciais de acesso são usuário "kminchelle" e senha "0lelplR"
    And o token será gerado automaticamente via POST /auth/login com essas credenciais

  # ── TC-API-011 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-011 — Login com credenciais válidas retorna token e dados do usuário
    When eu envio POST para "/auth/login" com body:
      """
      { "username": "kminchelle", "password": "0lelplR" }
      """
    Then o status code da resposta deve ser 200
    And o campo "token" deve ser uma string não vazia
    And o campo "refreshToken" deve ser uma string não vazia
    And o campo "id" deve ser um número maior que 0
    And o campo "username" deve conter o valor "kminchelle"
    And o campo "email" deve ser uma string no formato de e-mail
    And o tempo de resposta deve ser inferior a 3000ms

  # ── TC-API-012 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-012 — Login com senha incorreta deve retornar erro de autenticação
    When eu envio POST para "/auth/login" com body:
      """
      { "username": "kminchelle", "password": "senhaerrada123" }
      """
    Then o status code da resposta deve ser 400 ou 401
    And o campo "message" deve indicar credenciais inválidas

  # ── TC-API-013 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-013 — Acessar perfil autenticado com token válido
    Given o token foi obtido via login com usuário "kminchelle" e senha "0lelplR"
    When eu envio GET para "/auth/me" com header "Authorization: Bearer <token_obtido>"
    Then o status code da resposta deve ser 200
    And o campo "username" deve conter o valor "kminchelle"
    And o campo "email" deve ser uma string no formato de e-mail

  # ── TC-API-014 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-014 — Rota protegida sem token deve retornar erro de autorização
    When eu envio GET para "/auth/me" sem header Authorization
    Then o status code da resposta deve ser 401

  # ── TC-API-015 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-015 — Criar produto com token válido (Setup → Teste → Teardown)
    Given o token foi obtido via login com usuário "kminchelle" e senha "0lelplR"

    # Setup
    When eu envio POST para "/products/add" com Authorization Bearer e body:
      """
      {
        "title": "Produto QA Squad - TC015",
        "price": 99.99,
        "description": "Produto criado pelo squad de testes automatizados",
        "category": "electronics",
        "thumbnail": "https://placehold.co/300x300"
      }
      """
    Then o status code da resposta deve ser 201 ou 200
    And o campo "id" deve ser um número maior que 0
    And o campo "title" deve conter "Produto QA Squad - TC015"
    And o campo "price" deve ser igual a 99.99

    # Teardown implícito: DummyJSON não persiste dados reais entre requests

  # ── TC-API-016 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-016 — Atualização parcial de produto via PATCH com token válido
    Given o token foi obtido via login com usuário "kminchelle" e senha "0lelplR"
    When eu envio PATCH para "/products/1" com Authorization Bearer e body:
      """
      { "price": 149.99 }
      """
    Then o status code da resposta deve ser 200
    And o campo "price" deve ser igual a 149.99
    And o campo "id" deve ser igual a 1

  # ── TC-API-017 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-017 — Listar produtos sem autenticação (endpoint público)
    When eu envio GET para "/products?limit=5"
    Then o status code da resposta deve ser 200
    And o campo "products" deve ser um array com 5 itens
    And cada item deve conter os campos "id", "title", "price" e "category"
    And o campo "total" deve ser maior que 0
```

---

## 4 · executor-api · Restful-Booker · Token de auth + CRUD completo

> **Executor:** `http` | **Tipo:** `integração` | **Ambiente:** `https://restful-booker.herokuapp.com`
> **Autenticação:** credenciais → token via `POST /auth` | Basic: `YWRtaW46cGFzc3dvcmQxMjM=`
> **Usuário:** `admin` | **Senha:** `password123`

```gherkin
Feature: Restful-Booker — Ciclo de Vida Completo de Reserva com Autenticação
  Como membro do squad QA
  Quero validar o ciclo CRUD completo da API de reservas
  usando autenticação via token e Basic Auth

  Background:
    Given a URL base da API é "https://restful-booker.herokuapp.com"
    And as credenciais de acesso são usuário "admin" e senha "password123"
    And o token de acesso pode ser obtido via POST /auth com essas credenciais
    And a autenticação Basic equivalente é "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="

  # ── TC-API-018 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-018 — Gerar token de acesso com credenciais válidas
    When eu envio POST para "/auth" com body:
      """
      { "username": "admin", "password": "password123" }
      """
    Then o status code da resposta deve ser 200
    And o campo "token" deve ser uma string não vazia

  # ── TC-API-019 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-019 — Credenciais incorretas não geram token válido
    When eu envio POST para "/auth" com body:
      """
      { "username": "admin", "password": "senhaerrada" }
      """
    Then o status code da resposta deve ser 200
    And o campo "reason" deve conter "Bad credentials"

  # ── TC-API-020 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-020 — Listar todas as reservas existentes
    When eu envio GET para "/booking"
    Then o status code da resposta deve ser 200
    And a resposta deve ser um array não vazio
    And cada item do array deve conter o campo "bookingid" com valor maior que 0

  # ── TC-API-021 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-021 — Criar nova reserva e validar dados persistidos
    # Setup: sem pré-condições — o POST cria os dados
    When eu envio POST para "/booking" com body:
      """
      {
        "firstname":    "QA",
        "lastname":     "Squad",
        "totalprice":   500,
        "depositpaid":  true,
        "bookingdates": {
          "checkin":  "2025-06-01",
          "checkout": "2025-06-07"
        },
        "additionalneeds": "Breakfast"
      }
      """
    Then o status code da resposta deve ser 200
    And o campo "bookingid" deve ser um número maior que 0
    And o campo "booking.firstname" deve conter "QA"
    And o campo "booking.lastname" deve conter "Squad"
    And o campo "booking.totalprice" deve ser igual a 500
    And o campo "booking.depositpaid" deve ser true
    And o campo "booking.bookingdates.checkin" deve conter "2025-06-01"
    And o campo "booking.additionalneeds" deve conter "Breakfast"

  # ── TC-API-022 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-022 — Ler reserva recém-criada por ID
    # Setup: reserva criada no TC-API-021 (bookingid disponível como variável)
    Given a reserva com os dados do TC-API-021 foi criada e o bookingid está disponível
    When eu envio GET para "/booking/<bookingid>"
    Then o status code da resposta deve ser 200
    And o campo "firstname" deve conter "QA"
    And o campo "lastname" deve conter "Squad"
    And o campo "totalprice" deve ser igual a 500

  # ── TC-API-023 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-023 — Atualizar reserva completa via PUT com autenticação por token
    Given a reserva com bookingid da suite está disponível
    And o token foi obtido via POST /auth com usuário "admin" e senha "password123"
    When eu envio PUT para "/booking/<bookingid>" com header "Cookie: token=<token_obtido>" e body:
      """
      {
        "firstname":    "QA-Atualizado",
        "lastname":     "Squad-Atualizado",
        "totalprice":   750,
        "depositpaid":  false,
        "bookingdates": {
          "checkin":  "2025-07-01",
          "checkout": "2025-07-10"
        },
        "additionalneeds": "Lunch"
      }
      """
    Then o status code da resposta deve ser 200
    And o campo "firstname" deve conter "QA-Atualizado"
    And o campo "totalprice" deve ser igual a 750
    And o campo "depositpaid" deve ser false

  # ── TC-API-024 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-024 — Atualização parcial via PATCH com Basic Auth
    Given a reserva com bookingid da suite está disponível
    When eu envio PATCH para "/booking/<bookingid>" com header "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" e body:
      """
      { "totalprice": 900 }
      """
    Then o status code da resposta deve ser 200
    And o campo "totalprice" deve ser igual a 900

  # ── TC-API-025 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-025 — Deletar reserva com token de autenticação
    Given a reserva com bookingid da suite está disponível
    And o token foi obtido via POST /auth com usuário "admin" e senha "password123"
    When eu envio DELETE para "/booking/<bookingid>" com header "Cookie: token=<token_obtido>"
    Then o status code da resposta deve ser 201
    # Teardown: a própria operação é o teardown — a reserva foi removida

  # ── TC-API-026 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-026 — Confirmar que a reserva deletada não existe mais
    Given a reserva foi deletada no TC-API-025
    When eu envio GET para "/booking/<bookingid>"
    Then o status code da resposta deve ser 404

  # ── TC-API-027 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-027 — Operação de escrita sem token deve ser rejeitada com 403
    When eu envio DELETE para "/booking/1" sem nenhum header de autenticação
    Then o status code da resposta deve ser 403

  # ── TC-API-028 ──────────────────────────────────────────────────────────────
  Scenario: TC-API-028 — Filtrar reservas por nome do hóspede
    When eu envio GET para "/booking?firstname=QA&lastname=Squad"
    Then o status code da resposta deve ser 200
    And a resposta deve ser um array
```

---

## 5 · executor-browser · AutomationExercise · Smoke, E2E, Regressão, Cross-Browser

> **Executor:** `magnitude` | **Tipos:** `smoke`, `e2e`, `regressão`, `cross-browser`
> **Ambiente:** `https://automationexercise.com`
> **Credenciais:** e-mail `qa_squad_test@venturus.org.br` | senha `QASquad@2024!`
> **Nota:** domínio reconhecido como demo — o executor pode criar a conta automaticamente se ela não existir

```gherkin
Feature: AutomationExercise — Testes de Browser e UI
  Como membro do squad QA
  Quero validar os fluxos críticos da interface web do AutomationExercise
  usando Playwright com Page Object Model

  Background:
    Given o ambiente de testes é "https://automationexercise.com"
    And as credenciais do usuário de teste são e-mail "qa_squad_test@venturus.org.br" e senha "QASquad@2024!"

  # ── TC-BROWSER-001 ──────────────────────────────────────────────────────────
  @smoke
  Scenario: TC-BROWSER-001 — Homepage carrega com todos os elementos críticos visíveis
    When o navegador acessa "https://automationexercise.com"
    Then o título da página deve conter "Automation Exercise"
    And o elemento de navegação com texto "Signup / Login" deve estar visível
    And o elemento de navegação com texto "Products" deve estar visível
    And o elemento de navegação com texto "Cart" deve estar visível
    And o logo da página deve estar visível
    And não deve haver erros JavaScript no console
    And o tempo total de carregamento da página deve ser inferior a 5000ms

  # ── TC-BROWSER-002 ──────────────────────────────────────────────────────────
  @smoke
  Scenario: TC-BROWSER-002 — Página de produtos carrega lista com itens disponíveis
    When o navegador acessa "https://automationexercise.com/products"
    Then o título da página deve conter "Products"
    And a lista de produtos deve conter pelo menos 1 item
    And cada item de produto deve ter nome, preço e botão "Add to cart" visíveis

  # ── TC-BROWSER-003 ──────────────────────────────────────────────────────────
  @e2e
  Scenario: TC-BROWSER-003 — Cadastro de novo usuário com dados completos
    Given o usuário acessa "https://automationexercise.com"
    When o usuário clica no link "Signup / Login"
    And o usuário preenche o campo "Name" com "QA Squad"
    And o usuário preenche o campo "Email Address" no formulário "New User Signup!" com "qa_squad_test@venturus.org.br"
    And o usuário clica no botão "Signup"
    Then o usuário deve ser redirecionado para o formulário de dados da conta
    When o usuário preenche o campo de título como "Mr"
    And o usuário preenche o campo "Password" com "QASquad@2024!"
    And o usuário seleciona dia "15", mês "June" e ano "1990" para data de nascimento
    And o usuário preenche o campo "First name" com "QA"
    And o usuário preenche o campo "Last name" com "Squad"
    And o usuário preenche o campo "Address" com "Rua dos Testes, 42"
    And o usuário seleciona "Brazil" no campo "Country"
    And o usuário preenche o campo "State" com "São Paulo"
    And o usuário preenche o campo "City" com "Campinas"
    And o usuário preenche o campo "Zipcode" com "13000-000"
    And o usuário preenche o campo "Mobile Number" com "19999999999"
    And o usuário clica no botão "Create Account"
    Then a mensagem "ACCOUNT CREATED!" deve estar visível
    When o usuário clica no botão "Continue"
    Then o texto "Logged in as QA Squad" deve estar visível na barra de navegação

  # ── TC-BROWSER-004 ──────────────────────────────────────────────────────────
  @e2e
  Scenario: TC-BROWSER-004 — Login com credenciais válidas e logout subsequente
    Given o usuário acessa "https://automationexercise.com"
    When o usuário clica no link "Signup / Login"
    And o usuário preenche o campo "Email Address" no formulário "Login to your account" com "qa_squad_test@venturus.org.br"
    And o usuário preenche o campo "Password" com "QASquad@2024!"
    And o usuário clica no botão "Login"
    Then o texto "Logged in as" deve estar visível na barra de navegação
    When o usuário clica no link "Logout"
    Then o usuário deve ser redirecionado para a página de login
    And o link "Signup / Login" deve estar visível na barra de navegação

  # ── TC-BROWSER-005 ──────────────────────────────────────────────────────────
  @e2e
  Scenario: TC-BROWSER-005 — Login com credenciais incorretas exibe mensagem de erro
    Given o usuário acessa "https://automationexercise.com"
    When o usuário clica no link "Signup / Login"
    And o usuário preenche o campo "Email Address" no formulário "Login to your account" com "qa_squad_test@venturus.org.br"
    And o usuário preenche o campo "Password" com "SenhaErrada999!"
    And o usuário clica no botão "Login"
    Then a mensagem "Your email or password is incorrect!" deve estar visível

  # ── TC-BROWSER-006 ──────────────────────────────────────────────────────────
  @regressao
  Scenario: TC-BROWSER-006 — Fluxo completo de compra do início ao pagamento
    Given o usuário está logado com e-mail "qa_squad_test@venturus.org.br" e senha "QASquad@2024!"
    When o usuário clica no link "Products" na barra de navegação
    And o usuário posiciona o cursor sobre o primeiro produto da lista
    And o usuário clica no botão "Add to cart" do primeiro produto
    Then o modal com texto "Added!" deve aparecer
    When o usuário clica no botão "View Cart"
    Then o carrinho deve conter pelo menos 1 produto
    And o valor total do carrinho deve ser maior que 0
    When o usuário clica no botão "Proceed To Checkout"
    Then a seção de endereço de entrega deve estar visível
    And o resumo do pedido deve estar visível com o produto adicionado
    When o usuário clica no botão "Place Order"
    And o usuário preenche o campo "Name on Card" com "QA Squad Test"
    And o usuário preenche o campo "Card Number" com "4111111111111111"
    And o usuário preenche o campo "CVC" com "123"
    And o usuário preenche o campo "Expiry Month" com "12"
    And o usuário preenche o campo "Expiry Year" com "2028"
    And o usuário clica no botão "Pay and Confirm Order"
    Then a mensagem "Order Placed!" deve estar visível
    And a mensagem "Congratulations!" deve estar visível

  # ── TC-BROWSER-007 ──────────────────────────────────────────────────────────
  @regressao
  Scenario: TC-BROWSER-007 — Busca de produto por nome retorna resultados relevantes
    Given o navegador acessa "https://automationexercise.com/products"
    When o usuário preenche o campo de busca com "dress"
    And o usuário clica no botão "Submit" da busca
    Then o título "Searched Products" deve estar visível
    And a lista de resultados deve conter pelo menos 1 produto
    And cada produto listado deve ter "dress" no nome (case-insensitive)

  # ── TC-BROWSER-008 ──────────────────────────────────────────────────────────
  @cross-browser
  Scenario Outline: TC-BROWSER-008 — Formulário de contato funciona em múltiplos navegadores
    Given o navegador "<browser>" acessa "https://automationexercise.com/contact_us"
    When o usuário preenche o campo "Name" com "QA Squad"
    And o usuário preenche o campo "Email" com "qa_squad_test@venturus.org.br"
    And o usuário preenche o campo "Subject" com "Teste Cross-Browser - <browser>"
    And o usuário preenche o campo "Message" com "Mensagem de teste automatizado cross-browser pelo squad QA"
    And o usuário clica no botão "Submit"
    Then a mensagem "Success! Your details have been submitted successfully." deve estar visível

    Examples:
      | browser  |
      | chromium |
      | firefox  |
      | webkit   |
```

---

## 6 · executor-performance · SWAPI & Restful-Booker · Performance, Carga, Stress, Soak

> **Executor:** `k6` | **Tipos:** `performance`, `carga`, `stress`, `soak`
> **Modo:** k6 nativo (fallback automático para Python threading se k6 não estiver instalado)

```gherkin
Feature: Testes de Performance — SWAPI e Restful-Booker
  Como membro do squad QA
  Quero validar que os ambientes de API suportam os SLAs definidos
  sob diferentes perfis de carga e por duração prolongada

  # ── TC-PERF-001 ──────────────────────────────────────────────────────────────
  @performance
  Scenario: TC-PERF-001 — SWAPI responde dentro do SLA com 10 usuários simultâneos por 30 segundos
    Given o ambiente de performance é "https://swapi.dev/api"
    And não há autenticação necessária
    And o perfil de carga é:
      | VUs simultâneos | 10  |
      | Duração         | 30s |
      | Tipo            | performance |
    When os 10 VUs enviam GET para "/people/1/" repetidamente durante 30 segundos
    Then a taxa de erro deve ser inferior a 1%
    And o percentil p95 do tempo de resposta deve ser inferior a 2000ms
    And o percentil p99 do tempo de resposta deve ser inferior a 4000ms
    And o throughput deve ser de pelo menos 5 requisições por segundo

  # ── TC-PERF-002 ──────────────────────────────────────────────────────────────
  @carga
  Scenario: TC-PERF-002 — Restful-Booker suporta 50 usuários simultâneos por 60 segundos
    Given o ambiente de carga é "https://restful-booker.herokuapp.com"
    And as credenciais de acesso são usuário "admin" e senha "password123"
    And o token é gerado automaticamente via POST /auth antes do início da carga
    And o perfil de carga é:
      | VUs simultâneos | 50  |
      | Duração         | 60s |
      | Tipo            | carga |
    When os 50 VUs enviam GET para "/booking" com o token obtido repetidamente durante 60 segundos
    Then a taxa de erro deve ser inferior a 5%
    And o percentil p95 do tempo de resposta deve ser inferior a 5000ms
    And o throughput deve ser de pelo menos 10 requisições por segundo

  # ── TC-PERF-003 ──────────────────────────────────────────────────────────────
  @stress
  Scenario: TC-PERF-003 — SWAPI mantém operação sob rampa crescente de até 100 VUs
    Given o ambiente de stress é "https://swapi.dev/api"
    And não há autenticação necessária
    And o perfil de rampa é:
      | Etapa | VUs alvo | Duração |
      | 1     | 10       | 30s     |
      | 2     | 50       | 30s     |
      | 3     | 100      | 30s     |
      | 4     | 0        | 10s     |
    When os VUs são incrementados progressivamente conforme a rampa enviando GET para "/films/"
    Then nenhuma etapa deve produzir taxa de erro superior a 10%
    And o serviço não deve retornar status 5xx em nenhuma etapa
    And o p95 durante o pico de 100 VUs deve ser inferior a 8000ms

  # ── TC-PERF-004 ──────────────────────────────────────────────────────────────
  @soak
  Scenario: TC-PERF-004 — SWAPI mantém desempenho estável com 20 VUs durante 10 minutos contínuos
    Given o ambiente de soak é "https://swapi.dev/api"
    And não há autenticação necessária
    And o perfil de soak é:
      | VUs simultâneos | 20  |
      | Duração         | 10m |
      | Tipo            | soak |
    When os 20 VUs alternam entre GET /people/, GET /films/ e GET /starships/ durante 10 minutos
    Then a taxa de erro deve ser inferior a 2% durante todo o período
    And o percentil p95 apurado no último minuto não deve ser 50% superior ao p95 do primeiro minuto
    And o serviço não deve retornar status 5xx em nenhum momento
```

---

## 7 · executor-visual · Books to Scrape · Regressão Visual

> **Executor:** `playwright-visual` | **Tipo:** `visual`
> **Ambiente:** `https://books.toscrape.com`
> **Autenticação:** nenhuma — site público
> **Threshold:** 2% de diferença de pixels aceita
> **Nota:** primeira execução captura o baseline; execuções seguintes comparam com ele

```gherkin
Feature: Books to Scrape — Regressão Visual de Páginas Estáticas
  Como membro do squad QA
  Quero detectar alterações visuais não intencionais nas páginas do Books to Scrape
  usando comparação de screenshots com baseline

  Background:
    Given o ambiente de testes visuais é "https://books.toscrape.com"
    And não há autenticação necessária
    And o threshold de diferença aceitável é 2% de pixels

  # ── TC-VISUAL-001 ──────────────────────────────────────────────────────────
  @visual
  Scenario: TC-VISUAL-001 — Capturar ou comparar screenshot da homepage completa
    When o navegador acessa "https://books.toscrape.com"
    And aguarda o estado de carregamento "domcontentloaded"
    And elementos dinâmicos (contadores de visitas, banners rotativos) são ocultados se presentes
    And o executor captura o screenshot da página inteira
    Then se o baseline "homepage-completa.png" não existir:
         o arquivo de baseline é criado e o usuário recebe aviso para validação visual obrigatória
    And se o baseline "homepage-completa.png" já existir:
         a diferença entre o screenshot atual e o baseline deve ser inferior a 2%

  # ── TC-VISUAL-002 ──────────────────────────────────────────────────────────
  @visual
  Scenario: TC-VISUAL-002 — Comparar screenshot da seção de categorias com baseline
    When o navegador acessa "https://books.toscrape.com"
    And aguarda o estado de carregamento "domcontentloaded"
    And o executor captura o screenshot do elemento correspondente ao menu lateral de categorias
    Then se o baseline "sidebar-categorias.png" não existir:
         o arquivo de baseline é criado com aviso de validação visual obrigatória
    And se o baseline "sidebar-categorias.png" já existir:
         a diferença deve ser inferior a 2%

  # ── TC-VISUAL-003 ──────────────────────────────────────────────────────────
  @visual
  Scenario: TC-VISUAL-003 — Capturar ou comparar screenshot da página de categoria Mystery
    When o navegador acessa "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    And aguarda o estado de carregamento "domcontentloaded"
    And o executor captura o screenshot da página inteira
    Then se o baseline "categoria-mystery.png" não existir:
         o arquivo de baseline é criado com aviso de validação visual obrigatória
    And se o baseline "categoria-mystery.png" já existir:
         a diferença deve ser inferior a 2%

  # ── TC-VISUAL-004 ──────────────────────────────────────────────────────────
  @visual
  Scenario Outline: TC-VISUAL-004 — Layout responsivo da homepage em múltiplas resoluções
    Given o viewport do navegador está configurado como <largura>x<altura> pixels
    When o navegador acessa "https://books.toscrape.com"
    And aguarda o estado de carregamento "domcontentloaded"
    And o executor captura o screenshot da página inteira
    Then se o baseline "homepage-<largura>x<altura>.png" não existir:
         o arquivo de baseline é criado com aviso de validação visual obrigatória
    And se o baseline "homepage-<largura>x<altura>.png" já existir:
         a diferença deve ser inferior a 2%

    Examples:
      | largura | altura |
      | 1920    | 1080   |
      | 1280    | 720    |
      | 768     | 1024   |
      | 375     | 812    |
```

---

## 8 · executor-acessibilidade · WCAG 2.1 AA

> **Executor:** `axe-core` | **Tipo:** `acessibilidade` | **Nível:** WCAG 2.1 AA
> **Regra de bloqueio:** `critical` ou `serious` → `failed`; `moderate` ou `minor` → `warning`

```gherkin
Feature: Acessibilidade WCAG 2.1 AA — Books to Scrape e The Internet
  Como membro do squad QA
  Quero verificar a conformidade WCAG 2.1 AA das páginas testadas
  para garantir que o conteúdo seja acessível a todos os usuários

  # ──────────────────────────────────────────────────────────────────────────────
  # BOOKS TO SCRAPE (site sem autenticação)
  # ──────────────────────────────────────────────────────────────────────────────

  Background:
    Given o nível de conformidade WCAG alvo é "wcag2aa" (WCAG 2.1 AA)
    And violações de impacto "critical" ou "serious" reprovam o teste
    And violações de impacto "moderate" ou "minor" geram aviso sem reprovar

  # ── TC-A11Y-001 ──────────────────────────────────────────────────────────────
  @acessibilidade
  Scenario: TC-A11Y-001 — Homepage do Books to Scrape não possui violações críticas de acessibilidade
    When o navegador acessa "https://books.toscrape.com"
    And aguarda o estado de carregamento "domcontentloaded"
    And o axe-core analisa a página inteira com regras "wcag2a, wcag2aa, wcag21aa"
    Then não devem existir violações de impacto "critical"
    And não devem existir violações de impacto "serious"
    And violações de impacto "moderate" ou "minor" são reportadas como aviso sem bloquear o deploy
    And o relatório deve listar cada violação com: rule_id, impact, affected_elements e sugestão de correção

  # ── TC-A11Y-002 ──────────────────────────────────────────────────────────────
  @acessibilidade
  Scenario: TC-A11Y-002 — Página de categoria do Books to Scrape é acessível
    When o navegador acessa "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    And aguarda o estado de carregamento "domcontentloaded"
    And o axe-core analisa a página inteira com regras "wcag2a, wcag2aa, wcag21aa"
    Then não devem existir violações de impacto "critical"
    And não devem existir violações de impacto "serious"
    And todas as imagens de livros devem ter atributo "alt" não vazio
    And todos os links devem ter texto acessível

  # ──────────────────────────────────────────────────────────────────────────────
  # THE INTERNET HEROKUAPP (site sem autenticação nas páginas testadas)
  # ──────────────────────────────────────────────────────────────────────────────

  # ── TC-A11Y-003 ──────────────────────────────────────────────────────────────
  @acessibilidade
  Scenario: TC-A11Y-003 — Formulário de login do The Internet respeita WCAG 2.1 AA
    Given o ambiente de testes é "https://the-internet.herokuapp.com"
    When o navegador acessa "https://the-internet.herokuapp.com/login"
    And aguarda o estado de carregamento "domcontentloaded"
    And o axe-core analisa a página inteira com regras "wcag2a, wcag2aa, wcag21aa"
    Then não devem existir violações de impacto "critical"
    And não devem existir violações de impacto "serious"
    And o campo de usuário deve ter um label associado acessível
    And o campo de senha deve ter um label associado acessível
    And o botão de login deve ter texto acessível não vazio

  # ── TC-A11Y-004 ──────────────────────────────────────────────────────────────
  @acessibilidade
  Scenario: TC-A11Y-004 — Mensagem de erro após login inválido é anunciada de forma acessível
    Given o ambiente de testes é "https://the-internet.herokuapp.com"
    When o navegador acessa "https://the-internet.herokuapp.com/login"
    And o usuário preenche o campo "Username" com "wronguser"
    And o usuário preenche o campo "Password" com "wrongpassword"
    And o usuário clica no botão "Login"
    And aguarda a mensagem de erro aparecer
    And o axe-core analisa a página após o erro com regras "wcag2a, wcag2aa, wcag21aa"
    Then não devem existir violações de impacto "critical"
    And a mensagem de erro deve estar dentro de um elemento com role "alert" ou atributo aria-live
    And o foco do teclado deve permanecer gerenciável após o erro

  # ──────────────────────────────────────────────────────────────────────────────
  # AUTOMATIONEXERCISE (domínio de demonstração — falhas conhecidas permitidas)
  # ──────────────────────────────────────────────────────────────────────────────

  # ── TC-A11Y-005 ──────────────────────────────────────────────────────────────
  @acessibilidade
  Scenario: TC-A11Y-005 — Homepage do AutomationExercise não possui novas violações críticas
    Given o ambiente de testes é "https://automationexercise.com"
    And o domínio é reconhecido como ambiente de demonstração
    And violações anotadas como "known_demo_failure" ou "aceito pelo time" NÃO bloqueiam o deploy
    When o navegador acessa "https://automationexercise.com"
    And aguarda o estado de carregamento "domcontentloaded"
    And o axe-core analisa a página inteira com regras "wcag2a, wcag2aa, wcag21aa"
    Then todas as novas violações de impacto "critical" ou "serious" devem ser reportadas como falha
    And violações marcadas como "known_demo_failure" na anotação do step devem ter "known_environment_failure: true"
    And o campo "deploy_blocked" deve ser "false" somente se todas as violações "critical"/"serious" forem conhecidas do ambiente
    And imagens de produtos sem atributo "alt" devem ser reportadas (known_demo_failure neste ambiente de demonstração)
```

---

## 9 · executor-seguranca · Headers, Auth, CORS, Endpoints Sensíveis

> **Executor:** `zap` | **Tipo:** `segurança` | **Tecnologia:** Python requests (verificações não invasivas)
> **Escopo:** sem SQL injection, XSS, fuzzing ou força bruta

```gherkin
Feature: Segurança Não Invasiva — SWAPI e Restful-Booker
  Como membro do squad QA
  Quero verificar configurações básicas de segurança nos ambientes testados
  sem realizar nenhuma técnica invasiva ou exploração de vulnerabilidades

  # ──────────────────────────────────────────────────────────────────────────────
  # SWAPI — classificado como "public_test_api" pelo executor
  # Headers/CORS ausentes geram "warning", não "failed"
  # ──────────────────────────────────────────────────────────────────────────────

  # ── TC-SEC-001 ──────────────────────────────────────────────────────────────
  @seguranca
  Scenario: TC-SEC-001 — Verificar headers de segurança na SWAPI (API pública de teste)
    Given o ambiente de segurança é "https://swapi.dev"
    And o domínio "swapi.dev" é classificado automaticamente como "public_test_api"
    And para APIs públicas de teste: ausência de headers gera "warning" e não "failed"
    When o executor envia GET para "https://swapi.dev/api/"
    Then o executor verifica a presença dos headers de segurança:
      | Header                    | Comportamento se ausente |
      | Strict-Transport-Security | warning (API pública)    |
      | X-Content-Type-Options    | warning (API pública)    |
      | X-Frame-Options           | warning (API pública)    |
      | Content-Security-Policy   | warning (API pública)    |
    And o header "Server" não deve revelar versão detalhada do servidor (ex: "Apache/2.4.62")
    And o header "X-Powered-By" não deve estar presente com informação de tecnologia

  # ── TC-SEC-002 ──────────────────────────────────────────────────────────────
  @seguranca
  Scenario: TC-SEC-002 — Endpoints sensíveis da SWAPI não expõem conteúdo interno
    Given o ambiente de segurança é "https://swapi.dev"
    When o executor envia GET para cada um dos endpoints da lista:
      | Endpoint    |
      | /admin      |
      | /.env       |
      | /.git       |
      | /debug      |
      | /config     |
      | /swagger    |
      | /api-docs   |
    Then cada endpoint deve retornar status 404 ou 403
    And nenhum endpoint deve retornar status 200 com conteúdo interno sensível

  # ── TC-SEC-003 ──────────────────────────────────────────────────────────────
  @seguranca
  Scenario: TC-SEC-003 — CORS da SWAPI com origem não autorizada (API pública — warning esperado)
    Given o ambiente de segurança é "https://swapi.dev"
    And o domínio é classificado como "public_test_api" — CORS aberto gera "warning" não "failed"
    When o executor envia GET para "https://swapi.dev/api/people/" com header:
      | Origin | https://malicious-site-teste.com |
    Then o executor analisa o header "Access-Control-Allow-Origin" na resposta
    And o executor envia OPTIONS para "https://swapi.dev/api/people/" com headers:
      | Origin                         | https://malicious-site-teste.com |
      | Access-Control-Request-Method  | DELETE                           |
    Then o executor analisa o header "Access-Control-Allow-Origin" na resposta OPTIONS
    And se o CORS aceitar a origem maliciosa: registrar como "warning" com nota "API pública de teste — comportamento esperado"
    And se o CORS rejeitar a origem maliciosa: registrar como "passed"

  # ──────────────────────────────────────────────────────────────────────────────
  # RESTFUL-BOOKER — classificado como "production" pelo executor (não está na lista pública)
  # Headers/Auth ausentes geram "failed"
  # ──────────────────────────────────────────────────────────────────────────────

  # ── TC-SEC-004 ──────────────────────────────────────────────────────────────
  @seguranca
  Scenario: TC-SEC-004 — Endpoint protegido do Restful-Booker retorna 403 sem autenticação
    Given o ambiente de segurança é "https://restful-booker.herokuapp.com"
    And o domínio é classificado como "production" (não está na lista de APIs públicas)
    When o executor envia DELETE para "https://restful-booker.herokuapp.com/booking/1" sem header Authorization
    Then o status code da resposta deve ser 403
    And o corpo da resposta não deve conter dados de outras reservas

  # ── TC-SEC-005 ──────────────────────────────────────────────────────────────
  @seguranca
  Scenario: TC-SEC-005 — Token inválido é rejeitado com 403
    Given o ambiente de segurança é "https://restful-booker.herokuapp.com"
    When o executor envia DELETE para "https://restful-booker.herokuapp.com/booking/1" com header:
      | Cookie | token=tokeninvalido12345xyz |
    Then o status code da resposta deve ser 403

  # ── TC-SEC-006 ──────────────────────────────────────────────────────────────
  @seguranca
  Scenario: TC-SEC-006 — Verificar headers de segurança no Restful-Booker
    Given o ambiente de segurança é "https://restful-booker.herokuapp.com"
    And o domínio é classificado como "production" — ausência de headers gera "failed"
    When o executor envia GET para "https://restful-booker.herokuapp.com/booking"
    Then o executor verifica a presença dos headers de segurança:
      | Header                    | Severidade se ausente |
      | Strict-Transport-Security | medium                |
      | X-Content-Type-Options    | medium                |
      | X-Frame-Options           | medium                |
      | Content-Security-Policy   | medium                |

  # ── TC-SEC-007 ──────────────────────────────────────────────────────────────
  @seguranca
  Scenario: TC-SEC-007 — CORS preflight do Restful-Booker não aceita origens arbitrárias
    Given o ambiente de segurança é "https://restful-booker.herokuapp.com"
    When o executor envia OPTIONS para "https://restful-booker.herokuapp.com/booking" com headers:
      | Origin                          | https://malicious-site-teste.com |
      | Access-Control-Request-Method   | DELETE                           |
      | Access-Control-Request-Headers  | Authorization                    |
    Then o header "Access-Control-Allow-Origin" não deve ser "*"
    And o header "Access-Control-Allow-Origin" não deve conter "malicious-site-teste.com"

  # ── TC-SEC-008 ──────────────────────────────────────────────────────────────
  @seguranca
  Scenario: TC-SEC-008 — Endpoints sensíveis do Restful-Booker não estão acessíveis publicamente
    Given o ambiente de segurança é "https://restful-booker.herokuapp.com"
    When o executor envia GET para cada endpoint da lista:
      | Endpoint     |
      | /admin       |
      | /.env        |
      | /debug       |
      | /actuator    |
      | /metrics     |
      | /swagger     |
    Then cada endpoint deve retornar status 401, 403 ou 404
    And nenhum endpoint deve retornar status 200 com conteúdo interno

  # ── TC-SEC-009 ──────────────────────────────────────────────────────────────
  @seguranca
  Scenario: TC-SEC-009 — Resposta de GET público não contém campos sensíveis
    Given o ambiente de segurança é "https://restful-booker.herokuapp.com"
    When o executor envia GET para "https://restful-booker.herokuapp.com/booking/1"
    Then o status code deve ser 200 ou 404
    And o corpo da resposta não deve conter os campos "password", "cpf", "ssn", "credit_card" ou "secret"
```

---

## 10 · executor-banco · SQLite em Memória (simulado)

> **Executor:** `db` | **Tipo:** `banco` | **Modo:** simulado (SQLite `:memory:`)
> **Connection String:** `:memory:`
> **Nota:** o executor cria o schema automaticamente a partir dos steps e popula com dados compatíveis

```gherkin
Feature: Banco de Dados — SQLite em Memória (Modo Simulado)
  Como membro do squad QA
  Quero validar queries de integridade de dados em um banco SQLite em memória
  para garantir que o executor-banco funciona corretamente no modo simulado

  Background:
    Given a string de conexão do banco é ":memory:" (SQLite em memória)
    And o executor operará no modo simulado
    And o executor deve criar as tabelas abaixo com dados compatíveis com os cenários:
      """
      CREATE TABLE usuarios (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        nome     TEXT    NOT NULL,
        email    TEXT    UNIQUE NOT NULL,
        status   TEXT    DEFAULT 'ativo',
        criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
      );
      CREATE TABLE pedidos (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        referencia TEXT    UNIQUE NOT NULL,
        usuario_id INTEGER REFERENCES usuarios(id),
        status     TEXT    DEFAULT 'processando',
        valor      REAL    NOT NULL
      );
      """

  # ── TC-DB-001 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-001 — Tabela de usuários deve ser criada com schema correto
    When o executor executa:
      """sql
      PRAGMA table_info(usuarios);
      """
    Then o resultado deve conter as colunas: id, nome, email, status, criado_em
    And a coluna "id" deve ser do tipo INTEGER com PRIMARY KEY
    And a coluna "email" deve ter constraint UNIQUE
    And o campo "simulated" deve ser "true" no relatório de saída

  # ── TC-DB-002 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-002 — Todos os usuários pré-populados devem ter status "ativo"
    When o executor executa:
      """sql
      SELECT COUNT(*) as total,
             SUM(CASE WHEN status = 'ativo' THEN 1 ELSE 0 END) as ativos
      FROM usuarios;
      """
    Then o campo "total" deve ser maior que 0
    And o campo "ativos" deve ser igual ao campo "total"

  # ── TC-DB-003 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-003 — Não devem existir emails duplicados na tabela de usuários
    When o executor executa:
      """sql
      SELECT COUNT(*) AS total,
             COUNT(DISTINCT email) AS distintos
      FROM usuarios;
      """
    Then o campo "total" deve ser igual ao campo "distintos"

  # ── TC-DB-004 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-004 — Pedidos devem estar vinculados a usuários existentes (integridade referencial)
    When o executor executa:
      """sql
      SELECT COUNT(*) AS pedidos_orfaos
      FROM pedidos p
      WHERE NOT EXISTS (
        SELECT 1 FROM usuarios u WHERE u.id = p.usuario_id
      );
      """
    Then o campo "pedidos_orfaos" deve ser igual a 0

  # ── TC-DB-005 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-005 — Nenhum pedido deve ter valor negativo ou zero
    When o executor executa:
      """sql
      SELECT COUNT(*) AS invalidos
      FROM pedidos
      WHERE valor <= 0;
      """
    Then o campo "invalidos" deve ser igual a 0

  # ── TC-DB-006 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-006 — Referências de pedidos devem ser únicas
    When o executor executa:
      """sql
      SELECT COUNT(*) AS total,
             COUNT(DISTINCT referencia) AS distintas
      FROM pedidos;
      """
    Then o campo "total" deve ser igual ao campo "distintas"
```

---

## 11 · executor-banco · MySQL — db4free.net (banco real)

> **Executor:** `db` | **Tipo:** `banco` | **Modo:** banco real
> **Connection String:** `mysql+connector://qa_squad_2024:QASquad2024!@db4free.net:3306/qa_squad_db`
> **Usuário:** `qa_squad_2024` | **Senha:** `QASquad2024!` | **Host:** `db4free.net:3306` | **Banco:** `qa_squad_db`
> **Como criar:** acesse [db4free.net](https://db4free.net) → Register → crie banco `qa_squad_db` com usuário `qa_squad_2024`

```gherkin
Feature: Banco de Dados — MySQL Real via db4free.net
  Como membro do squad QA
  Quero validar conexão e schema no banco MySQL real do ambiente de testes
  para garantir que o executor-banco funciona com bancos remotos

  Background:
    Given a string de conexão do banco é "mysql+connector://qa_squad_2024:QASquad2024!@db4free.net:3306/qa_squad_db"
    And o tipo de banco é MySQL
    And o executor instalará automaticamente o driver "mysql-connector-python" se necessário

  # ── TC-DB-007 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-007 — Conexão com o banco MySQL real deve ser estabelecida com sucesso
    When o executor testa a conexão usando a string de conexão fornecida no Background
    Then a conexão deve ser estabelecida sem erros
    And a credencial mascarada no relatório deve ser "mysql+connector://****@db4free.net:3306/qa_squad_db"

  # ── TC-DB-008 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-008 — Versão do MySQL Server deve ser retornada corretamente
    When o executor executa:
      """sql
      SELECT VERSION() AS versao_mysql,
             DATABASE() AS banco_atual,
             USER()     AS usuario_atual;
      """
    Then o campo "versao_mysql" deve ser uma string no formato "X.Y.Z"
    And o campo "banco_atual" deve conter "qa_squad_db"
    And o campo "usuario_atual" deve conter "qa_squad_2024"

  # ── TC-DB-009 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-009 — Listar tabelas do banco qa_squad_db via information_schema
    When o executor executa:
      """sql
      SELECT TABLE_NAME    AS tabela,
             TABLE_TYPE    AS tipo,
             TABLE_ROWS    AS linhas_estimadas,
             CREATE_TIME   AS criado_em
      FROM   information_schema.TABLES
      WHERE  TABLE_SCHEMA = 'qa_squad_db'
      ORDER BY TABLE_NAME;
      """
    Then a query deve executar sem erros de conexão ou permissão
    And o resultado deve conter zero ou mais tabelas (banco pode estar vazio em criação nova)
    And cada tabela listada deve ter o campo "tabela" não nulo

  # ── TC-DB-010 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-010 — Usuário qa_squad_2024 possui permissões de leitura no banco
    When o executor executa:
      """sql
      SELECT GRANTEE, PRIVILEGE_TYPE, IS_GRANTABLE
      FROM   information_schema.USER_PRIVILEGES
      WHERE  GRANTEE LIKE '%qa_squad_2024%';
      """
    Then a query deve executar sem erros
    And o usuário deve ter ao menos o privilégio "SELECT"

  # ── TC-DB-011 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-011 — Verificar charset e collation do banco
    When o executor executa:
      """sql
      SELECT DEFAULT_CHARACTER_SET_NAME AS charset,
             DEFAULT_COLLATION_NAME     AS collation
      FROM   information_schema.SCHEMATA
      WHERE  SCHEMA_NAME = 'qa_squad_db';
      """
    Then o campo "charset" deve ser "utf8mb4" ou "utf8"
    And o campo "collation" deve ser uma string não vazia
```

---

## 12 · executor-banco · PostgreSQL — Neon.tech (banco real)

> **Executor:** `db` | **Tipo:** `banco` | **Modo:** banco real
> **Connection String template:** `postgresql://qa_squad:QASquad2024@ep-XXXXXXXX.us-east-2.aws.neon.tech/qa_test_db?sslmode=require`
> **Usuário:** `qa_squad` | **Senha:** `QASquad2024` | **Banco:** `qa_test_db` | **SSL:** obrigatório
> **Como criar:** acesse [neon.tech](https://neon.tech) → New Project → copie a connection string gerada

```gherkin
Feature: Banco de Dados — PostgreSQL Real via Neon.tech
  Como membro do squad QA
  Quero validar conexão SSL e schema no PostgreSQL do ambiente de testes
  para garantir que o executor-banco funciona com PostgreSQL em nuvem com SSL obrigatório

  Background:
    Given a string de conexão do banco é "postgresql://qa_squad:QASquad2024@ep-XXXXXXXX.us-east-2.aws.neon.tech/qa_test_db?sslmode=require"
    And o tipo de banco é PostgreSQL
    And o SSL é obrigatório para esta conexão (sslmode=require)
    And o executor instalará automaticamente o driver "psycopg2-binary" se necessário
    And no relatório, a credencial deve ser mascarada como "postgresql://****@ep-XXXXXXXX.neon.tech/qa_test_db"

  # ── TC-DB-012 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-012 — Conexão SSL com o PostgreSQL Neon deve ser estabelecida com sucesso
    When o executor testa a conexão usando a string de conexão fornecida no Background
    Then a conexão deve ser estabelecida sem erros de SSL ou autenticação
    And a credencial mascarada deve aparecer no relatório de saída

  # ── TC-DB-013 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-013 — Versão e identidade do servidor PostgreSQL devem ser retornadas
    When o executor executa:
      """sql
      SELECT version()            AS versao_pg,
             current_database()  AS banco,
             current_user        AS usuario,
             pg_is_in_recovery() AS em_recovery;
      """
    Then o campo "versao_pg" deve conter a string "PostgreSQL"
    And o campo "banco" deve conter "qa_test_db"
    And o campo "usuario" deve conter "qa_squad"
    And o campo "em_recovery" deve ser "f" (false — banco primário)

  # ── TC-DB-014 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-014 — Listar tabelas do schema público
    When o executor executa:
      """sql
      SELECT table_name   AS tabela,
             table_type   AS tipo
      FROM   information_schema.tables
      WHERE  table_schema = 'public'
      ORDER BY table_name;
      """
    Then a query deve executar sem erros de conexão ou permissão
    And o resultado deve conter zero ou mais tabelas (banco pode estar vazio em projeto novo)

  # ── TC-DB-015 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-015 — Usuário qa_squad possui permissões necessárias no banco
    When o executor executa:
      """sql
      SELECT
        has_database_privilege('qa_squad', 'qa_test_db', 'CONNECT') AS pode_conectar,
        has_schema_privilege('qa_squad', 'public', 'USAGE')         AS pode_usar_schema,
        has_schema_privilege('qa_squad', 'public', 'CREATE')        AS pode_criar_objetos;
      """
    Then o campo "pode_conectar" deve ser "t" (true)
    And o campo "pode_usar_schema" deve ser "t" (true)

  # ── TC-DB-016 ──────────────────────────────────────────────────────────────
  @banco
  Scenario: TC-DB-016 — Verificar configurações de encoding e timezone do servidor
    When o executor executa:
      """sql
      SELECT
        pg_encoding_to_char(encoding) AS encoding,
        datcollate                    AS collation,
        pg_postmaster_start_time()    AS servidor_iniciado_em
      FROM pg_database
      WHERE datname = 'qa_test_db';
      """
    Then o campo "encoding" deve conter "UTF8"
    And o campo "collation" deve ser uma string não vazia
    And o campo "servidor_iniciado_em" deve ser um timestamp válido
```

---

## Resumo dos Casos de Teste

| # | ID | Executor | Tipo | Ambiente | Autenticação embutida |
|---|---|---|---|---|---|
| 1 | TC-API-001 a 006 | `http` | integração | swapi.dev | nenhuma |
| 2 | TC-API-007 a 010 | `http` | integração | api.nasa.gov | api_key=DEMO_KEY |
| 3 | TC-API-011 a 017 | `http` | integração | dummyjson.com | kminchelle / 0lelplR |
| 4 | TC-API-018 a 028 | `http` | integração | restful-booker.herokuapp.com | admin / password123 |
| 5 | TC-BROWSER-001/002 | `magnitude` | smoke | automationexercise.com | qa_squad_test@venturus.org.br / QASquad@2024! |
| 6 | TC-BROWSER-003 a 005 | `magnitude` | e2e | automationexercise.com | idem |
| 7 | TC-BROWSER-006/007 | `magnitude` | regressão | automationexercise.com | idem |
| 8 | TC-BROWSER-008 | `playwright-multibrowser` | cross-browser | automationexercise.com | idem |
| 9 | TC-PERF-001 | `k6` | performance | swapi.dev | nenhuma |
| 10 | TC-PERF-002 | `k6` | carga | restful-booker.herokuapp.com | admin / password123 |
| 11 | TC-PERF-003 | `k6` | stress | swapi.dev | nenhuma |
| 12 | TC-PERF-004 | `k6` | soak | swapi.dev | nenhuma |
| 13 | TC-VISUAL-001 a 004 | `playwright-visual` | visual | books.toscrape.com | nenhuma |
| 14 | TC-A11Y-001/002 | `axe-core` | acessibilidade | books.toscrape.com | nenhuma |
| 15 | TC-A11Y-003/004 | `axe-core` | acessibilidade | the-internet.herokuapp.com | nenhuma |
| 16 | TC-A11Y-005 | `axe-core` | acessibilidade | automationexercise.com | nenhuma |
| 17 | TC-SEC-001 a 003 | `zap` | segurança | swapi.dev | nenhuma |
| 18 | TC-SEC-004 a 009 | `zap` | segurança | restful-booker.herokuapp.com | admin / password123 |
| 19 | TC-DB-001 a 006 | `db` | banco | SQLite :memory: | nenhuma |
| 20 | TC-DB-007 a 011 | `db` | banco | db4free.net / MySQL | qa_squad_2024 / QASquad2024! |
| 21 | TC-DB-012 a 016 | `db` | banco | neon.tech / PostgreSQL | qa_squad / QASquad2024 |

**Total: 66 cenários Gherkin · 7 executores cobertos · Todos os tipos do classifier testados**

---

*Squad de Automação de Testes QA · v1.19.0 · 2026-05-11*
