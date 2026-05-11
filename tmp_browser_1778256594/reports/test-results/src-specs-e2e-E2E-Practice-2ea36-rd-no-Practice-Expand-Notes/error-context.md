# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: src\specs\e2e.spec.ts >> E2E Practice Expand Notes @e2e >> TC-E2E-009 — Login e dashboard no Practice Expand Notes
- Location: src\specs\e2e.spec.ts:189:7

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: locator.fill: Test timeout of 30000ms exceeded.
Call log:
  - waiting for getByPlaceholder(/email/i)

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - paragraph [ref=e3]:
    - link "PMP Practice" [ref=e4] [cursor=pointer]:
      - /url: https://pmp.expandtesting.com/
    - text: "| Free PMP Certification Mock Exam Test +900 Questions & Quizzes"
    - link "PMP certification prep" [ref=e5] [cursor=pointer]:
      - img [ref=e7]
      - text: PMP certification prep
  - banner [ref=e10]:
    - navigation "Main navigation" [ref=e11]:
      - link "SUT" [ref=e12] [cursor=pointer]:
        - /url: /
        - 'img "Best Website for Practice Automation Testing: Free UI and REST API Examples and Apps. Using Cypress, Playwright, Selenium, WebdriverIO and Postman." [ref=e13]'
        - text: Practice
      - generic [ref=e14]:
        - list [ref=e15]:
          - listitem [ref=e16]:
            - button "Demos" [ref=e17] [cursor=pointer]
          - listitem [ref=e18]:
            - link "Tools" [ref=e19] [cursor=pointer]:
              - /url: /#tools
          - listitem [ref=e20]:
            - link "Tips" [ref=e21] [cursor=pointer]:
              - /url: /tips
          - listitem [ref=e22]:
            - link "Test Cases" [ref=e23] [cursor=pointer]:
              - /url: /test-cases
          - listitem [ref=e24]:
            - link "API Testing" [ref=e25] [cursor=pointer]:
              - /url: /notes/api/api-docs/
          - listitem [ref=e26]:
            - link "About" [ref=e27] [cursor=pointer]:
              - /url: /about
        - list
        - link "Free ISTQB Mock Exams" [ref=e28] [cursor=pointer]:
          - /url: https://istqb.expandtesting.com/
  - main [ref=e29]:
    - paragraph [ref=e34]:
      - text: Do you enjoy this platform? ❤️
      - link "Buy us a coffee" [ref=e35] [cursor=pointer]:
        - /url: https://www.buymeacoffee.com/expandtesting
    - generic [ref=e36]:
      - insertion [ref=e38]:
        - generic [ref=e41]:
          - heading "These are topics related to the article that might interest you" [level=2] [ref=e43]: Discover more
          - link "UI automation resources" [ref=e44] [cursor=pointer]:
            - generic "UI automation resources" [ref=e45]
            - img [ref=e47]
          - link "PMP certification prep" [ref=e49] [cursor=pointer]:
            - generic "PMP certification prep" [ref=e50]
            - img [ref=e52]
          - link "Test automation webinars" [ref=e54] [cursor=pointer]:
            - generic "Test automation webinars" [ref=e55]
            - img [ref=e57]
          - link "Automation testing tips" [ref=e59] [cursor=pointer]:
            - generic "Automation testing tips" [ref=e60]
            - img [ref=e62]
          - link "Software testing courses" [ref=e64] [cursor=pointer]:
            - generic "Software testing courses" [ref=e65]
            - img [ref=e67]
          - link "Mobile Apps & Add-Ons" [ref=e69] [cursor=pointer]:
            - generic "Mobile Apps & Add-Ons" [ref=e70]
            - img [ref=e72]
          - link "Automation practice platform" [ref=e74] [cursor=pointer]:
            - generic "Automation practice platform" [ref=e75]
            - img [ref=e77]
          - link "Cypress testing tutorials" [ref=e79] [cursor=pointer]:
            - generic "Cypress testing tutorials" [ref=e80]
            - img [ref=e82]
      - generic [ref=e86]:
        - navigation "breadcrumb mb-2" [ref=e87]:
          - list [ref=e88]:
            - listitem [ref=e89]:
              - link "Practice" [ref=e90] [cursor=pointer]:
                - /url: /
            - listitem [ref=e91]:
              - text: /
              - link "Home - My Notes - The App for Automation Testing Practice" [ref=e92] [cursor=pointer]:
                - /url: /notes/app/
        - generic [ref=e97]:
          - generic [ref=e98]:
            - heading "Welcome to Notes App" [level=1] [ref=e99]
            - heading "A Better Way To Track Your Tasks" [level=3] [ref=e100]
            - paragraph [ref=e101]:
              - text: Stay productive and organized with our notes app.
              - text: Create an account to get started and then easily create, edit, categorize, filter, search, and toggle your notes. Plus, update your profile and reset your password anytime.
              - text: Simplify your life with our notes app today!
            - generic [ref=e102]:
              - link "Login" [ref=e103] [cursor=pointer]:
                - /url: /notes/app/login
              - link "Create an account" [ref=e104] [cursor=pointer]:
                - /url: /notes/app/register
            - generic [ref=e105]:
              - paragraph [ref=e106]:
                - text: Connect with your
                - link "Google account" [ref=e107] [cursor=pointer]:
                  - /url: https://practice.expandtesting.com/notes/app/auth/google
                - text: quickly.
              - paragraph [ref=e108]:
                - link "Forgot your password?" [ref=e109] [cursor=pointer]:
                  - /url: /notes/app/forgot-password
          - img "Practice" [ref=e111]
      - insertion [ref=e113]:
        - generic [ref=e116]:
          - heading "These are topics related to the article that might interest you" [level=2] [ref=e118]: Discover more
          - link "Digital notebook" [ref=e119] [cursor=pointer]:
            - generic "Digital notebook" [ref=e120]
            - img [ref=e122]
          - link "API testing certification" [ref=e124] [cursor=pointer]:
            - generic "API testing certification" [ref=e125]
            - img [ref=e127]
          - link "Task management solution" [ref=e129] [cursor=pointer]:
            - generic "Task management solution" [ref=e130]
            - img [ref=e132]
          - link "Software testing books" [ref=e134] [cursor=pointer]:
            - generic "Software testing books" [ref=e135]
            - img [ref=e137]
          - link "Notes app subscription" [ref=e139] [cursor=pointer]:
            - generic "Notes app subscription" [ref=e140]
            - img [ref=e142]
          - link "Writers Resources" [ref=e144] [cursor=pointer]:
            - generic "Writers Resources" [ref=e145]
            - img [ref=e147]
          - link "Programming" [ref=e149] [cursor=pointer]:
            - generic "Programming" [ref=e150]
            - img [ref=e152]
          - link "Mac OS" [ref=e154] [cursor=pointer]:
            - generic "Mac OS" [ref=e155]
            - img [ref=e157]
  - contentinfo [ref=e159]:
    - generic [ref=e164]:
      - heading "Practice Test Automation WebSite for Web UI and Rest API" [level=4] [ref=e165]
      - paragraph [ref=e166]:
        - text: "Version: e64cd80e | Copyright"
        - link "Expand Testing" [ref=e167] [cursor=pointer]:
          - /url: https://expandtesting.com/
        - text: "2026"
  - img [ref=e169] [cursor=pointer]
  - generic [ref=e171]:
    - generic [ref=e172] [cursor=pointer]:
      - img [ref=e174]
      - link "Go to shopping options for Test automation webinars" [ref=e176]: Test automation webinars
    - button "Close shopping anchor" [ref=e177]
```

# Test source

```ts
  95  | 
  96  |     await test.step('Validar campos preenchidos', async () => {
  97  |       await expect(page.locator('#name')).toHaveValue('QA Agente');
  98  |       await expect(page.locator('#email')).toHaveValue('qa@teste.com');
  99  |       await captureScreenshot(page, 'TC-E2E-004-contato');
  100 |     });
  101 |   });
  102 | 
  103 | });
  104 | 
  105 | test.describe('E2E The Internet @e2e', () => {
  106 | 
  107 |   test('TC-E2E-005 — Login por formulario seguro no The Internet', async ({ page }) => {
  108 |     await test.step('Navegar para pagina de login', async () => {
  109 |       await page.goto('https://the-internet.herokuapp.com/login', { waitUntil: 'domcontentloaded' });
  110 |     });
  111 | 
  112 |     await test.step('Preencher credenciais e fazer login', async () => {
  113 |       await page.locator('#username').fill('tomsmith');
  114 |       await page.locator('#password').fill('SuperSecretPassword!');
  115 |       await page.locator("button[type='submit']").click();
  116 |       await page.waitForLoadState('domcontentloaded');
  117 |     });
  118 | 
  119 |     await test.step('Validar login bem-sucedido', async () => {
  120 |       await expect(page.locator('.flash.success')).toContainText('You logged into a secure area!');
  121 |       await expect(page.locator('h2')).toContainText('Secure Area');
  122 |       await captureScreenshot(page, 'TC-E2E-005-secure-area');
  123 |     });
  124 |   });
  125 | 
  126 |   test('TC-E2E-006 — Drag and drop no The Internet', async ({ page }) => {
  127 |     await test.step('Navegar para pagina drag and drop', async () => {
  128 |       await page.goto('https://the-internet.herokuapp.com/drag_and_drop', { waitUntil: 'domcontentloaded' });
  129 |     });
  130 | 
  131 |     await test.step('Realizar drag and drop', async () => {
  132 |       const colA = page.locator('#column-a');
  133 |       const colB = page.locator('#column-b');
  134 |       await colA.dragTo(colB);
  135 |       await page.waitForTimeout(500);
  136 |     });
  137 | 
  138 |     await test.step('Validar posicoes apos drag', async () => {
  139 |       const headerA = await page.locator('#column-a header').textContent();
  140 |       const headerB = await page.locator('#column-b header').textContent();
  141 |       // Drag and drop em alguns browsers pode nao funcionar perfeitamente - registrar o estado real
  142 |       await captureScreenshot(page, 'TC-E2E-006-drag-drop');
  143 |       // Aceitar ambos os resultados (drag pode ou nao funcionar dependendo do browser)
  144 |       expect(['A', 'B']).toContain(headerA?.trim());
  145 |       expect(['A', 'B']).toContain(headerB?.trim());
  146 |     });
  147 |   });
  148 | 
  149 |   test('TC-E2E-007 — Multiplas janelas no The Internet', async ({ page, context }) => {
  150 |     await test.step('Navegar para pagina de janelas', async () => {
  151 |       await page.goto('https://the-internet.herokuapp.com/windows', { waitUntil: 'domcontentloaded' });
  152 |     });
  153 | 
  154 |     await test.step('Abrir nova janela', async () => {
  155 |       const [newPage] = await Promise.all([
  156 |         context.waitForEvent('page'),
  157 |         page.getByText('Click Here').click()
  158 |       ]);
  159 |       await newPage.waitForLoadState('domcontentloaded');
  160 |       await expect(newPage.locator('h3')).toContainText('New Window');
  161 |       await captureScreenshot(newPage, 'TC-E2E-007-new-window');
  162 |     });
  163 |   });
  164 | 
  165 |   test('TC-E2E-008 — Upload de arquivo no The Internet', async ({ page }) => {
  166 |     await test.step('Navegar para pagina de upload', async () => {
  167 |       await page.goto('https://the-internet.herokuapp.com/upload', { waitUntil: 'domcontentloaded' });
  168 |     });
  169 | 
  170 |     await test.step('Fazer upload de arquivo', async () => {
  171 |       // Criar arquivo temporario para upload
  172 |       const tmpFile = path.join(screenshotsDir, 'test_upload.txt');
  173 |       fs.writeFileSync(tmpFile, 'arquivo de teste para upload');
  174 |       await page.setInputFiles('#file-upload', tmpFile);
  175 |       await page.locator('#file-submit').click();
  176 |       await page.waitForLoadState('domcontentloaded');
  177 |     });
  178 | 
  179 |     await test.step('Validar upload concluido', async () => {
  180 |       await expect(page.locator('#uploaded-files')).toBeVisible();
  181 |       await captureScreenshot(page, 'TC-E2E-008-upload');
  182 |     });
  183 |   });
  184 | 
  185 | });
  186 | 
  187 | test.describe('E2E Practice Expand Notes @e2e', () => {
  188 | 
  189 |   test('TC-E2E-009 — Login e dashboard no Practice Expand Notes', async ({ page }) => {
  190 |     await test.step('Navegar para pagina de notas', async () => {
  191 |       await page.goto('https://practice.expandtesting.com/notes/app', { waitUntil: 'domcontentloaded' });
  192 |     });
  193 | 
  194 |     await test.step('Fazer login', async () => {
> 195 |       await page.getByPlaceholder(/email/i).fill('qa_agente_v3@test.com');
      |                                             ^ Error: locator.fill: Test timeout of 30000ms exceeded.
  196 |       await page.getByPlaceholder(/password/i).fill('Test@1234');
  197 |       await page.getByRole('button', { name: /login/i }).click();
  198 |       await page.waitForLoadState('domcontentloaded');
  199 |     });
  200 | 
  201 |     await test.step('Validar dashboard', async () => {
  202 |       // Aguardar redirecionamento
  203 |       await page.waitForURL(/notes\/app/, { timeout: 10000 }).catch(() => {});
  204 |       const isLoggedIn = await page.locator('[class*="dashboard"], [class*="notes"], h1, h2').first().isVisible();
  205 |       expect(isLoggedIn).toBe(true);
  206 |       await captureScreenshot(page, 'TC-E2E-009-dashboard');
  207 |     });
  208 |   });
  209 | 
  210 | });
  211 | 
```