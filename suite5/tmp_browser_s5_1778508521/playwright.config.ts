import { defineConfig } from '@playwright/test';
import * as dotenv from 'dotenv';
dotenv.config();

export default defineConfig({
  timeout: 60_000,
  expect: { timeout: 10_000 },
  fullyParallel: false,
  workers: 1,
  retries: 0,
  testMatch: ['**/*.spec.ts'],
  reporter: [['json', { outputFile: 'resultado_raw.json' }]],
  outputDir: 'reports/test-results',
  globalSetup: './src/support/globalSetup',
  use: {
    headless: process.env.HEADED !== 'true',
    slowMo: process.env.HEADED === 'true' ? 300 : 0,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    baseURL: process.env.BASE_URL,
    trace: 'retain-on-failure',
    screenshot: process.env.HEADED === 'true' ? 'on' : 'only-on-failure',
    video: process.env.HEADED === 'true' ? 'on' : 'retain-on-failure',
  },
});
