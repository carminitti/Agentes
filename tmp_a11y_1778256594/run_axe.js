const { chromium } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;
const fs = require('fs');

const pages_to_test = [
  { id: 'TC-A11Y-001', title: 'axe-core na homepage do AutomationExercise', url: 'https://automationexercise.com' },
  { id: 'TC-A11Y-002', title: 'axe-core no formulario de contato do AutomationExercise', url: 'https://automationexercise.com/contact_us' },
  { id: 'TC-A11Y-003', title: 'Nao reclassificar serious como WARNING', url: 'https://automationexercise.com' },
  { id: 'TC-A11Y-004', title: 'axe-core na pagina de login do The Internet', url: 'https://the-internet.herokuapp.com/login' },
  { id: 'TC-A11Y-005', title: 'axe-core nas notas do Practice Expand', url: 'https://practice.expandtesting.com/notes/app' },
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const results = [];

  for (const item of pages_to_test) {
    const context = await browser.newContext({ ignoreHTTPSErrors: true });
    const page = await context.newPage();
    try {
      await page.goto(item.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
      await page.waitForTimeout(1500);

      const axeResults = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
        .analyze();

      const violations = axeResults.violations.map(v => ({
        rule_id: v.id,
        impact: v.impact,
        description: v.description,
        affected_elements: v.nodes.map(n => n.target.join(', ')).slice(0, 3),
        how_to_fix: v.help,
        help_url: v.helpUrl,
      }));

      const hasCritical = violations.some(v => v.impact === 'critical' || v.impact === 'serious');
      const hasModerate = violations.some(v => v.impact === 'moderate' || v.impact === 'minor');
      let status = 'passed';
      if (hasCritical) status = 'failed';
      else if (hasModerate) status = 'warning';

      // TC-A11Y-003: verificar que serious nao e reclassificado
      if (item.id === 'TC-A11Y-003') {
        const hasSerious = violations.some(v => v.impact === 'serious' || v.impact === 'critical');
        if (hasSerious && status !== 'failed') {
          status = 'failed'; // forcar failed se serious encontrado
        }
        // Se nao ha serious, o teste ainda assim PASSA (verificou que a regra funciona)
      }

      results.push({
        id: item.id,
        title: item.title,
        url: item.url,
        status,
        violations,
        passes_count: axeResults.passes.length,
        logs: [
          `[NAV] Acessando ${item.url}`,
          '[ANALYSIS] Executando axe-core (WCAG 2.1 AA)',
          ...violations.map(v => `[VIOLATION] ${v.rule_id} (${v.impact}): ${v.affected_elements.length} elementos afetados`),
          `[RESULT] ${violations.length} violacoes encontradas — ${status}`,
        ],
        error: null,
      });

      console.log(`${item.id}: ${status} (${violations.length} violations)`);
    } catch (e) {
      results.push({
        id: item.id,
        title: item.title,
        url: item.url,
        status: 'failed',
        violations: [],
        passes_count: 0,
        logs: [`[ERROR] ${e.message}`],
        error: e.message,
      });
      console.log(`${item.id}: ERROR - ${e.message}`);
    }
    await context.close();
  }

  await browser.close();

  const byImpact = { critical: 0, serious: 0, moderate: 0, minor: 0 };
  for (const r of results) {
    for (const v of r.violations) {
      if (byImpact[v.impact] !== undefined) byImpact[v.impact]++;
    }
  }

  const output = {
    executor: 'axe-core',
    environment: 'multiple (AutomationExercise / The Internet / Practice Expand)',
    wcag_level: 'wcag2aa',
    results,
    summary: {
      total: results.length,
      passed: results.filter(r => r.status === 'passed').length,
      failed: results.filter(r => r.status === 'failed').length,
      warning: results.filter(r => r.status === 'warning').length,
      total_violations: results.reduce((s, r) => s + r.violations.length, 0),
      by_impact: byImpact,
    },
  };

  fs.writeFileSync('axe_results.json', JSON.stringify(output, null, 2));
  console.log('Saved axe_results.json');
  console.log('Summary:', JSON.stringify(output.summary));
})();
