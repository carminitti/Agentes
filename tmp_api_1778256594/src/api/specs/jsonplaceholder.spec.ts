import { test, expect } from '../../support/fixtures';
import { postSchema, userSchema, todoSchema } from '../schemas/jsonplaceholder.schema';

test.describe('JSONPlaceholder API @api', () => {

  test('TC-API-001 — Listar todos os posts e validar contagem', async ({ jsonApi }) => {
    let response: Awaited<ReturnType<typeof jsonApi.get>>;

    await test.step('Requisitar lista de posts', async () => {
      response = await jsonApi.get('/posts');
    });

    await test.step('Validar resposta', async () => {
      expect(response!.status()).toBe(200);
      expect(response!.ok()).toBeTruthy();
      const data = await response!.json();
      expect(Array.isArray(data), 'deve ser array').toBeTruthy();
      expect(data.length).toBe(100);
      expect(data[0].id).toBe(1);
      expect(data[0].userId).toBe(1);
      for (const item of data) {
        expect(typeof item.id).toBe('number');
        expect(typeof item.userId).toBe('number');
        expect(typeof item.title).toBe('string');
        expect(typeof item.body).toBe('string');
      }
    });
  });

  test('TC-API-002 — Buscar post específico pelo ID 1', async ({ jsonApi }) => {
    let response: Awaited<ReturnType<typeof jsonApi.get>>;

    await test.step('Requisitar post ID 1', async () => {
      response = await jsonApi.get('/posts/1');
    });

    await test.step('Validar campos do post', async () => {
      expect(response!.status()).toBe(200);
      const data = await response!.json();
      expect(data.id).toBe(1);
      expect(data.userId).toBe(1);
      expect(data.title).toBe('sunt aut facere repellat provident occaecati excepturi optio reprehenderit');
      expect(data.body).toBeTruthy();
      expect(data.body.length).toBeGreaterThan(0);
    });
  });

  test('TC-API-003 — Criar novo post via POST', async ({ jsonApi }) => {
    let response: Awaited<ReturnType<typeof jsonApi.post>>;

    await test.step('Criar post', async () => {
      response = await jsonApi.post('/posts', {
        data: { title: 'QA Agente Post', body: 'Criado pelo executor-api', userId: 1 },
      });
    });

    await test.step('Validar criação', async () => {
      expect(response!.status()).toBe(201);
      const data = await response!.json();
      expect(data.id).toBe(101);
      expect(data.title).toBe('QA Agente Post');
      expect(data.userId).toBe(1);
    });
  });

  test('TC-API-004 — Atualizar post via PUT', async ({ jsonApi }) => {
    let response: Awaited<ReturnType<typeof jsonApi.put>>;

    await test.step('Atualizar post', async () => {
      response = await jsonApi.put('/posts/1', {
        data: { id: 1, title: 'Título Atualizado', body: 'Corpo atualizado pelo executor-api', userId: 1 },
      });
    });

    await test.step('Validar atualização', async () => {
      expect(response!.status()).toBe(200);
      const data = await response!.json();
      expect(data.title).toBe('Título Atualizado');
      expect(data.id).toBe(1);
    });
  });

  test('TC-API-005 — Deletar post via DELETE', async ({ jsonApi }) => {
    let response: Awaited<ReturnType<typeof jsonApi.delete>>;

    await test.step('Deletar post', async () => {
      response = await jsonApi.delete('/posts/1');
    });

    await test.step('Validar deleção', async () => {
      expect(response!.status()).toBe(200);
      const data = await response!.json();
      expect(Object.keys(data).length).toBe(0);
    });
  });

  test('TC-API-006 — Buscar todos os posts do usuário 1', async ({ jsonApi }) => {
    let response: Awaited<ReturnType<typeof jsonApi.get>>;

    await test.step('Requisitar posts do usuário 1', async () => {
      response = await jsonApi.get('/posts?userId=1');
    });

    await test.step('Validar filtro por userId', async () => {
      expect(response!.status()).toBe(200);
      const data = await response!.json();
      expect(data.length).toBe(10);
      for (const item of data) {
        expect(item.userId).toBe(1);
      }
    });
  });

  test('TC-API-007 — Buscar usuário ID 1 e validar schema completo', async ({ jsonApi }) => {
    let response: Awaited<ReturnType<typeof jsonApi.get>>;

    await test.step('Requisitar usuário ID 1', async () => {
      response = await jsonApi.get('/users/1');
    });

    await test.step('Validar campos do usuário', async () => {
      expect(response!.status()).toBe(200);
      const data = await response!.json();
      expect(data.id).toBe(1);
      expect(data.name).toBe('Leanne Graham');
      expect(data.username).toBe('Bret');
      expect(data.email).toBe('Sincere@april.biz');
      expect(data.address).toBeTruthy();
      expect(typeof data.address.city).toBe('string');
      expect(typeof data.address.zipcode).toBe('string');
      expect(data.company).toBeTruthy();
      expect(typeof data.company.name).toBe('string');
    });
  });

  test('TC-API-008 — Validar schema Zod do endpoint /users/1', async ({ jsonApi }) => {
    let response: Awaited<ReturnType<typeof jsonApi.get>>;

    await test.step('Requisitar usuário ID 1', async () => {
      response = await jsonApi.get('/users/1');
    });

    await test.step('Validar contrato Zod', async () => {
      expect(response!.status()).toBe(200);
      const data = await response!.json();
      const validation = userSchema.safeParse(data);
      if (!validation.success) {
        console.error('[CONTRACT] Falha Zod:', JSON.stringify(validation.error.format()));
      }
      expect(validation.success, 'Contrato Zod deve ser válido').toBeTruthy();
    });
  });

  test('TC-API-009 — Buscar todos os todos do usuário 1', async ({ jsonApi }) => {
    let response: Awaited<ReturnType<typeof jsonApi.get>>;

    await test.step('Requisitar todos do usuário 1', async () => {
      response = await jsonApi.get('/todos?userId=1');
    });

    await test.step('Validar todos', async () => {
      expect(response!.status()).toBe(200);
      const data = await response!.json();
      expect(data.length).toBe(20);
      for (const item of data) {
        expect(typeof item.id).toBe('number');
        expect(typeof item.userId).toBe('number');
        expect(typeof item.title).toBe('string');
        expect(typeof item.completed).toBe('boolean');
      }
    });
  });

  test('TC-API-010 — Buscar todo ID 1', async ({ jsonApi }) => {
    let response: Awaited<ReturnType<typeof jsonApi.get>>;

    await test.step('Requisitar todo ID 1', async () => {
      response = await jsonApi.get('/todos/1');
    });

    await test.step('Validar todo', async () => {
      expect(response!.status()).toBe(200);
      const data = await response!.json();
      expect(data.userId).toBe(1);
      expect(data.id).toBe(1);
      expect(data.title).toBe('delectus aut autem');
      expect(data.completed).toBe(false);
    });
  });

});
