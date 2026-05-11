import { defineConfig } from '@playwright/test';
import * as dotenv from 'dotenv';
dotenv.config();

export default defineConfig({
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: true,
  workers: 4,
  retries: 0,
  testMatch: ['**/*.spec.ts'],
  reporter: [['json', { outputFile: 'resultado_raw.json' }]],
  outputDir: 'reports/test-results',
  globalSetup: './src/support/globalSetup',
  use: {
    ignoreHTTPSErrors: true,
    baseURL: process.env.BASE_URL,
  },
});
