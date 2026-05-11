# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: src\specs\login.spec.ts >> Login @smoke @sanity @e2e >> TC-CL-002 — Verificar login com credenciais válidas
- Location: src\specs\login.spec.ts:21:7

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByText(/logged in as/i)
Expected: visible
Timeout: 10000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 10000ms
  - waiting for getByText(/logged in as/i)

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - banner [ref=e2]:
    - generic [ref=e5]:
      - link "Website for automation practice" [ref=e8] [cursor=pointer]:
        - /url: /
        - img "Website for automation practice" [ref=e9]
      - list [ref=e12]:
        - listitem [ref=e13]:
          - link " Home" [ref=e14] [cursor=pointer]:
            - /url: /
            - generic [ref=e15]: 
            - text: Home
        - listitem [ref=e16]:
          - link " Products" [ref=e17] [cursor=pointer]:
            - /url: /products
            - generic [ref=e18]: 
            - text: Products
        - listitem [ref=e19]:
          - link " Cart" [ref=e20] [cursor=pointer]:
            - /url: /view_cart
            - generic [ref=e21]: 
            - text: Cart
        - listitem [ref=e22]:
          - link " Signup / Login" [ref=e23] [cursor=pointer]:
            - /url: /login
            - generic [ref=e24]: 
            - text: Signup / Login
        - listitem [ref=e25]:
          - link " Test Cases" [ref=e26] [cursor=pointer]:
            - /url: /test_cases
            - generic [ref=e27]: 
            - text: Test Cases
        - listitem [ref=e28]:
          - link " API Testing" [ref=e29] [cursor=pointer]:
            - /url: /api_list
            - generic [ref=e30]: 
            - text: API Testing
        - listitem [ref=e31]:
          - link " Video Tutorials" [ref=e32] [cursor=pointer]:
            - /url: https://www.youtube.com/c/AutomationExercise
            - generic [ref=e33]: 
            - text: Video Tutorials
        - listitem [ref=e34]:
          - link " Contact us" [ref=e35] [cursor=pointer]:
            - /url: /contact_us
            - generic [ref=e36]: 
            - text: Contact us
  - generic [ref=e39]:
    - generic [ref=e41]:
      - heading "Login to your account" [level=2] [ref=e42]
      - generic [ref=e43]:
        - textbox "Email Address" [ref=e44]: test@test.com
        - textbox "Password" [ref=e45]: test123
        - paragraph [ref=e46]: Your email or password is incorrect!
        - button "Login" [ref=e47] [cursor=pointer]
    - heading "OR" [level=2] [ref=e49]
    - generic [ref=e51]:
      - heading "New User Signup!" [level=2] [ref=e52]
      - generic [ref=e53]:
        - textbox "Name" [ref=e54]
        - textbox "Email Address" [ref=e55]
        - button "Signup" [ref=e56] [cursor=pointer]
  - contentinfo [ref=e57]:
    - generic [ref=e62]:
      - heading "Subscription" [level=2] [ref=e63]
      - generic [ref=e64]:
        - textbox "Your email address" [ref=e65]
        - button "" [ref=e66] [cursor=pointer]:
          - generic [ref=e67]: 
        - paragraph [ref=e68]:
          - text: Get the most recent updates from
          - text: our site and be updated your self...
    - paragraph [ref=e72]: Copyright © 2021 All rights reserved
  - text: 
  - insertion [ref=e73]:
    - iframe [ref=e76]:
      - generic [ref=f23e2]:
        - iframe [ref=f23e5]:
          - generic [ref=f31e1]:
            - img [ref=f31e4]
            - img [ref=f31e7]
            - paragraph [ref=f31e9]: Escolha seu plano
            - paragraph [ref=f31e11]: Curta e economize
            - generic [ref=f31e12]:
              - paragraph [ref=f31e15] [cursor=pointer]: Selecione o plano
              - paragraph [ref=f31e16]: Termos se aplicam.
            - generic [ref=f31e17]:
              - paragraph [ref=f31e20] [cursor=pointer]: Selecione o plano
              - paragraph [ref=f31e21]: Termos se aplicam.
            - generic [ref=f31e22]:
              - paragraph [ref=f31e25] [cursor=pointer]: Selecione o plano
              - paragraph [ref=f31e26]: Termos se aplicam.
            - generic [ref=f31e27]:
              - generic [ref=f31e28]:
                - paragraph [ref=f31e29]: Standard
                - paragraph [ref=f31e30]: 2 dispositivos ao mesmo tempo
                - paragraph [ref=f31e31]: R$39,90/mês
              - generic [ref=f31e32]:
                - paragraph [ref=f31e33]: Platinum
                - paragraph [ref=f31e34]: 4 dispositivos ao mesmo tempo
                - paragraph [ref=f31e35]: R$55,90/mês
              - generic [ref=f31e36]:
                - paragraph [ref=f31e37]: Básico com anúncios
                - paragraph [ref=f31e38]: Resolução Full HD
                - paragraph [ref=f31e39]: 12x R$22,90/mês
            - generic [ref=f31e43]:
              - paragraph [ref=f31e45] [cursor=pointer]: Por mês
              - paragraph [ref=f31e47] [cursor=pointer]: Por ano
            - img [ref=f31e48] [cursor=pointer]
            - img [ref=f31e49] [cursor=pointer]
        - generic [ref=f23e6]:
          - generic:
            - img [ref=f23e10] [cursor=pointer]
            - button [ref=f23e12] [cursor=pointer]:
              - img [ref=f23e13]
```

# Test source

```ts
  1  | import { test, expect } from '../support/fixtures';
  2  | import { request } from '@playwright/test';
  3  | 
  4  | test.describe('Login @smoke @sanity @e2e', () => {
  5  | 
  6  |   // TC-CL-001: Smoke — página de login carrega corretamente
  7  |   test('TC-CL-001 — Verificar se a página de login carrega corretamente', async ({ loginPage, page }) => {
  8  |     await test.step('Acessar a página de login', async () => {
  9  |       await loginPage.navigate();
  10 |     });
  11 | 
  12 |     await test.step('Verificar elementos obrigatórios presentes', async () => {
  13 |       await expect(loginPage.formLogin).toBeVisible();
  14 |       await expect(loginPage.inputEmail).toBeVisible();
  15 |       await expect(loginPage.inputPassword).toBeVisible();
  16 |       await expect(loginPage.btnLogin).toBeVisible();
  17 |     });
  18 |   });
  19 | 
  20 |   // TC-CL-002: E2E — login com credenciais válidas
  21 |   test('TC-CL-002 — Verificar login com credenciais válidas', async ({ loginPage, page }) => {
  22 |     await test.step('Acessar a página de login', async () => {
  23 |       await loginPage.navigate();
  24 |     });
  25 | 
  26 |     await test.step('Preencher credenciais e submeter', async () => {
  27 |       await loginPage.login(
  28 |         process.env.USER_EMAIL as string,
  29 |         process.env.USER_PASSWORD as string
  30 |       );
  31 |     });
  32 | 
  33 |     await test.step('Verificar redirecionamento para home autenticada', async () => {
> 34 |       await expect(loginPage.loggedInAs).toBeVisible({ timeout: 10_000 });
     |                                          ^ Error: expect(locator).toBeVisible() failed
  35 |     });
  36 |   });
  37 | 
  38 |   // TC-CL-003: E2E — login com credenciais inválidas exibe erro
  39 |   test('TC-CL-003 — Verificar login com credenciais inválidas', async ({ loginPage }) => {
  40 |     await test.step('Acessar a página de login', async () => {
  41 |       await loginPage.navigate();
  42 |     });
  43 | 
  44 |     await test.step('Preencher credenciais inválidas e submeter', async () => {
  45 |       await loginPage.login('wrong@email.com', 'wrongpass');
  46 |     });
  47 | 
  48 |     await test.step('Verificar mensagem de erro', async () => {
  49 |       await expect(loginPage.errorMessage).toBeVisible({ timeout: 5_000 });
  50 |     });
  51 |   });
  52 | 
  53 |   // TC-CL-004: Sanity http — API de produtos retorna status 200
  54 |   test('TC-CL-004 — Verificar se a API de produtos retorna status 200', async ({ page }) => {
  55 |     let statusCode: number;
  56 |     let body: unknown;
  57 | 
  58 |     await test.step('Fazer GET /api/productsList', async () => {
  59 |       const ctx = await (page.context().request as unknown as { newContext?: never });
  60 |       const apiCtx = await request.newContext({ baseURL: process.env.BASE_URL });
  61 |       const resp = await apiCtx.get('/api/productsList');
  62 |       statusCode = resp.status();
  63 |       body = await resp.json();
  64 |       await apiCtx.dispose();
  65 |     });
  66 | 
  67 |     await test.step('Verificar status 200 e lista de produtos', async () => {
  68 |       expect(statusCode!).toBe(200);
  69 |       const data = body as { products?: unknown[] };
  70 |       expect(Array.isArray(data.products) && data.products.length > 0).toBeTruthy();
  71 |     });
  72 |   });
  73 | 
  74 | });
  75 | 
```