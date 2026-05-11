import { test, expect } from '../support/fixtures';

test('diagnose login page elements', async ({ page }) => {
  page.setDefaultNavigationTimeout(60_000);

  await page.goto('https://practicesoftwaretesting.com/');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(2000);

  // Click sign in
  const signIn = page.locator('[data-test="nav-sign-in"]');
  if (await signIn.isVisible().catch(() => false)) {
    await signIn.click();
  } else {
    const link = page.getByRole('link', { name: /sign in/i });
    await link.first().click();
  }
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1000);

  // Fill credentials
  await page.locator('[data-test="email"]').or(page.locator('input[type="email"]')).first().fill('customer@practicesoftwaretesting.com');
  await page.locator('[data-test="password"]').or(page.locator('input[type="password"]')).first().fill('welcome01');
  await page.locator('[data-test="login-submit"]').or(page.getByRole('button', { name: /login/i })).first().click();
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(3000);

  const url = page.url();
  const title = await page.title();
  console.log('URL after login:', url);
  console.log('Title:', title);

  const selectors = [
    '[data-test="nav-user-menu"]',
    '[data-test="nav-menu"]',
    '.navbar .dropdown',
    'nav .dropdown-toggle',
    'a[href*="account"]',
    '.customer-name',
    'span.navbar-text',
  ];

  for (const sel of selectors) {
    const el = page.locator(sel);
    const visible = await el.isVisible().catch(() => false);
    if (visible) {
      const text = await el.first().textContent().catch(() => '');
      console.log(`VISIBLE: ${sel} = "${text?.trim().slice(0,80)}"`);
    } else {
      console.log(`NOT_VISIBLE: ${sel}`);
    }
  }

  // Take screenshot for manual inspection
  await page.screenshot({ path: 'diag_after_login.png' });
  expect(url).toBeTruthy();
});
