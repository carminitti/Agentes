# Casos de Teste — Squad QA · Suite 2 · Ambientes Reais
> Squad v1.19.0 · Gerado em 2026-05-11
> Um cenário por executor · Ambientes distintos da Suite 1

---

## Ambientes desta suite

| Executor | Ambiente | URL | Autenticação |
|---|---|---|---|
| `http` | Open-Meteo Weather API | `https://api.open-meteo.com` | nenhuma (pública) |
| `magnitude` | SauceDemo | `https://www.saucedemo.com` | `standard_user` / `secret_sauce` |
| `k6` | JSONPlaceholder | `https://jsonplaceholder.typicode.com` | nenhuma (pública) |
| `playwright-visual` | Wikipedia | `https://en.wikipedia.org` | nenhuma (pública) |
| `axe-core` | DemoQA | `https://demoqa.com` | nenhuma (domínio demo) |
| `zap` | httpbin.org | `https://httpbin.org` | nenhuma (serviço de teste HTTP) |
| `db` | SQLite arquivo local | `sqlite:///qa_suite2.db` | nenhuma |

---

## TC-S2-API-001 · executor-api · Open-Meteo Weather API

> **Executor:** `http` | **Tipo:** `integração`
> **Ambiente:** `https://api.open-meteo.com`
> **Autenticação:** nenhuma — API meteorológica pública e gratuita, sem chave necessária

```gherkin
Feature: Open-Meteo Weather API — Consulta de Dados Meteorológicos em Tempo Real
  Como membro do squad QA
  Quero validar que a API Open-Meteo retorna dados climáticos reais
  para um conjunto de coordenadas geográficas conhecidas

  Background:
    Given a URL base da API é "https://api.open-meteo.com"
    And não há autenticação necessária

  Scenario: TC-S2-API-001 — Consultar temperatura e vento atuais em São Paulo e validar estrutura e valores
    # Setup: sem pré-condições — API pública de leitura

    # ── Requisição principal ──────────────────────────────────────────────────
    When eu envio GET para "/v1/forecast?latitude=-23.5505&longitude=-46.6333&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&wind_speed_unit=kmh&timezone=America%2FSao_Paulo"

    # ── Validações de status e contrato ──────────────────────────────────────
    Then o status code da resposta deve ser 200
    And o campo "latitude" deve ser um número entre -24.0 e -23.0
    And o campo "longitude" deve ser um número entre -47.0 e -46.0
    And o campo "timezone" deve conter "America/Sao_Paulo"
    And o campo "current" deve existir e ser um objeto não vazio

    # ── Validações dos dados meteorológicos atuais ────────────────────────────
    And o campo "current.temperature_2m" deve ser um número entre -10.0 e 55.0
    And o campo "current.relative_humidity_2m" deve ser um número entre 0 e 100
    And o campo "current.wind_speed_10m" deve ser um número maior ou igual a 0
    And o campo "current.weather_code" deve ser um inteiro maior ou igual a 0
    And o campo "current.time" deve estar no formato "YYYY-MM-DDTHH:MM"

    # ── Validações da unidade e metadados ────────────────────────────────────
    And o campo "current_units.temperature_2m" deve conter "°C"
    And o campo "current_units.wind_speed_10m" deve conter "km/h"

    # ── Validações de performance ────────────────────────────────────────────
    And o tempo de resposta deve ser inferior a 4000ms

    # Teardown: sem dados criados — apenas leitura
```

---

## TC-S2-BROWSER-001 · executor-browser · SauceDemo

> **Executor:** `magnitude` | **Tipo:** `e2e`
> **Ambiente:** `https://www.saucedemo.com`
> **Autenticação:** usuário `standard_user` | senha `secret_sauce`
> **Nota:** domínio reconhecido como demo (`saucedemo.com` está na lista `DEMO_HOSTS` do executor)

```gherkin
Feature: SauceDemo — Fluxo E2E de Compra com Usuário Padrão
  Como membro do squad QA
  Quero validar o fluxo completo de login, seleção de produto,
  checkout e confirmação de pedido no SauceDemo

  Background:
    Given o ambiente de testes é "https://www.saucedemo.com"
    And as credenciais do usuário de teste são usuário "standard_user" e senha "secret_sauce"

  Scenario: TC-S2-BROWSER-001 — Login, adição ao carrinho e checkout completo até confirmação do pedido
    # ── Setup: login ─────────────────────────────────────────────────────────
    Given o navegador acessa "https://www.saucedemo.com"
    When o usuário preenche o campo "Username" com "standard_user"
    And o usuário preenche o campo "Password" com "secret_sauce"
    And o usuário clica no botão "Login"
    Then o usuário deve ser redirecionado para a página "/inventory.html"
    And o título "Swag Labs" deve estar visível
    And a lista de produtos deve conter pelo menos 1 item

    # ── Seleção e adição ao carrinho ─────────────────────────────────────────
    When o usuário clica no botão "Add to cart" do produto "Sauce Labs Backpack"
    Then o ícone do carrinho deve exibir o número "1"
    When o usuário clica no ícone do carrinho
    Then o usuário deve ser redirecionado para a página "/cart.html"
    And o item "Sauce Labs Backpack" deve estar visível no carrinho
    And o preço do item no carrinho deve ser "$29.99"

    # ── Início do checkout ───────────────────────────────────────────────────
    When o usuário clica no botão "Checkout"
    Then o usuário deve ser redirecionado para a página "/checkout-step-one.html"
    When o usuário preenche o campo "First Name" com "QA"
    And o usuário preenche o campo "Last Name" com "Squad"
    And o usuário preenche o campo "Zip/Postal Code" com "13000-000"
    And o usuário clica no botão "Continue"
    Then o usuário deve ser redirecionado para a página "/checkout-step-two.html"

    # ── Revisão e confirmação do pedido ──────────────────────────────────────
    And o item "Sauce Labs Backpack" deve aparecer no resumo do pedido
    And o campo "Item total" deve exibir "$29.99"
    And o campo "Tax" deve ser um valor positivo
    And o campo "Total" deve ser maior que "$29.99"
    When o usuário clica no botão "Finish"
    Then o usuário deve ser redirecionado para a página "/checkout-complete.html"
    And o texto "Thank you for your order!" deve estar visível
    And o texto "Your order has been dispatched" deve estar visível

    # ── Teardown: retornar ao inventário (sem dados persistidos) ─────────────
    When o usuário clica no botão "Back Home"
    Then o usuário deve ser redirecionado para a página "/inventory.html"
```

---

## TC-S2-PERF-001 · executor-performance · JSONPlaceholder

> **Executor:** `k6` | **Tipo:** `carga`
> **Ambiente:** `https://jsonplaceholder.typicode.com`
> **Autenticação:** nenhuma — serviço público de mock REST
> **Modo:** k6 nativo; fallback automático para Python threading se k6 não estiver instalado

```gherkin
Feature: JSONPlaceholder — Teste de Carga em Endpoint de Posts
  Como membro do squad QA
  Quero validar que o JSONPlaceholder suporta carga simultânea de 30 usuários
  por 45 segundos sem degradação relevante de latência

  Background:
    Given o ambiente de performance é "https://jsonplaceholder.typicode.com"
    And não há autenticação necessária

  Scenario: TC-S2-PERF-001 — API de posts suporta 30 VUs simultâneos durante 45 segundos dentro do SLA
    Given o perfil de carga é:
      | VUs simultâneos | 30  |
      | Duração         | 45s |
      | Tipo            | carga |
    And o endpoint alvo é GET "/posts"
    And os thresholds de SLA são:
      | Métrica          | Limite       |
      | taxa de erro     | inferior a 2% |
      | p95 de latência  | inferior a 3000ms |
      | p99 de latência  | inferior a 5000ms |
      | throughput       | pelo menos 8 req/s |
    When os 30 VUs enviam GET para "https://jsonplaceholder.typicode.com/posts" repetidamente durante 45 segundos
    Then a taxa de erro deve ser inferior a 2%
    And o percentil p95 do tempo de resposta deve ser inferior a 3000ms
    And o percentil p99 do tempo de resposta deve ser inferior a 5000ms
    And o throughput deve ser de pelo menos 8 requisições por segundo
    And nenhuma resposta deve ter status code 5xx
    And cada resposta bem-sucedida deve retornar um array com 100 posts
```

---

## TC-S2-VISUAL-001 · executor-visual · Wikipedia

> **Executor:** `playwright-visual` | **Tipo:** `visual`
> **Ambiente:** `https://en.wikipedia.org`
> **Autenticação:** nenhuma — site público
> **Threshold:** 2% de diferença de pixels aceita

```gherkin
Feature: Wikipedia — Regressão Visual da Página de Software Testing
  Como membro do squad QA
  Quero detectar alterações visuais não intencionais
  na página da Wikipedia sobre Software Testing

  Background:
    Given o ambiente de testes visuais é "https://en.wikipedia.org"
    And não há autenticação necessária
    And o threshold de diferença aceitável é 2% de pixels
    And o viewport é configurado como 1280x720 pixels

  Scenario: TC-S2-VISUAL-001 — Capturar ou comparar o cabeçalho e infobox da página Software Testing
    # ── Navegação e preparação ───────────────────────────────────────────────
    When o navegador acessa "https://en.wikipedia.org/wiki/Software_testing"
    And aguarda o estado de carregamento "domcontentloaded"
    And os seguintes elementos dinâmicos são ocultados para evitar falso positivo:
      | Seletor                         | Razão                            |
      | #siteNotice                     | banner rotativo de doação        |
      | .mw-editsection                 | links de edição de seção         |
      | #centralNotice                  | notificações centrais dinâmicas  |
    # ── Captura do elemento-alvo ─────────────────────────────────────────────
    And o executor captura o screenshot do elemento correspondente ao cabeçalho principal "#firstHeading"
    # ── Comparação ou criação de baseline ────────────────────────────────────
    Then se o baseline "wikipedia-software-testing-heading.png" não existir:
         o arquivo de baseline é criado e o usuário recebe aviso para validação visual obrigatória antes de usar como referência
    And se o baseline "wikipedia-software-testing-heading.png" já existir:
         a diferença entre o screenshot atual e o baseline deve ser inferior a 2%
    # ── Captura complementar: tabela de conteúdo ────────────────────────────
    And o executor captura o screenshot do elemento "#toc" se estiver presente na página
    Then se o baseline "wikipedia-software-testing-toc.png" não existir:
         o arquivo de baseline é criado com aviso de validação visual obrigatória
    And se o baseline "wikipedia-software-testing-toc.png" já existir:
         a diferença deve ser inferior a 2%
```

---

## TC-S2-A11Y-001 · executor-acessibilidade · DemoQA

> **Executor:** `axe-core` | **Tipo:** `acessibilidade` | **Nível:** WCAG 2.1 AA
> **Ambiente:** `https://demoqa.com`
> **Autenticação:** nenhuma — domínio de demonstração reconhecido pelo executor
> **Nota:** DemoQA está na lista `DEMO_HOSTS` — violações anotadas como `known_demo_failure` não bloqueiam deploy

```gherkin
Feature: DemoQA — Acessibilidade WCAG 2.1 AA na Página de Buttons
  Como membro do squad QA
  Quero verificar a conformidade WCAG 2.1 AA da página de interação com botões do DemoQA
  para identificar violações novas separadas das já conhecidas no ambiente de demonstração

  Background:
    Given o ambiente de testes é "https://demoqa.com"
    And o nível de conformidade WCAG alvo é "wcag2aa" (WCAG 2.1 AA)
    And o domínio "demoqa.com" é reconhecido como ambiente de demonstração
    And violações anotadas como "known_demo_failure" NÃO bloqueiam o deploy
    And o campo "deploy_blocked" deve ser "false" somente se todas as violações "critical"/"serious" forem conhecidas

  Scenario: TC-S2-A11Y-001 — Página de Buttons do DemoQA não possui novas violações críticas de acessibilidade
    # ── Navegação ─────────────────────────────────────────────────────────────
    When o navegador acessa "https://demoqa.com/buttons"
    And aguarda o estado de carregamento "domcontentloaded"
    And o executor aguarda o elemento de título da seção estar visível

    # ── Análise axe-core ──────────────────────────────────────────────────────
    And o axe-core analisa a página inteira com regras "wcag2a, wcag2aa, wcag21aa"

    # ── Verificações de resultado ─────────────────────────────────────────────
    Then não devem existir violações de impacto "critical" além das já mapeadas como "known_demo_failure" neste ambiente
    And não devem existir violações de impacto "serious" além das já mapeadas como "known_demo_failure" neste ambiente
    And os três botões da página ("Double Click Me", "Right Click Me", "Click Me") devem ter roles acessíveis de botão
    And cada botão deve ter texto acessível não vazio (via texto visível ou aria-label)
    And violações de impacto "moderate" ou "minor" são reportadas como aviso sem bloquear deploy
    And o relatório deve incluir o campo "known_environment_failure: true" para cada violação já conhecida do ambiente DemoQA
    And o campo "deploy_blocked" deve refletir corretamente se todas as violações bloqueantes são conhecidas do ambiente
```

---

## TC-S2-SEC-001 · executor-seguranca · httpbin.org

> **Executor:** `zap` | **Tipo:** `segurança`
> **Ambiente:** `https://httpbin.org`
> **Autenticação:** nenhuma — serviço público para inspeção de HTTP
> **Classificação automática:** `public_test_api` (httpbin.org está na lista `PUBLIC_TEST_API_DOMAINS` do executor)
> **Comportamento:** ausência de headers de segurança e CORS aberto geram `warning`, não `failed`

```gherkin
Feature: httpbin.org — Verificações de Segurança em Serviço Público de Teste HTTP
  Como membro do squad QA
  Quero verificar o comportamento de segurança do httpbin.org
  como validação do funcionamento correto do executor-seguranca
  em um ambiente classificado como "public_test_api"

  Background:
    Given o ambiente de segurança é "https://httpbin.org"
    And o domínio "httpbin.org" é classificado automaticamente como "public_test_api"
    And para APIs públicas de teste: ausência de headers e CORS aberto geram "warning" e NÃO "failed"
    And não há autenticação necessária

  Scenario: TC-S2-SEC-001 — Verificar headers de segurança, CORS, endpoint de auth e rota de status do httpbin.org
    # ── Verificação 1: Headers de segurança ──────────────────────────────────
    When o executor envia GET para "https://httpbin.org/get"
    Then o executor verifica a presença dos headers de segurança:
      | Header                    | Resultado se ausente (public_test_api) |
      | Strict-Transport-Security | warning — comportamento esperado       |
      | X-Content-Type-Options    | warning — comportamento esperado       |
      | X-Frame-Options           | warning — comportamento esperado       |
      | Content-Security-Policy   | warning — comportamento esperado       |
    And o status code da resposta deve ser 200
    And o campo "url" no corpo deve conter "https://httpbin.org/get"

    # ── Verificação 2: Rota de status explícito retorna código correto ────────
    When o executor envia GET para "https://httpbin.org/status/200"
    Then o status code da resposta deve ser 200
    When o executor envia GET para "https://httpbin.org/status/401"
    Then o status code da resposta deve ser 401
    When o executor envia GET para "https://httpbin.org/status/403"
    Then o status code da resposta deve ser 403

    # ── Verificação 3: Endpoint de autenticação Basic requer credenciais ─────
    When o executor envia GET para "https://httpbin.org/basic-auth/admin/secret" sem header Authorization
    Then o status code da resposta deve ser 401
    And o header "WWW-Authenticate" deve estar presente indicando autenticação Basic

    # ── Verificação 4: CORS com origem arbitrária (warning esperado) ─────────
    When o executor envia GET para "https://httpbin.org/get" com header:
      | Origin | https://malicious-site-teste.com |
    Then o executor registra o valor do header "Access-Control-Allow-Origin"
    And o executor envia OPTIONS para "https://httpbin.org/get" com headers:
      | Origin                         | https://malicious-site-teste.com |
      | Access-Control-Request-Method  | DELETE                           |
    Then se o CORS aceitar a origem: registrar como "warning" com nota "API pública de teste — comportamento esperado"
    And se o CORS rejeitar a origem: registrar como "passed"

    # ── Verificação 5: Endpoints sensíveis ───────────────────────────────────
    When o executor envia GET para cada endpoint da lista:
      | Endpoint  |
      | /.env     |
      | /admin    |
      | /.git     |
    Then cada endpoint deve retornar status 404
    And nenhum deve retornar conteúdo interno sensível
```

---

## TC-S2-DB-001 · executor-banco · SQLite arquivo local

> **Executor:** `db` | **Tipo:** `banco` | **Modo:** banco real (arquivo local)
> **Connection String:** `sqlite:///qa_suite2.db`
> **Nota:** o executor cria o arquivo `qa_suite2.db` no diretório de trabalho se não existir
> **Schema:** tabela `produtos` e tabela `categorias` (domínio diferente da Suite 1)

```gherkin
Feature: Banco de Dados — SQLite Arquivo Local com Schema de Produtos e Categorias
  Como membro do squad QA
  Quero validar integridade de dados em um banco SQLite persistido em arquivo local
  usando um schema de domínio diferente da Suite 1 (produtos e categorias)

  Background:
    Given a string de conexão do banco é "sqlite:///qa_suite2.db"
    And o tipo de banco é SQLite (arquivo local)
    And o executor deve criar o arquivo e as tabelas abaixo se ainda não existirem:
      """
      CREATE TABLE IF NOT EXISTS categorias (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        nome      TEXT    NOT NULL UNIQUE,
        ativo     INTEGER NOT NULL DEFAULT 1
      );
      CREATE TABLE IF NOT EXISTS produtos (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        sku          TEXT    NOT NULL UNIQUE,
        nome         TEXT    NOT NULL,
        preco        REAL    NOT NULL CHECK(preco > 0),
        estoque      INTEGER NOT NULL DEFAULT 0,
        categoria_id INTEGER NOT NULL REFERENCES categorias(id),
        ativo        INTEGER NOT NULL DEFAULT 1
      );
      INSERT OR IGNORE INTO categorias (nome) VALUES ('Eletrônicos'), ('Vestuário'), ('Alimentos');
      INSERT OR IGNORE INTO produtos (sku, nome, preco, estoque, categoria_id) VALUES
        ('SKU-001', 'Notebook QA Pro', 4999.90, 10, 1),
        ('SKU-002', 'Mouse Sem Fio',    149.90,  50, 1),
        ('SKU-003', 'Camiseta QA',       89.90,  30, 2),
        ('SKU-004', 'Café Especial',     45.00, 100, 3),
        ('SKU-005', 'Monitor 27"',     1899.90,   0, 1);
      """

  Scenario: TC-S2-DB-001 — Validar integridade referencial, constraints e regras de negócio do catálogo de produtos
    # ── Verificação 1: Nenhum produto tem preço zero ou negativo ─────────────
    When o executor executa:
      """sql
      SELECT COUNT(*) AS invalidos
      FROM produtos
      WHERE preco <= 0;
      """
    Then o campo "invalidos" deve ser igual a 0

    # ── Verificação 2: SKUs são únicos em todo o catálogo ────────────────────
    When o executor executa:
      """sql
      SELECT COUNT(*) AS total, COUNT(DISTINCT sku) AS distintos
      FROM produtos;
      """
    Then o campo "total" deve ser igual ao campo "distintos"

    # ── Verificação 3: Todo produto referencia uma categoria existente ────────
    When o executor executa:
      """sql
      SELECT COUNT(*) AS orfaos
      FROM produtos p
      WHERE NOT EXISTS (
        SELECT 1 FROM categorias c WHERE c.id = p.categoria_id
      );
      """
    Then o campo "orfaos" deve ser igual a 0

    # ── Verificação 4: Existem produtos com estoque zerado (esperado) ─────────
    When o executor executa:
      """sql
      SELECT sku, nome, estoque
      FROM produtos
      WHERE estoque = 0
      ORDER BY sku;
      """
    Then o resultado deve conter pelo menos 1 linha
    And cada linha deve ter os campos "sku", "nome" e "estoque"
    And o campo "estoque" de cada linha retornada deve ser igual a 0

    # ── Verificação 5: Valor médio dos produtos ativos deve ser positivo ──────
    When o executor executa:
      """sql
      SELECT ROUND(AVG(preco), 2) AS preco_medio,
             MIN(preco)           AS preco_minimo,
             MAX(preco)           AS preco_maximo,
             COUNT(*)             AS total_ativos
      FROM produtos
      WHERE ativo = 1;
      """
    Then o campo "preco_medio" deve ser maior que 0
    And o campo "preco_minimo" deve ser maior que 0
    And o campo "preco_maximo" deve ser maior ou igual ao campo "preco_minimo"
    And o campo "total_ativos" deve ser maior que 0

    # ── Verificação 6: Categoria "Eletrônicos" tem mais de 1 produto ─────────
    When o executor executa:
      """sql
      SELECT c.nome AS categoria, COUNT(p.id) AS qtd_produtos
      FROM categorias c
      LEFT JOIN produtos p ON p.categoria_id = c.id
      WHERE c.nome = 'Eletrônicos'
      GROUP BY c.nome;
      """
    Then o campo "categoria" deve conter "Eletrônicos"
    And o campo "qtd_produtos" deve ser maior que 1
```

---

## Resumo da Suite 2

| TC | Executor | Tipo | Ambiente | Autenticação |
|---|---|---|---|---|
| TC-S2-API-001 | `http` | integração | api.open-meteo.com | nenhuma |
| TC-S2-BROWSER-001 | `magnitude` | e2e | www.saucedemo.com | `standard_user` / `secret_sauce` |
| TC-S2-PERF-001 | `k6` | carga | jsonplaceholder.typicode.com | nenhuma |
| TC-S2-VISUAL-001 | `playwright-visual` | visual | en.wikipedia.org | nenhuma |
| TC-S2-A11Y-001 | `axe-core` | acessibilidade | demoqa.com | nenhuma |
| TC-S2-SEC-001 | `zap` | segurança | httpbin.org | nenhuma |
| TC-S2-DB-001 | `db` | banco | sqlite:///qa_suite2.db | nenhuma |

**Total: 7 cenários · 7 executores · 7 ambientes distintos da Suite 1**

---

*Squad de Automação de Testes QA · v1.19.0 · Suite 2 · 2026-05-11*
