import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 60_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  testMatch: ['**/*.spec.ts'],
  reporter: [['json', { outputFile: 'resultado.json' }], ['list']],
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    baseURL: 'https://automationexercise.com',
  },
});
