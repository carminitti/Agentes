import { Page } from '@playwright/test';
import type { TestInfo } from '@playwright/test';
import { faker } from '@faker-js/faker';

export async function captureScreenshot(page: Page, testInfo: TestInfo): Promise<void> {
  const screenshot = await page.screenshot();
  await testInfo.attach(`screenshot-${Date.now()}`, { body: screenshot, contentType: 'image/png' });
}

export function generateTestData(): { name: string; code: string; price: string } {
  const letter = faker.string.alpha({ length: 1, casing: 'upper' });
  const digits = faker.string.numeric(3);
  return {
    name: faker.commerce.productName(),
    code: `${letter}${digits}`,
    price: faker.number.int({ min: 10, max: 500 }).toString(),
  };
}
