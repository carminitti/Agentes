import { test, expect } from '../support/fixtures';

test('diag login with network interception', async ({ page }) => {
  page.setDefaultNavigationTimeout(60_000);

  const responses: string[] = [];
  page.on('response', resp => {
    if (resp.url().includes('login') || resp.url().includes('auth') || resp.url().includes('token')) {
      responses.push(`${resp.status()} ${resp.url()}`);
    }
  });

  await page.goto('https://practicesoftwaretesting.com/auth/login');
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1000);

  await page.locator('[data-test="email"]').first().fill('customer@practicesoftwaretesting.com');
  await page.locator('[data-test="password"]').first().fill('welcome01');
  await page.locator('[data-test="login-submit"]').first().click();
  await page.waitForTimeout(5000);

  console.log('Network responses:', responses.join(' | '));

  // Check error text
  const body = await page.locator('body').textContent();
  const errorPatterns = ['Invalid', 'incorrect', 'error', 'wrong', 'failed', 'captcha', 'rate limit'];
  for (const pat of errorPatterns) {
    if (body && body.toLowerCase().includes(pat.toLowerCase())) {
      console.log('Found error pattern in body:', pat);
    }
  }

  // Check the form state
  const emailVal = await page.locator('[data-test="email"]').first().inputValue().catch(() => '');
  console.log('Email field value:', emailVal);
  console.log('Final URL:', page.url());
  expect(true).toBeTruthy();
});
