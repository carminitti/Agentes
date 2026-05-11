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
  reporter: [['json', { outputFile: 'results.json' }]],
  outputDir: 'reports/test-results',
  globalSetup: './src/support/globalSetup',
  use: {
    ignoreHTTPSErrors: true,
  },
});
