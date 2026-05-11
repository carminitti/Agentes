# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: visual.spec.ts >> Visual Regression Tests @visual >> TC-VIS-005 — Baseline pagina de login Practice Expand
- Location: visual.spec.ts:61:7

# Error details

```
Error: A snapshot doesn't exist at C:\Users\gabriel.carminitti\Documents\claude\agentes\tmp_visual_1778256594\baselines\visual.spec.ts-snapshots\expandtesting-login-baseline-win32.png, writing actual.
```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - paragraph [ref=e3]:
    - link "PMP Practice" [ref=e4] [cursor=pointer]:
      - /url: https://pmp.expandtesting.com/
    - text: "| Free PMP Certification Mock Exam Test +900 Questions & Quizzes"
    - link "Mock exam questions" [ref=e5] [cursor=pointer]:
      - img [ref=e7]
      - text: Mock exam questions
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
    - generic [ref=e32]:
      - insertion:
        - iframe [ref=e34]:
          
    - paragraph [ref=e36]:
      - text: Do you enjoy this platform? ❤️
      - link "Buy us a coffee" [ref=e37] [cursor=pointer]:
        - /url: https://www.buymeacoffee.com/expandtesting
    - generic [ref=e38]:
      - insertion [ref=e40]:
        - generic [ref=e43]:
          - heading "These are topics related to the article that might interest you" [level=2] [ref=e45]: Discover more
          - link "Search Engines" [ref=e46] [cursor=pointer]:
            - generic "Search Engines" [ref=e47]
            - img [ref=e49]
          - link "Internet Software" [ref=e51] [cursor=pointer]:
            - generic "Internet Software" [ref=e52]
            - img [ref=e54]
          - link "Email & Messaging" [ref=e56] [cursor=pointer]:
            - generic "Email & Messaging" [ref=e57]
            - img [ref=e59]
          - link "Email" [ref=e61] [cursor=pointer]:
            - generic "Email" [ref=e62]
            - img [ref=e64]
          - link "Computer Science" [ref=e66] [cursor=pointer]:
            - generic "Computer Science" [ref=e67]
            - img [ref=e69]
          - link "Development Tools" [ref=e71] [cursor=pointer]:
            - generic "Development Tools" [ref=e72]
            - img [ref=e74]
          - link "Social Networks" [ref=e76] [cursor=pointer]:
            - generic "Social Networks" [ref=e77]
            - img [ref=e79]
          - link "Computers & Electronics" [ref=e81] [cursor=pointer]:
            - generic "Computers & Electronics" [ref=e82]
            - img [ref=e84]
      - generic [ref=e88]:
        - navigation "breadcrumb mb-2" [ref=e89]:
          - list [ref=e90]:
            - listitem [ref=e91]:
              - link "Practice" [ref=e92] [cursor=pointer]:
                - /url: /
            - listitem [ref=e93]:
              - text: /
              - link "Home - My Notes - The App for Automation Testing Practice" [ref=e94] [cursor=pointer]:
                - /url: /notes/app/
        - generic [ref=e100]:
          - heading "Login" [level=1] [ref=e101]
          - generic [ref=e102]:
            - generic [ref=e103]:
              - generic [ref=e104]:
                - generic [ref=e105]: Email address
                - textbox "Email address" [ref=e106]
              - generic [ref=e107]:
                - generic [ref=e108]: Password
                - link "Forgot password" [ref=e109] [cursor=pointer]:
                  - /url: /notes/app/forgot-password
                - textbox "Password" [ref=e110]
            - button "Login" [ref=e112] [cursor=pointer]
          - generic [ref=e113]:
            - link "Login with Google" [ref=e114] [cursor=pointer]:
              - /url: https://practice.expandtesting.com/notes/app/auth/google
            - link "Login with LinkedIn" [ref=e115] [cursor=pointer]:
              - /url: https://practice.expandtesting.com/notes/app/auth/linkedin
            - link "Software" [ref=e116] [cursor=pointer]:
              - img [ref=e118]
              - text: Software
          - generic [ref=e120]:
            - text: Don't have an account?
            - link "Create a free account!" [ref=e121] [cursor=pointer]:
              - /url: /notes/app/register
      - insertion [ref=e123]:
        - generic [ref=e126]:
          - heading "These are topics related to the article that might interest you" [level=2] [ref=e128]: Discover more
          - link "Programming" [ref=e129] [cursor=pointer]:
            - generic "Programming" [ref=e130]
            - img [ref=e132]
          - link "AI Tools, Chatbots & Virtual Assistants" [ref=e134] [cursor=pointer]:
            - generic "AI Tools, Chatbots & Virtual Assistants" [ref=e135]
            - img [ref=e137]
          - link "Dictionaries & Encyclopedias" [ref=e139] [cursor=pointer]:
            - generic "Dictionaries & Encyclopedias" [ref=e140]
            - img [ref=e142]
          - link "Networking" [ref=e144] [cursor=pointer]:
            - generic "Networking" [ref=e145]
            - img [ref=e147]
          - link "Web Apps & Online Tools" [ref=e149] [cursor=pointer]:
            - generic "Web Apps & Online Tools" [ref=e150]
            - img [ref=e152]
          - link "WebdriverIO tutorials" [ref=e154] [cursor=pointer]:
            - generic "WebdriverIO tutorials" [ref=e155]
            - img [ref=e157]
          - link "Automation consulting service" [ref=e159] [cursor=pointer]:
            - generic "Automation consulting service" [ref=e160]
            - img [ref=e162]
          - link "Website testing services" [ref=e164] [cursor=pointer]:
            - generic "Website testing services" [ref=e165]
            - img [ref=e167]
  - contentinfo [ref=e169]:
    - generic [ref=e174]:
      - heading "Practice Test Automation WebSite for Web UI and Rest API" [level=4] [ref=e175]
      - paragraph [ref=e176]:
        - text: "Version: e64cd80e | Copyright"
        - link "Expand Testing" [ref=e177] [cursor=pointer]:
          - /url: https://expandtesting.com/
        - text: "2026"
  - img [ref=e179] [cursor=pointer]
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import * as fs from 'fs';
  3  | import * as path from 'path';
  4  | 
  5  | const baselineDir = path.join(__dirname, 'baselines');
  6  | fs.mkdirSync(baselineDir, { recursive: true });
  7  | 
  8  | test.describe('Visual Regression Tests @visual', () => {
  9  | 
  10 |   test('TC-VIS-001 — Baseline homepage AutomationExercise', async ({ page }) => {
  11 |     await page.goto('https://automationexercise.com', { waitUntil: 'domcontentloaded' });
  12 |     await page.waitForTimeout(1500);
  13 |     // Ocultar elementos dinamicos (banners, timers)
  14 |     await page.evaluate(() => {
  15 |       document.querySelectorAll('[id*="timer"], [class*="countdown"], [class*="timer"]').forEach((el: any) => {
  16 |         el.style.visibility = 'hidden';
  17 |       });
  18 |     });
  19 |     await expect(page).toHaveScreenshot('automationexercise_home_baseline.png', {
  20 |       maxDiffPixelRatio: 0.02,
  21 |       animations: 'disabled',
  22 |       fullPage: true,
  23 |     });
  24 |   });
  25 | 
  26 |   test('TC-VIS-002 — Baseline pagina de produtos AutomationExercise', async ({ page }) => {
  27 |     await page.goto('https://automationexercise.com/products', { waitUntil: 'domcontentloaded' });
  28 |     await page.waitForTimeout(1000);
  29 |     await expect(page).toHaveScreenshot('automationexercise_products_baseline.png', {
  30 |       maxDiffPixelRatio: 0.02,
  31 |       animations: 'disabled',
  32 |       fullPage: true,
  33 |     });
  34 |   });
  35 | 
  36 |   test('TC-VIS-003 — Comparacao visual homepage dentro do threshold', async ({ page }) => {
  37 |     await page.goto('https://automationexercise.com', { waitUntil: 'domcontentloaded' });
  38 |     await page.waitForTimeout(1500);
  39 |     await page.evaluate(() => {
  40 |       document.querySelectorAll('[id*="timer"], [class*="countdown"], [class*="timer"]').forEach((el: any) => {
  41 |         el.style.visibility = 'hidden';
  42 |       });
  43 |     });
  44 |     await expect(page).toHaveScreenshot('automationexercise_home_baseline.png', {
  45 |       maxDiffPixelRatio: 0.02,
  46 |       animations: 'disabled',
  47 |       fullPage: true,
  48 |     });
  49 |   });
  50 | 
  51 |   test('TC-VIS-004 — Comparacao visual produtos (pode ter regressao)', async ({ page }) => {
  52 |     await page.goto('https://automationexercise.com/products', { waitUntil: 'domcontentloaded' });
  53 |     await page.waitForTimeout(1000);
  54 |     await expect(page).toHaveScreenshot('automationexercise_products_baseline.png', {
  55 |       maxDiffPixelRatio: 0.02,
  56 |       animations: 'disabled',
  57 |       fullPage: true,
  58 |     });
  59 |   });
  60 | 
  61 |   test('TC-VIS-005 — Baseline pagina de login Practice Expand', async ({ page }) => {
  62 |     await page.goto('https://practice.expandtesting.com/notes/app/login', { waitUntil: 'domcontentloaded' });
  63 |     await page.waitForTimeout(1000);
> 64 |     await expect(page).toHaveScreenshot('expandtesting_login_baseline.png', {
     |     ^ Error: A snapshot doesn't exist at C:\Users\gabriel.carminitti\Documents\claude\agentes\tmp_visual_1778256594\baselines\visual.spec.ts-snapshots\expandtesting-login-baseline-win32.png, writing actual.
  65 |       maxDiffPixelRatio: 0.02,
  66 |       animations: 'disabled',
  67 |     });
  68 |   });
  69 | 
  70 |   test('TC-VIS-006 — Baseline dashboard Practice Expand apos login', async ({ page }) => {
  71 |     await page.goto('https://practice.expandtesting.com/notes/app/login', { waitUntil: 'domcontentloaded' });
  72 |     await page.getByPlaceholder(/email/i).fill('qa_agente_v3@test.com');
  73 |     await page.getByPlaceholder(/password/i).fill('Test@1234');
  74 |     await page.getByRole('button', { name: /login/i }).click();
  75 |     await page.waitForLoadState('domcontentloaded');
  76 |     await page.waitForTimeout(2000);
  77 |     await expect(page).toHaveScreenshot('expandtesting_dashboard_baseline.png', {
  78 |       maxDiffPixelRatio: 0.03,
  79 |       animations: 'disabled',
  80 |     });
  81 |   });
  82 | 
  83 | });
  84 | 
```