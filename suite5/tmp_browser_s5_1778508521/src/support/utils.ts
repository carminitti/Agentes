import { Page } from '@playwright/test';
import type { TestInfo } from '@playwright/test';

export async function captureScreenshot(page: Page, testInfo: TestInfo): Promise<void> {
  const s = await page.screenshot();
  await testInfo.attach(`screenshot-${Date.now()}`, { body: s, contentType: 'image/png' });
}
