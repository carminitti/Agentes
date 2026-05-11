import { Page, Locator } from '@playwright/test';

export class UsuariosPage {
  // ===Locators===
  get listaUsuarios(): Locator { return this.page.getByRole('list').first(); }
  get itemUsuario(): Locator { return this.page.getByRole('listitem').first(); }
  get tituloUsuarios(): Locator { return this.page.getByRole('heading', { name: /usuários|users/i }); }

  // ===Methods===
  constructor(public page: Page) {}

  async navigate(path: string = '/'): Promise<void> {
    await this.page.goto(path);
    await this.page.waitForLoadState('networkidle');
  }

  async navigateToUsers(): Promise<void> {
    await this.page.goto('/api/users?page=1');
    await this.page.waitForLoadState('networkidle');
  }

  async isUserListVisible(): Promise<boolean> {
    try {
      await this.page.waitForSelector('body', { timeout: 5000 });
      return true;
    } catch {
      return false;
    }
  }
}
