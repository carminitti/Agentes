import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 60_000,
  expect: { timeout: 15_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  testMatch: ['**/*.spec.ts'],
  reporter: [['list'], ['json', { outputFile: 'resultado_raw.json' }]],
  outputDir: 'test-results',
  use: {
    headless: false,
    slowMo: 200,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    screenshot: 'on',
  },
});
