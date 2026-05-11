import { test, expect } from '@playwright/test';

test.describe('Regressão Visual SWAPI @visual', () => {
  test('TC-VIS-001 — Baseline página inicial https://swapi.dev', async ({ page }) => {
    await test.step('Navegar para a página inicial', async () => {
      await page.goto('https://swapi.dev/');
      await page.waitForLoadState('domcontentloaded');
      await page.waitForTimeout(1000);
    });
    await test.step('Capturar screenshot e criar/comparar baseline', async () => {
      await expect(page).toHaveScreenshot('swapi-home.png', { maxDiffPixelRatio: 0.02, animations: 'disabled' });
    });
  });

  test('TC-VIS-002 — Baseline API root https://swapi.dev/api/', async ({ page }) => {
    await test.step('Navegar para /api/', async () => {
      await page.goto('https://swapi.dev/api/');
      await page.waitForLoadState('domcontentloaded');
      await page.waitForTimeout(500);
    });
    await test.step('Capturar screenshot API root', async () => {
      await expect(page).toHaveScreenshot('swapi-api-root.png', { maxDiffPixelRatio: 0.02, animations: 'disabled' });
    });
  });
});
