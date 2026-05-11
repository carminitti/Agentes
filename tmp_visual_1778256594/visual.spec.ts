import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const baselineDir = path.join(__dirname, 'baselines');
fs.mkdirSync(baselineDir, { recursive: true });

test.describe('Visual Regression Tests @visual', () => {

  test('TC-VIS-001 — Baseline homepage AutomationExercise', async ({ page }) => {
    await page.goto('https://automationexercise.com', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1500);
    // Ocultar elementos dinamicos (banners, timers)
    await page.evaluate(() => {
      document.querySelectorAll('[id*="timer"], [class*="countdown"], [class*="timer"]').forEach((el: any) => {
        el.style.visibility = 'hidden';
      });
    });
    await expect(page).toHaveScreenshot('automationexercise_home_baseline.png', {
      maxDiffPixelRatio: 0.02,
      animations: 'disabled',
      fullPage: true,
    });
  });

  test('TC-VIS-002 — Baseline pagina de produtos AutomationExercise', async ({ page }) => {
    await page.goto('https://automationexercise.com/products', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);
    await expect(page).toHaveScreenshot('automationexercise_products_baseline.png', {
      maxDiffPixelRatio: 0.02,
      animations: 'disabled',
      fullPage: true,
    });
  });

  test('TC-VIS-003 — Comparacao visual homepage dentro do threshold', async ({ page }) => {
    await page.goto('https://automationexercise.com', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1500);
    await page.evaluate(() => {
      document.querySelectorAll('[id*="timer"], [class*="countdown"], [class*="timer"]').forEach((el: any) => {
        el.style.visibility = 'hidden';
      });
    });
    await expect(page).toHaveScreenshot('automationexercise_home_baseline.png', {
      maxDiffPixelRatio: 0.02,
      animations: 'disabled',
      fullPage: true,
    });
  });

  test('TC-VIS-004 — Comparacao visual produtos (pode ter regressao)', async ({ page }) => {
    await page.goto('https://automationexercise.com/products', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);
    await expect(page).toHaveScreenshot('automationexercise_products_baseline.png', {
      maxDiffPixelRatio: 0.02,
      animations: 'disabled',
      fullPage: true,
    });
  });

  test('TC-VIS-005 — Baseline pagina de login Practice Expand', async ({ page }) => {
    await page.goto('https://practice.expandtesting.com/notes/app/login', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);
    await expect(page).toHaveScreenshot('expandtesting_login_baseline.png', {
      maxDiffPixelRatio: 0.02,
      animations: 'disabled',
    });
  });

  test('TC-VIS-006 — Baseline dashboard Practice Expand apos login', async ({ page }) => {
    await page.goto('https://practice.expandtesting.com/notes/app/login', { waitUntil: 'domcontentloaded' });
    await page.getByPlaceholder(/email/i).fill('qa_agente_v3@test.com');
    await page.getByPlaceholder(/password/i).fill('Test@1234');
    await page.getByRole('button', { name: /login/i }).click();
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(2000);
    await expect(page).toHaveScreenshot('expandtesting_dashboard_baseline.png', {
      maxDiffPixelRatio: 0.03,
      animations: 'disabled',
    });
  });

});
