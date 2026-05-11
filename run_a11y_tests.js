
const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const SUITE_DIR = 'suite_axe_core_db_http_k6_magnitude_playwright_20260511_083909';
fs.mkdirSync(path.join(SUITE_DIR, 'acessibilidade'), { recursive: true });

function ts() {
  return new Date().toISOString().replace('T', ' ').slice(0, 19);
}

let AxeBuilder;
try {
  AxeBuilder = require('@axe-core/playwright').default;
} catch (e) {
  AxeBuilder = null;
}

async function runA11yTest(testId, title, url, options = {}) {
  const start = Date.now();
  const logs = [];
  let status = 'passed';
  let error = null;
  let violations = [];
  let passesCount = 0;
  let deployBlocked = false;
  const { actions, isDemo } = options;

  if (!AxeBuilder) {
    return {
      id: testId, title,
      status: 'skipped',
      deploy_blocked: false,
      violations: [],
      passes_count: 0,
      logs: ['[SKIP] @axe-core/playwright nao instalado -- instale com: npm install @axe-core/playwright'],
      error: '@axe-core/playwright nao disponivel',
      duration_ms: Date.now() - start
    };
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ ignoreHTTPSErrors: true });
  const page = await context.newPage();

  try {
    logs.push(`[NAV] Acessando ${url}`);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

    if (actions) {
      await actions(page, logs);
    }

    logs.push('[ANALYSIS] Executando axe-core (WCAG 2.1 AA)');
    const axe = new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa']);

    const axeResults = await axe.analyze();
    violations = axeResults.violations || [];
    passesCount = (axeResults.passes || []).length;

    violations = violations.map(v => {
      const impact = v.impact;
      const isKnownDemo = isDemo && (
        impact === 'critical' || impact === 'serious'
      );
      return {
        rule_id: v.id,
        impact: impact,
        description: v.description,
        affected_elements: (v.nodes || []).map(n => n.html || n.target?.[0] || '').slice(0, 3),
        how_to_fix: v.help,
        help_url: v.helpUrl,
        known_environment_failure: isKnownDemo,
        known_failure_note: isKnownDemo ? 'falha conhecida do ambiente de demonstracao -- nao corrigivel pelo time' : null
      };
    });

    const criticalOrSerious = violations.filter(v => v.impact === 'critical' || v.impact === 'serious');
    const newViolations = criticalOrSerious.filter(v => !v.known_environment_failure);
    const moderateOrMinor = violations.filter(v => v.impact === 'moderate' || v.impact === 'minor');

    for (const v of violations) {
      const known = v.known_environment_failure ? ' (known demo failure)' : '';
      logs.push(`[VIOLATION] ${v.rule_id} (${v.impact}): ${(v.affected_elements || []).length} elementos afetados${known}`);
    }

    if (newViolations.length > 0) {
      status = 'failed';
      deployBlocked = !isDemo;
      logs.push(`[RESULT] ${violations.length} violacoes encontradas (${newViolations.length} novas) -- failed`);
    } else if (moderateOrMinor.length > 0 && criticalOrSerious.length === 0) {
      status = 'warning';
      deployBlocked = false;
      logs.push(`[RESULT] ${moderateOrMinor.length} violacoes moderate/minor -- warning`);
    } else if (criticalOrSerious.length > 0 && criticalOrSerious.every(v => v.known_environment_failure)) {
      status = 'warning';
      deployBlocked = false;
      logs.push(`[RESULT] ${criticalOrSerious.length} violacoes conhecidas do ambiente -- deploy nao bloqueado`);
    } else {
      status = 'passed';
      logs.push(`[RESULT] 0 violacoes -- passed`);
    }

  } catch (e) {
    status = 'error';
    error = e.message || String(e);
    logs.push(`[ERROR] ${error}`);
  } finally {
    await browser.close();
  }

  return {
    id: testId, title, status,
    deploy_blocked: deployBlocked,
    violations, passes_count: passesCount,
    logs, error,
    duration_ms: Date.now() - start
  };
}

async function main() {
  const results = [];

  console.log('TC-A11Y-001: Books homepage...');
  const r1 = await runA11yTest('TC-A11Y-001', 'Homepage Books to Scrape acessibilidade',
    'https://books.toscrape.com');
  results.push(r1);
  console.log(`TC-A11Y-001: ${r1.status} (${(r1.violations || []).length} violacoes)`);

  console.log('TC-A11Y-002: Books categoria Mystery...');
  const r2 = await runA11yTest('TC-A11Y-002', 'Categoria Mystery acessibilidade',
    'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html');
  results.push(r2);
  console.log(`TC-A11Y-002: ${r2.status} (${(r2.violations || []).length} violacoes)`);

  console.log('TC-A11Y-003: The Internet login form...');
  const r3 = await runA11yTest('TC-A11Y-003', 'Formulario login The Internet acessibilidade',
    'https://the-internet.herokuapp.com/login');
  results.push(r3);
  console.log(`TC-A11Y-003: ${r3.status} (${(r3.violations || []).length} violacoes)`);

  console.log('TC-A11Y-004: The Internet login error message...');
  const r4 = await runA11yTest('TC-A11Y-004', 'Mensagem erro login acessivel',
    'https://the-internet.herokuapp.com/login',
    {
      actions: async (page, logs) => {
        await page.locator('#username').fill('wronguser');
        await page.locator('#password').fill('wrongpassword');
        logs.push('[ACTION] Credenciais invalidas preenchidas');
        await page.locator('button[type="submit"]').click();
        logs.push('[ACTION] Login submetido');
        await page.waitForLoadState('domcontentloaded');
        await page.waitForTimeout(500);
        logs.push('[INFO] Aguardando mensagem de erro');
      }
    });
  results.push(r4);
  console.log(`TC-A11Y-004: ${r4.status} (${(r4.violations || []).length} violacoes)`);

  console.log('TC-A11Y-005: AutomationExercise (demo)...');
  const r5 = await runA11yTest('TC-A11Y-005', 'AutomationExercise homepage acessibilidade (demo)',
    'https://automationexercise.com', { isDemo: true });
  results.push(r5);
  console.log(`TC-A11Y-005: ${r5.status} (${(r5.violations || []).length} violacoes)`);

  // Summary
  const passed = results.filter(r => r.status === 'passed').length;
  const failed = results.filter(r => r.status === 'failed').length;
  const warning = results.filter(r => r.status === 'warning').length;
  const skipped = results.filter(r => r.status === 'skipped').length;
  const knownEnvFailures = results.flatMap(r => r.violations || []).filter(v => v.known_environment_failure).length;
  const totalViolations = results.flatMap(r => r.violations || []).length;
  const byCritical = results.flatMap(r => r.violations || []).filter(v => v.impact === 'critical').length;
  const bySerious = results.flatMap(r => r.violations || []).filter(v => v.impact === 'serious').length;
  const byModerate = results.flatMap(r => r.violations || []).filter(v => v.impact === 'moderate').length;
  const byMinor = results.flatMap(r => r.violations || []).filter(v => v.impact === 'minor').length;

  const summary = {
    total: results.length, passed, failed, warning, skipped,
    known_environment_failures: knownEnvFailures,
    total_violations: totalViolations,
    by_impact: { critical: byCritical, serious: bySerious, moderate: byModerate, minor: byMinor }
  };

  const outputJson = {
    executor: 'axe-core',
    environment: 'books.toscrape.com|the-internet.herokuapp.com|automationexercise.com',
    wcag_level: 'wcag2aa',
    generated_files: null,
    results,
    summary
  };

  fs.writeFileSync(path.join(SUITE_DIR, 'acessibilidade', 'resultado.json'), JSON.stringify(outputJson, null, 2));

  const logLines = [`[${ts()}] === executor-acessibilidade -- inicio ===`];
  logLines.push(`[${ts()}] Nivel WCAG: wcag2aa`);
  for (const res of results) {
    logLines.push(`[${ts()}] [${res.id}] ${res.title}`);
    for (const line of (res.logs || [])) {
      logLines.push(`[${ts()}]   ${line}`);
    }
    logLines.push(`[${ts()}]   -> STATUS: ${res.status.toUpperCase()}`);
  }
  logLines.push(`[${ts()}] === Fim: ${passed} passou, ${failed} falhou, ${warning} aviso ===`);
  fs.writeFileSync(path.join(SUITE_DIR, 'acessibilidade', 'execution.log'), logLines.join('\n'));

  console.log(`\n=== A11Y SUMMARY: ${passed} passed, ${failed} failed, ${warning} warning, ${skipped} skipped ===`);
}

main().catch(e => {
  console.error('Fatal:', e);
  process.exit(1);
});
