import { Page, Locator } from '@playwright/test';

export class SwapiHomePage {
  get body(): Locator { return this.page.locator('body'); }
  get heading(): Locator { return this.page.getByRole('heading').first(); }

  constructor(public page: Page) {}

  async navigate(): Promise<void> {
    await this.page.goto('https://swapi.dev/');
    await this.page.waitForLoadState('domcontentloaded');
  }
}
