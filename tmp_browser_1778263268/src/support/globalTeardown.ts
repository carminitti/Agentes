import { FullConfig } from '@playwright/test';

export default async function globalTeardown(_config: FullConfig): Promise<void> {
  // Limpeza global pós-suite: fechar conexões, enviar notificações
}
