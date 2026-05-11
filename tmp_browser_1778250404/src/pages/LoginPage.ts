import { Page, Locator } from '@playwright/test';

export class LoginPage {
  // ===Locators===
  get formLogin(): Locator { return this.page.locator('div.login-form'); }
  get loginForm(): Locator { return this.page.locator('div.login-form'); }
  get inputEmail(): Locator { return this.page.locator('[data-qa="login-email"]'); }
  get inputPassword(): Locator { return this.page.locator('[data-qa="login-password"]'); }
  get btnLogin(): Locator { return this.page.locator('[data-qa="login-button"]'); }
  get errorMessage(): Locator { return this.page.getByText(/your email or password is incorrect/i); }
  get loggedInAs(): Locator { return this.page.getByText(/logged in as/i); }

  // ===Methods===
  constructor(private page: Page) {}

  async navigate(): Promise<void> {
    await this.page.goto('/login');
    await this.page.waitForLoadState('domcontentloaded');
  }

  async login(email: string, password: string): Promise<void> {
    await this.inputEmail.fill(email);
    await this.inputPassword.fill(password);
    await this.btnLogin.click();
  }
}
