import { test, expect } from '../../support/fixtures';

let authToken: string = '';

test.describe('Practice Expand API @api', () => {

  test('TC-API-011 — Health check da API de notas', async ({ expandApi }) => {
    let response: Awaited<ReturnType<typeof expandApi.get>>;

    await test.step('GET /health-check', async () => {
      response = await expandApi.get('/health-check');
    });

    await test.step('Validar health check', async () => {
      expect(response!.status()).toBe(200);
      const data = await response!.json();
      expect(data.message).toBe('Notes API is Running');
    });
  });

  test('TC-API-012 — Registrar usuário no Practice Expand', async ({ expandApi }) => {
    let response: Awaited<ReturnType<typeof expandApi.post>>;

    await test.step('POST /users/register', async () => {
      response = await expandApi.post('/users/register', {
        data: {
          name: 'QA Agente',
          email: 'qa_agente_v3@test.com',
          password: 'Test@1234',
        },
      });
    });

    await test.step('Validar registro ou usuário já existente', async () => {
      // 201 = criado com sucesso; 409 = usuário já existe (aceitável em re-execução)
      expect([200, 201, 409]).toContain(response!.status());
      if (response!.status() === 201) {
        const data = await response!.json();
        expect(data.data.name).toBe('QA Agente');
        expect(data.data.email).toBe('qa_agente_v3@test.com');
      }
    });
  });

  test('TC-API-013 — Login e obter token no Practice Expand', async ({ expandApi }) => {
    let response: Awaited<ReturnType<typeof expandApi.post>>;

    await test.step('POST /users/login', async () => {
      response = await expandApi.post('/users/login', {
        data: {
          email: 'qa_agente_v3@test.com',
          password: 'Test@1234',
        },
      });
    });

    await test.step('Validar token obtido', async () => {
      expect(response!.status()).toBe(200);
      const data = await response!.json();
      expect(data.data.token).toBeTruthy();
      expect(data.data.token.length).toBeGreaterThan(0);
      authToken = data.data.token;
      process.env['EXPAND_AUTH_TOKEN'] = authToken;
    });
  });

  test('TC-API-014 — Criar nota autenticada no Practice Expand', async ({ expandApi }) => {
    let loginResp: Awaited<ReturnType<typeof expandApi.post>>;
    let noteResp: Awaited<ReturnType<typeof expandApi.post>>;
    let token: string;

    await test.step('Obter token via login', async () => {
      loginResp = await expandApi.post('/users/login', {
        data: { email: 'qa_agente_v3@test.com', password: 'Test@1234' },
      });
      expect(loginResp.status()).toBe(200);
      const loginData = await loginResp.json();
      token = loginData.data.token;
    });

    await test.step('POST /notes com token', async () => {
      noteResp = await expandApi.post('/notes', {
        headers: { 'x-auth-token': token },
        data: {
          title: 'Nota do QA Agente',
          description: 'Criada pelo executor-api v3',
          category: 'Work',
        },
      });
    });

    await test.step('Validar nota criada', async () => {
      expect(noteResp!.status()).toBe(200);
      const data = await noteResp!.json();
      expect(data.data.title).toBe('Nota do QA Agente');
      expect(data.data.category).toBe('Work');
    });
  });

  test('TC-API-015 — Listar notas autenticado no Practice Expand', async ({ expandApi }) => {
    let loginResp: Awaited<ReturnType<typeof expandApi.post>>;
    let notesResp: Awaited<ReturnType<typeof expandApi.get>>;
    let token: string;

    await test.step('Obter token via login', async () => {
      loginResp = await expandApi.post('/users/login', {
        data: { email: 'qa_agente_v3@test.com', password: 'Test@1234' },
      });
      expect(loginResp.status()).toBe(200);
      const loginData = await loginResp.json();
      token = loginData.data.token;
    });

    await test.step('GET /notes com token', async () => {
      notesResp = await expandApi.get('/notes', {
        headers: { 'x-auth-token': token },
      });
    });

    await test.step('Validar lista de notas', async () => {
      expect(notesResp!.status()).toBe(200);
      const data = await notesResp!.json();
      expect(Array.isArray(data.data)).toBeTruthy();
      if (data.data.length > 0) {
        const note = data.data[0];
        expect(typeof note.id).toBe('string');
        expect(typeof note.title).toBe('string');
        expect(typeof note.description).toBe('string');
        expect(typeof note.category).toBe('string');
      }
    });
  });

  test('TC-API-016 — Tentar criar nota sem autenticação retorna 401', async ({ expandApi }) => {
    let response: Awaited<ReturnType<typeof expandApi.post>>;

    await test.step('POST /notes sem x-auth-token', async () => {
      response = await expandApi.post('/notes', {
        data: {
          title: 'Nota sem auth',
          description: 'Não deve ser criada',
          category: 'Home',
        },
      });
    });

    await test.step('Validar 401', async () => {
      expect(response!.status()).toBe(401);
    });
  });

});
