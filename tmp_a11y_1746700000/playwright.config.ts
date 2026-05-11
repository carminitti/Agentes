import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: '.',
  timeout: 60000,
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
  },
  reporter: [['list']],
});
