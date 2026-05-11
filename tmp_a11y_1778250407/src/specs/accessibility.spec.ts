import { test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import * as fs from 'fs';

// TC-CL-006: Acessibilidade — página de login, WCAG 2.1 AA
test('TC-CL-006 — Verificar acessibilidade da página de login (WCAG 2.1 AA)', async ({ page }) => {
  await test.step('Acessar página de login', async () => {
    await page.goto('https://automationexercise.com/login');
    await page.waitForLoadState('networkidle');
  });

  await test.step('Executar análise axe-core (WCAG 2.1 AA)', async () => {
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();

    // Salva resultado completo para parse posterior
    fs.writeFileSync('axe_result.json', JSON.stringify(results, null, 2));

    // Loga resumo
    console.log(`Violações encontradas: ${results.violations.length}`);
    results.violations.forEach(v => {
      console.log(`[VIOLATION] ${v.id} (${v.impact}): ${v.nodes.length} elemento(s) afetado(s)`);
    });
    console.log(`Regras aprovadas: ${results.passes.length}`);
  });
});
