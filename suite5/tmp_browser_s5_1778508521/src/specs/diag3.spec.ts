import { test, expect } from '../support/fixtures';

test('diag TC-001 - check all nav elements after login', async ({ page }) => {
  page.setDefaultNavigationTimeout(60_000);

  await page.goto('https://practicesoftwaretesting.com/auth/login');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1000);

  await page.locator('[data-test="email"]').or(page.locator('input[type="email"]')).first().fill('customer@practicesoftwaretesting.com');
  await page.locator('[data-test="password"]').or(page.locator('input[type="password"]')).first().fill('welcome01');
  await page.locator('[data-test="login-submit"]').or(page.getByRole('button', { name: /login/i })).first().click();
  await page.waitForURL('**/account', { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(2000);

  console.log('Final URL:', page.url());
  // Check URL includes /account
  const urlOK = page.url().includes('/account');
  console.log('URL includes /account:', urlOK);

  // All data-test elements visible
  const allDataTest = page.locator('[data-test]');
  const count = await allDataTest.count();
  const visible_attrs: string[] = [];
  for (let i = 0; i < Math.min(count, 30); i++) {
    const attr = await allDataTest.nth(i).getAttribute('data-test');
    const vis = await allDataTest.nth(i).isVisible().catch(() => false);
    if (vis) visible_attrs.push(attr || '?');
  }
  console.log('Visible data-test elements:', visible_attrs.join(', '));
  expect(urlOK).toBeTruthy();
});
