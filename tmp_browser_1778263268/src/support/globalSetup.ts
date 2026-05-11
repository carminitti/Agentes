import { request, FullConfig } from '@playwright/test';
import * as fs from 'fs';

export default async function globalSetup(config: FullConfig): Promise<void> {
  fs.mkdirSync('reports', { recursive: true });

  // Auto-geração de token com fallback de auto-registro
  // Fluxo: tenta login → se falhar (usuário não existe), registra → tenta login novamente
  if (process.env.USER_EMAIL && process.env.USER_PASSWORD && !process.env.AUTH_TOKEN) {
    const apiCtx = await request.newContext({ baseURL: process.env.BASE_URL });
    const authEndpoints = ['/auth/login', '/api/auth/login', '/api/login', '/login', '/oauth/token'];

    const tryLogin = async (): Promise<boolean> => {
      for (const endpoint of authEndpoints) {
        try {
          const resp = await apiCtx.post(endpoint, {
            data: { email: process.env.USER_EMAIL, password: process.env.USER_PASSWORD },
          });
          if (resp.ok()) {
            const body = await resp.json();
            const token = body.access_token || body.token || body.accessToken || body.jwt || body.authToken;
            if (token) { process.env.AUTH_TOKEN = token; return true; }
          }
        } catch {}
      }
      return false;
    };

    const tokenAcquired = await tryLogin();

    // Login falhou — usuário provavelmente não existe; tenta registrar e refaz login
    // REGRA: nunca use credenciais de fallback. Se o registro falhar, os cenários que
    // dependem de autenticação devem ser marcados como FAIL com causa "falha no setup —
    // registro não concluído". Não prossiga com o login usando outra conta.
    if (!tokenAcquired) {
      const registerEndpoints = [
        '/api/register', '/api/auth/register', '/register',
        '/signup', '/api/signup', '/auth/register', '/api/v1/register',
      ];
      let registered = false;
      for (const endpoint of registerEndpoints) {
        try {
          const resp = await apiCtx.post(endpoint, {
            data: {
              name: process.env.USER_NAME || 'QA Test User',
              email: process.env.USER_EMAIL,
              password: process.env.USER_PASSWORD,
            },
          });
          if (resp.status() === 200 || resp.status() === 201) {
            registered = true;
            await tryLogin();
            break;
          }
        } catch {}
      }
      // Se o registro falhou em todos os endpoints, sinaliza para os specs falharem
      if (!registered) {
        process.env.SETUP_FAILED = 'Registro não concluído — nenhum endpoint de registro respondeu com sucesso. Marque cenários de login como FAIL com causa: falha no setup — registro não concluído.';
      }
    }

    await apiCtx.dispose();
  }
}
