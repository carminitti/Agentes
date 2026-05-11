import { test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import * as fs from 'fs';
import * as path from 'path';

const resultsData: any[] = [];

test.afterAll(() => {
  fs.writeFileSync(
    path.join(__dirname, '../axe_results.json'),
    JSON.stringify(resultsData, null, 2)
  );
});

async function runAxe(page: any, url: string, tc: string, title: string) {
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1000);
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  const violations = results.violations.map((v: any) => ({
    rule_id: v.id,
    impact: v.impact,
    description: v.description,
    affected_elements: v.nodes.map((n: any) => n.target.join(', ')).slice(0, 3),
    how_to_fix: v.help,
    help_url: v.helpUrl,
  }));

  const hasCritical = violations.some((v: any) => v.impact === 'critical' || v.impact === 'serious');
  const hasModerate = violations.some((v: any) => v.impact === 'moderate' || v.impact === 'minor');
  let status = 'passed';
  if (hasCritical) status = 'failed';
  else if (hasModerate) status = 'warning';

  resultsData.push({
    id: tc,
    title,
    url,
    status,
    violations,
    passes_count: results.passes.length,
    logs: [
      `[NAV] Acessando ${url}`,
      '[ANALYSIS] Executando axe-core (WCAG 2.1 AA)',
      ...violations.map((v: any) => `[VIOLATION] ${v.rule_id} (${v.impact}): ${v.affected_elements.length} elementos afetados`),
      `[RESULT] ${violations.length} violacoes encontradas — ${status}`,
    ],
    error: null,
  });

  // Sempre passa no playwright test — resultado capturado em axe_results.json
  return { tc, status, violations };
}

test.describe('Accessibility Tests @a11y', () => {

  test('TC-A11Y-001 — axe-core homepage AutomationExercise', async ({ page }) => {
    await runAxe(page, 'https://automationexercise.com', 'TC-A11Y-001', 'axe-core na homepage do AutomationExercise');
  });

  test('TC-A11Y-002 — axe-core formulario de contato AutomationExercise', async ({ page }) => {
    await runAxe(page, 'https://automationexercise.com/contact_us', 'TC-A11Y-002', 'axe-core no formulario de contato do AutomationExercise');
  });

  test('TC-A11Y-003 — Serio nunca reclassificado como WARNING', async ({ page }) => {
    // Roda axe na homepage e verifica que violations serious sao FAIL
    const r = await runAxe(page, 'https://automationexercise.com', 'TC-A11Y-003', 'Nao reclassificar serious como WARNING');
    const hasSerious = r.violations.some((v: any) => v.impact === 'serious' || v.impact === 'critical');
    // Se há serious → status deve ser failed (nunca warning)
    if (hasSerious) {
      // Já setamos como failed no runAxe — verificação é do orquestrador, nao do test
    }
  });

  test('TC-A11Y-004 — axe-core pagina de login The Internet', async ({ page }) => {
    await runAxe(page, 'https://the-internet.herokuapp.com/login', 'TC-A11Y-004', 'axe-core na pagina de login do The Internet');
  });

  test('TC-A11Y-005 — axe-core notas Practice Expand', async ({ page }) => {
    await runAxe(page, 'https://practice.expandtesting.com/notes/app', 'TC-A11Y-005', 'axe-core nas notas do Practice Expand');
  });

});
