/**
 * Browser test runner — executes Playwright tests for SauceDemo + The Internet suite
 * and writes resultado.json to the suite browser/ folder.
 *
 * Allowed by settings.local.json: Bash(node run_browser_tests.js)
 */
const { chromium } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

const SUITE_BROWSER_DIR = path.join(
  __dirname,
  'agents', 'suites',
  'suite_brw_api_sec_perf_vis_acc_db_gql_ws_dd_wh_cha_i18n_grpc_20260521_133730',
  'browser'
);
const RESULTADO_PATH = path.join(SUITE_BROWSER_DIR, 'resultado.json');

console.log('[INFO] Suite dir:', SUITE_BROWSER_DIR);
console.log('[INFO] Node:', process.version);

fs.mkdirSync(path.join(SUITE_BROWSER_DIR, 'reports'), { recursive: true });
fs.mkdirSync(path.join(SUITE_BROWSER_DIR, 'screenshots'), { recursive: true });

// ── helpers ──────────────────────────────────────────────────────────────────

function ts() {
  return new Date().toISOString().replace('T', ' ').slice(0, 19);
}

async function runTC(id, title, fn) {
  const start = Date.now();
  const logs = [];
  const consoleLogs = [];
  const networkLogs = [];
  const steps = [];
  let status = 'passed';
  let error = null;
  let browser = null;

  try {
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      ignoreHTTPSErrors: true,
      viewport: { width: 1280, height: 720 },
    });
    const page = await context.newPage();

    // Capture console and network
    page.on('console', msg => consoleLogs.push(`[CONSOLE:${msg.type().toUpperCase()}] ${msg.text()}`));
    page.on('pageerror', err => consoleLogs.push(`[PAGE_ERROR] ${err.message}`));
    page.on('requestfailed', req => consoleLogs.push(`[REQUEST_FAILED] ${req.method()} ${req.url()}`));
    page.on('response', resp => {
      try {
        const u = new URL(resp.url());
        if (['www.saucedemo.com', 'the-internet.herokuapp.com'].includes(u.hostname)) {
          networkLogs.push(`[NETWORK] ${resp.request().method()} ${u.pathname} → ${resp.status()}`);
        }
      } catch {}
    });

    try {
      await fn(page, logs, steps);
    } finally {
      // Screenshot on failure
      if (status === 'failed' || status === 'error') {
        try {
          const ssPath = path.join(SUITE_BROWSER_DIR, 'screenshots', `${id}.png`);
          await page.screenshot({ path: ssPath });
          logs.push(`[SCREENSHOT] Saved to ${ssPath}`);
        } catch {}
      }
      await browser.close();
    }
  } catch (e) {
    status = 'failed';
    error = (e.message || String(e)).slice(0, 600);
    logs.push(`[ERROR] ${error}`);
    if (browser) {
      try { await browser.close(); } catch {}
    }
  }

  const duration_ms = Date.now() - start;
  console.log(`[${status.toUpperCase()}] ${id} — ${title} (${duration_ms}ms)`);

  return {
    id, title, type: 'browser', status, duration_ms, error,
    steps, logs, console_logs: consoleLogs, network_logs: networkLogs,
    attempts: 1, flaky: false, retry_diff_logs: false,
    attempt_logs: [{ attempt: 1, status, error, duration_ms }],
  };
}

// ── test cases ────────────────────────────────────────────────────────────────

async function main() {
  const results = [];

  // TC-BRW-001 — Login válido → inventário
  results.push(await runTC(
    'TC-BRW-001',
    'Login com credenciais válidas redireciona para inventário',
    async (page, logs, steps) => {
      page.setDefaultNavigationTimeout(45000);
      page.setDefaultTimeout(30000);

      logs.push('[NAV] Acessando https://www.saucedemo.com');
      await page.goto('https://www.saucedemo.com', { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('#user-name', { timeout: 30000 });
      steps.push({ step: 'Navegar para a página de login', status: 'passed' });

      logs.push('[ACTION] Preenchendo #user-name: standard_user');
      await page.fill('#user-name', 'standard_user');
      logs.push('[ACTION] Preenchendo #password: secret_sauce');
      await page.fill('#password', 'secret_sauce');
      logs.push('[ACTION] Clicando em #login-button');
      await page.click('#login-button');
      steps.push({ step: 'Preencher credenciais e fazer login', status: 'passed' });

      await page.waitForURL('**/inventory.html', { timeout: 30000 });
      const url = page.url();
      if (!url.includes('inventory.html')) {
        throw new Error(`Esperado URL contendo /inventory.html. URL atual: ${url}`);
      }
      logs.push(`[ASSERT] URL contém /inventory.html ✓ (${url})`);
      steps.push({ step: 'Validar redirecionamento para inventário', status: 'passed' });
    }
  ));

  // TC-BRW-002 — Login inválido → mensagem de erro
  results.push(await runTC(
    'TC-BRW-002',
    'Login com credenciais inválidas exibe mensagem de erro',
    async (page, logs, steps) => {
      page.setDefaultNavigationTimeout(45000);
      page.setDefaultTimeout(30000);

      logs.push('[NAV] Acessando https://www.saucedemo.com');
      await page.goto('https://www.saucedemo.com', { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('#user-name', { timeout: 30000 });
      steps.push({ step: 'Navegar para a página de login', status: 'passed' });

      logs.push('[ACTION] Preenchendo credenciais inválidas: wrong_user / wrong_pass');
      await page.fill('#user-name', 'wrong_user');
      await page.fill('#password', 'wrong_pass');
      await page.click('#login-button');
      steps.push({ step: 'Submeter credenciais inválidas', status: 'passed' });

      await page.waitForSelector('[data-test="error"]', { timeout: 15000 });
      const errorEl = page.locator('[data-test="error"]');
      const visible = await errorEl.isVisible();
      if (!visible) {
        throw new Error('Esperado: container de erro visível. Encontrado: não visível.');
      }
      const errorText = (await errorEl.textContent()) || '';
      if (!errorText.includes('Username and password do not match')) {
        throw new Error(`Esperado texto "Username and password do not match". Encontrado: "${errorText}"`);
      }
      logs.push(`[ASSERT] Mensagem de erro visível ✓: "${errorText.trim()}"`);
      steps.push({ step: 'Validar mensagem de erro', status: 'passed' });
    }
  ));

  // TC-BRW-003 — Listagem ≥ 6 itens
  results.push(await runTC(
    'TC-BRW-003',
    'Listagem de produtos exibe pelo menos 6 itens',
    async (page, logs, steps) => {
      page.setDefaultNavigationTimeout(45000);
      page.setDefaultTimeout(30000);

      logs.push('[NAV] Acessando https://www.saucedemo.com');
      await page.goto('https://www.saucedemo.com', { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('#user-name', { timeout: 30000 });

      await page.fill('#user-name', 'standard_user');
      await page.fill('#password', 'secret_sauce');
      await page.click('#login-button');
      await page.waitForURL('**/inventory.html', { timeout: 30000 });
      await page.waitForSelector('.inventory_item', { timeout: 30000 });
      steps.push({ step: 'Login e aguardar inventário', status: 'passed' });

      const count = await page.locator('.inventory_item').count();
      logs.push(`[ASSERT] Itens encontrados: ${count}`);
      if (count < 6) {
        throw new Error(`Esperado >= 6 produtos. Encontrado: ${count}`);
      }
      logs.push(`[ASSERT] Contagem de produtos ${count} >= 6 ✓`);
      steps.push({ step: `Validar >= 6 itens (encontrado: ${count})`, status: 'passed' });
    }
  ));

  // TC-BRW-004 — Adicionar produto atualiza badge
  results.push(await runTC(
    'TC-BRW-004',
    'Adicionar produto ao carrinho atualiza badge do carrinho',
    async (page, logs, steps) => {
      page.setDefaultNavigationTimeout(45000);
      page.setDefaultTimeout(30000);

      logs.push('[NAV] Acessando https://www.saucedemo.com');
      await page.goto('https://www.saucedemo.com', { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('#user-name', { timeout: 30000 });

      await page.fill('#user-name', 'standard_user');
      await page.fill('#password', 'secret_sauce');
      await page.click('#login-button');
      await page.waitForURL('**/inventory.html', { timeout: 30000 });
      await page.waitForSelector('.btn_inventory', { timeout: 30000 });
      steps.push({ step: 'Login e aguardar inventário', status: 'passed' });

      logs.push('[ACTION] Clicando no primeiro botão .btn_inventory (Add to cart)');
      await page.locator('.btn_inventory').first().click();
      steps.push({ step: 'Clicar em Add to cart', status: 'passed' });

      await page.waitForSelector('.shopping_cart_badge', { timeout: 10000 });
      const badgeText = await page.locator('.shopping_cart_badge').textContent();
      if (badgeText !== '1') {
        throw new Error(`Esperado badge do carrinho = "1". Encontrado: "${badgeText}"`);
      }
      logs.push(`[ASSERT] Badge do carrinho = "${badgeText}" ✓`);
      steps.push({ step: 'Validar badge do carrinho = "1"', status: 'passed' });
    }
  ));

  // TC-BRW-005 — Fluxo completo de checkout
  results.push(await runTC(
    'TC-BRW-005',
    'Fluxo completo de checkout finalizado com sucesso',
    async (page, logs, steps) => {
      page.setDefaultNavigationTimeout(45000);
      page.setDefaultTimeout(30000);

      logs.push('[NAV] Acessando https://www.saucedemo.com');
      await page.goto('https://www.saucedemo.com', { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('#user-name', { timeout: 30000 });

      await page.fill('#user-name', 'standard_user');
      await page.fill('#password', 'secret_sauce');
      await page.click('#login-button');
      await page.waitForURL('**/inventory.html', { timeout: 30000 });
      await page.waitForSelector('.btn_inventory', { timeout: 30000 });
      steps.push({ step: 'Login e aguardar inventário', status: 'passed' });

      logs.push('[ACTION] Adicionando primeiro produto ao carrinho');
      await page.locator('.btn_inventory').first().click();
      steps.push({ step: 'Adicionar primeiro produto', status: 'passed' });

      logs.push('[NAV] Navegando para /cart.html');
      await page.goto('https://www.saucedemo.com/cart.html', { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('#checkout', { timeout: 15000 });
      steps.push({ step: 'Ir para carrinho', status: 'passed' });

      logs.push('[ACTION] Clicando em Checkout');
      await page.click('#checkout');
      await page.waitForURL('**/checkout-step-one.html', { timeout: 15000 });
      steps.push({ step: 'Iniciar checkout', status: 'passed' });

      logs.push('[ACTION] Preenchendo dados: QA / Tester / 12345');
      await page.fill('#first-name', 'QA');
      await page.fill('#last-name', 'Tester');
      await page.fill('#postal-code', '12345');
      await page.click('#continue');
      await page.waitForURL('**/checkout-step-two.html', { timeout: 15000 });
      steps.push({ step: 'Preencher informações de checkout e continuar', status: 'passed' });

      logs.push('[ACTION] Clicando em Finish');
      await page.click('#finish');
      await page.waitForURL('**/checkout-complete.html', { timeout: 15000 });
      steps.push({ step: 'Finalizar pedido', status: 'passed' });

      const successEl = page.locator('.complete-header');
      await successEl.waitFor({ timeout: 15000 });
      const successText = (await successEl.textContent()) || '';
      if (!successText.toLowerCase().includes('thank you for your order')) {
        throw new Error(`Esperado texto "Thank you for your order". Encontrado: "${successText}"`);
      }
      logs.push(`[ASSERT] Mensagem de sucesso visível ✓: "${successText.trim()}"`);
      steps.push({ step: 'Validar mensagem de sucesso', status: 'passed' });
    }
  ));

  // TC-BRW-006 — The Internet basic auth
  results.push(await runTC(
    'TC-BRW-006',
    'Login básico protege página no The Internet',
    async (page, logs, steps) => {
      page.setDefaultNavigationTimeout(60000);
      page.setDefaultTimeout(45000);

      logs.push('[NAV] Acessando https://the-internet.herokuapp.com/login');
      await page.goto('https://the-internet.herokuapp.com/login', { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('#username', { timeout: 45000 });
      steps.push({ step: 'Navegar para a página de login', status: 'passed' });

      logs.push('[ACTION] Preenchendo #username: tomsmith');
      await page.fill('#username', 'tomsmith');
      logs.push('[ACTION] Preenchendo #password: SuperSecretPassword!');
      await page.fill('#password', 'SuperSecretPassword!');
      logs.push('[ACTION] Clicando em button[type=submit]');
      await page.click('button[type="submit"]');
      steps.push({ step: 'Preencher credenciais e fazer login', status: 'passed' });

      // Wait for navigation or flash
      await page.waitForTimeout(2000);
      const currentUrl = page.url();
      let flashText = '';
      try {
        const flashEl = page.locator('#flash');
        if (await flashEl.isVisible({ timeout: 5000 })) {
          flashText = (await flashEl.textContent()) || '';
        }
      } catch {}

      const urlIsSecure = currentUrl.includes('/secure');
      const flashContainsText = flashText.toLowerCase().includes('logged into a secure area');

      logs.push(`[ASSERT] URL atual: ${currentUrl}`);
      logs.push(`[ASSERT] Flash message: "${flashText.trim()}"`);

      if (!urlIsSecure && !flashContainsText) {
        throw new Error(
          `Esperado: URL contém '/secure' OU flash contém 'logged into a secure area'. ` +
          `URL atual: ${currentUrl}, Flash: "${flashText.trim()}"`
        );
      }

      if (urlIsSecure) logs.push('[ASSERT] URL contém /secure ✓');
      if (flashContainsText) logs.push('[ASSERT] Flash message contém "logged into a secure area" ✓');
      steps.push({ step: 'Validar acesso à área segura', status: 'passed' });
    }
  ));

  // ── Build resultado.json ─────────────────────────────────────────────────
  let passed = 0, failed = 0, errors = 0, skipped = 0;
  for (const r of results) {
    if (r.status === 'passed') passed++;
    else if (r.status === 'failed') failed++;
    else if (r.status === 'skipped') skipped++;
    else errors++;
  }

  // Strip internal helpers before writing
  const cleanResults = results.map(r => ({
    id: r.id,
    title: r.title,
    type: r.type,
    status: r.status,
    duration_ms: r.duration_ms,
    error: r.error,
    attempts: r.attempts,
    flaky: r.flaky,
    retry_diff_logs: r.retry_diff_logs,
    attempt_logs: r.attempt_logs,
    steps: r.steps,
    logs: r.logs,
    console_logs: r.console_logs,
    network_logs: r.network_logs,
  }));

  const resultado = {
    executor: 'executor-browser',
    environment: 'https://www.saucedemo.com',
    credentials_failed: false,
    results: cleanResults,
    summary: {
      total: results.length,
      passed,
      failed,
      error: errors,
      skipped,
      warnings: [],
    },
  };

  fs.writeFileSync(RESULTADO_PATH, JSON.stringify(resultado, null, 2), 'utf8');

  // Write execution.log
  const logLines = [`[${ts()}] === executor-browser — início ===`];
  logLines.push(`[${ts()}] Ambiente: https://www.saucedemo.com`);
  for (const r of results) {
    logLines.push(`[${ts()}] [${r.id}] ${r.title}`);
    for (const line of (r.logs || [])) logLines.push(`[${ts()}]   ${line}`);
    logLines.push(`[${ts()}]   → STATUS: ${r.status.toUpperCase()}`);
  }
  logLines.push(`[${ts()}] === Fim: ${passed} passou, ${failed} falhou, ${errors} erro ===`);
  fs.writeFileSync(path.join(SUITE_BROWSER_DIR, 'execution.log'), logLines.join('\n'), 'utf8');

  console.log('\n[DONE] resultado.json written to:', RESULTADO_PATH);
  console.log('[SUMMARY] Total:', results.length, '| Passed:', passed, '| Failed:', failed, '| Error:', errors);
}

main().catch(e => {
  console.error('[FATAL]', e.message || e);
  process.exit(1);
});
