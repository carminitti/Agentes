import { test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import * as fs from 'fs';

test('TC-A11Y-001 - Acessibilidade da página inicial (WCAG 2.1 AA)', async ({ page }) => {
  console.log('[NAV] Acessando https://automationexercise.com');
  await page.goto('https://automationexercise.com', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(2000);

  console.log('[ANALYSIS] Executando axe-core (WCAG 2.1 AA)');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
    .analyze();

  const output = {
    violations: results.violations,
    passes_count: results.passes.length,
    incomplete_count: results.incomplete.length
  };

  fs.writeFileSync('tmp_a11y_1746700000/results.json', JSON.stringify(output, null, 2));
  console.log('[RESULT] violations=' + results.violations.length + ' passes=' + results.passes.length);
  console.log('VIOLATIONS_JSON=' + JSON.stringify(results.violations));
});
