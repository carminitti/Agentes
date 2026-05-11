import { test, expect } from '../support/fixtures';

test('diag TC-001 full login trace', async ({ page }) => {
  page.setDefaultNavigationTimeout(60_000);

  await page.goto('https://practicesoftwaretesting.com/');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(2000);

  await page.locator('[data-test="nav-sign-in"]').click();
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1000);
  console.log('On login page:', page.url());

  const emailInput = page.locator('[data-test="email"]').or(page.locator('input[type="email"]'));
  const passwordInput = page.locator('[data-test="password"]').or(page.locator('input[type="password"]'));
  const loginBtn = page.locator('[data-test="login-submit"]').or(page.getByRole('button', { name: /login|sign in/i }));

  await emailInput.first().fill('customer@practicesoftwaretesting.com');
  await passwordInput.first().fill('welcome01');
  console.log('Credentials filled. Clicking login...');
  await loginBtn.first().click();

  // Wait a bit
  await page.waitForTimeout(4000);
  console.log('URL after click+4s:', page.url());

  // Check for error messages
  const errorMsg = page.locator('[data-test="login-error"], .alert-danger, .error-message, [class*="error"]');
  const hasError = await errorMsg.first().isVisible().catch(() => false);
  if (hasError) {
    const errText = await errorMsg.first().textContent();
    console.log('Error message:', errText);
  }

  console.log('nav-menu visible:', await page.locator('[data-test="nav-menu"]').isVisible().catch(()=>false));
  console.log('Page title:', await page.title());
  expect(true).toBeTruthy();
});
