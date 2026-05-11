import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 60_000,
  expect: { timeout: 30_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  testMatch: ['**/*.spec.ts'],
  reporter: [['list']],
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
  },
});
