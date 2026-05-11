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
  reporter: [['json', { outputFile: 'reports/results.json' }], ['list']],
  outputDir: 'reports/test-results',
  globalSetup: './src/support/globalSetup',
  globalTeardown: './src/support/globalTeardown',
  use: {
    ignoreHTTPSErrors: true,
    baseURL: process.env.BASE_URL,
  },
});
