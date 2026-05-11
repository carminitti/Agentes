import { test, expect } from '@playwright/test';

test.describe('Visual Regression Suite 5', () => {

  test('TC-VISUAL-S5-001 - Regressao visual da pagina de checklist do A11Y Project', async ({ page }) => {
    page.setDefaultNavigationTimeout(60_000);
    page.setDefaultTimeout(30_000);

    await page.goto('https://www.a11yproject.com/checklist/');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForSelector('main', { timeout: 20_000 });

    // Oculta elementos dinamicos (datas, contadores) que causam falso positivo
    await page.evaluate(() => {
      // Oculta elementos com data/hora dinamica
      const dateSelectors = [
        'time', '[data-date]', '.date', '.timestamp',
        '[class*="date"]', '[class*="time"]', '[class*="counter"]'
      ];
      dateSelectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(el => {
          (el as HTMLElement).style.visibility = 'hidden';
        });
      });
    });

    // Aguarda render estavel
    await page.waitForTimeout(1000);

    // Captura apenas o elemento main (area de conteudo principal)
    const mainContent = page.locator('main');
    await expect(mainContent).toHaveScreenshot('a11y-checklist.png', {
      maxDiffPixelRatio: 0.02,
      animations: 'disabled',
    });
  });

  test('TC-VISUAL-S5-002 - Regressao visual da pagina de recursos do WebAIM', async ({ page }) => {
    page.setDefaultNavigationTimeout(60_000);
    page.setDefaultTimeout(30_000);

    await page.goto('https://webaim.org/resources/');
    await page.waitForLoadState('domcontentloaded');

    // Aguarda main ou article estar visivel
    await page.waitForSelector('main, article', { timeout: 20_000 });

    // Aguarda render estavel
    await page.waitForTimeout(1000);

    // Captura pagina completa
    await expect(page).toHaveScreenshot('webaim-resources.png', {
      maxDiffPixelRatio: 0.02,
      animations: 'disabled',
      fullPage: true,
    });
  });

});
