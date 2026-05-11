import { test, expect } from '../support/fixtures';

test('diag TC-001 flow', async ({ page }) => {
  page.setDefaultNavigationTimeout(60_000);

  await page.goto('https://practicesoftwaretesting.com/');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(2000);

  // Same as TC-001: click Sign In from nav
  const signIn = page.locator('[data-test="nav-sign-in"]');
  if (await signIn.isVisible().catch(() => false)) {
    await signIn.click();
  } else {
    await page.getByRole('link', { name: /sign in/i }).first().click();
  }
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1000);
  console.log('URL on login page:', page.url());

  await page.locator('[data-test="email"]').or(page.locator('input[type="email"]')).first().fill('customer@practicesoftwaretesting.com');
  await page.locator('[data-test="password"]').or(page.locator('input[type="password"]')).first().fill('welcome01');
  await page.locator('[data-test="login-submit"]').or(page.getByRole('button', { name: /login/i })).first().click();
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(2000);

  console.log('URL after login:', page.url());
  console.log('nav-menu visible:', await page.locator('[data-test="nav-menu"]').isVisible().catch(()=>false));
  console.log('nav-user-menu visible:', await page.locator('[data-test="nav-user-menu"]').isVisible().catch(()=>false));
  expect(true).toBeTruthy();
});
