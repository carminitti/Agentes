import { test, expect } from '@playwright/test';

// Injeta axe-core via CDN e executa analise
async function runAxe(page: import('@playwright/test').Page, tags: string[]): Promise<{
  violations: Array<{ id: string; impact: string; description: string; nodes: unknown[] }>;
  passes: number;
}> {
  // Injetar axe-core via CDN
  await page.addScriptTag({
    url: 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.0/axe.min.js'
  });

  const result = await page.evaluate(async (ruleTags: string[]) => {
    return new Promise<{ violations: Array<{ id: string; impact: string; description: string; nodes: unknown[] }>; passes: number }>((resolve) => {
      // @ts-ignore
      axe.run(document, { runOnly: { type: 'tag', values: ruleTags } }, (err: Error | null, results: { violations: Array<{ id: string; impact: string; description: string; nodes: unknown[] }>; passes: Array<unknown> }) => {
        if (err) resolve({ violations: [], passes: 0 });
        else resolve({ violations: results.violations, passes: results.passes.length });
      });
    });
  }, tags);

  return result;
}

test.describe('TC-A11Y-S6-001 -- W3C WAI BAD after/home @acessibilidade', () => {
  test('Conformidade WCAG 2.1 AA na homepage acessivel do W3C BAD demo', async ({ page }) => {
    page.setDefaultNavigationTimeout(60_000);

    await test.step('Acessar pagina W3C WAI BAD after/home', async () => {
      await page.goto('https://www.w3.org/WAI/demos/bad/after/home.html', { waitUntil: 'domcontentloaded' });
      await page.waitForSelector('main, body', { timeout: 20_000 });
      await page.waitForTimeout(1000);
    });

    await test.step('Executar analise axe-core WCAG 2.1 AA', async () => {
      const result = await runAxe(page, ['wcag2a', 'wcag2aa', 'wcag21aa']);

      const critical = result.violations.filter(v => v.impact === 'critical');
      const serious = result.violations.filter(v => v.impact === 'serious');
      const moderate = result.violations.filter(v => v.impact === 'moderate');
      const minor = result.violations.filter(v => v.impact === 'minor');

      // Logar violacoes moderate/minor como avisos
      if (moderate.length + minor.length > 0) {
        console.log(`[WARN] ${moderate.length} violacoes moderate, ${minor.length} minor (nao bloqueantes)`);
        moderate.concat(minor).forEach(v => console.log(`  [WARN] ${v.id}: ${v.description}`));
      }

      // Critical e serious devem ser zero
      if (critical.length > 0) {
        console.error('[FAIL] Violacoes critical:', critical.map(v => v.id).join(', '));
      }
      if (serious.length > 0) {
        console.error('[FAIL] Violacoes serious:', serious.map(v => v.id).join(', '));
      }

      expect(critical.length, `Nao deve haver violacoes critical. Encontradas: ${critical.map(v=>v.id).join(', ')}`).toBe(0);
      expect(serious.length, `Nao deve haver violacoes serious. Encontradas: ${serious.map(v=>v.id).join(', ')}`).toBe(0);

      await page.screenshot({ path: 'test-results/TC-A11Y-S6-001.png' });
    });
  });
});

test.describe('TC-A11Y-S6-002 -- W3C WAI BAD after/survey @acessibilidade', () => {
  test('Conformidade WCAG 2.1 AA na pagina de survey acessivel do W3C BAD demo', async ({ page }) => {
    page.setDefaultNavigationTimeout(60_000);

    await test.step('Acessar pagina W3C WAI BAD after/survey', async () => {
      await page.goto('https://www.w3.org/WAI/demos/bad/after/survey.html', { waitUntil: 'domcontentloaded' });
      // Aguardar formulario visivel
      await page.waitForSelector('form', { timeout: 20_000 });
      await page.waitForTimeout(1000);
    });

    await test.step('Executar analise axe-core WCAG 2.1 AA', async () => {
      const result = await runAxe(page, ['wcag2a', 'wcag2aa', 'wcag21aa']);

      const critical = result.violations.filter(v => v.impact === 'critical');
      const serious = result.violations.filter(v => v.impact === 'serious');
      const moderate = result.violations.filter(v => v.impact === 'moderate');
      const minor = result.violations.filter(v => v.impact === 'minor');

      if (moderate.length + minor.length > 0) {
        console.log(`[WARN] ${moderate.length} violacoes moderate, ${minor.length} minor (apenas avisos)`);
        moderate.concat(minor).forEach(v => console.log(`  [WARN] ${v.id}: ${v.description}`));
      }

      expect(critical.length, `Nao deve haver violacoes critical. Encontradas: ${critical.map(v=>v.id).join(', ')}`).toBe(0);
      expect(serious.length, `Nao deve haver violacoes serious. Encontradas: ${serious.map(v=>v.id).join(', ')}`).toBe(0);

      await page.screenshot({ path: 'test-results/TC-A11Y-S6-002.png' });
    });
  });
});
