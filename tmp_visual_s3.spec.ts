import { test, expect } from '@playwright/test';

test('TC-VISUAL-S3-001 — Regressao visual da pagina inicial de citacoes', async ({ page }) => {
  await page.goto('https://quotes.toscrape.com/');
  await page.waitForSelector('div.quote', { timeout: 15000 });
  await page.evaluate(() => {
    // Ocultar elementos dinamicos que possam causar falso positivo
    const dynamics = document.querySelectorAll('time, .timestamp, [data-timestamp]');
    dynamics.forEach((el) => { (el as HTMLElement).style.visibility = 'hidden'; });
  });
  await expect(page).toHaveScreenshot('quotes-home.png', {
    maxDiffPixelRatio: 0.02,
    animations: 'disabled',
    fullPage: true,
  });
});

test('TC-VISUAL-S3-002 — Regressao visual da pagina de tags populares', async ({ page }) => {
  await page.goto('https://quotes.toscrape.com/tag/love/');
  await page.waitForSelector('div.quote', { timeout: 15000 });
  await page.evaluate(() => {
    // Ocultar elementos dinamicos de data
    const dynamics = document.querySelectorAll('time, .timestamp, [data-timestamp], .date, span[class*="date"]');
    dynamics.forEach((el) => { (el as HTMLElement).style.visibility = 'hidden'; });
  });
  const mainContent = page.locator('div.col-md-8');
  await expect(mainContent).toHaveScreenshot('quotes-love-tag.png', {
    maxDiffPixelRatio: 0.02,
    animations: 'disabled',
  });
});
