import { defineConfig } from '@playwright/test';
import * as dotenv from 'dotenv';
dotenv.config();

export default defineConfig({
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: true,
  workers: 4,
  retries: process.env.CI ? 2 : 0,
  testMatch: ['**/*.spec.ts'],
  reporter: [['html', { outputFolder: 'reports/html', open: 'never' }], ['json', { outputFile: 'resultado.json' }]],
  outputDir: 'reports/test-results',
  globalSetup: './src/support/globalSetup',
  globalTeardown: './src/support/globalTeardown',
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    baseURL: process.env.BASE_URL,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
});
