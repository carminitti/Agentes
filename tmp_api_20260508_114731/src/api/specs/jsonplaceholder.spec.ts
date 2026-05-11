import { test, expect } from '../../support/fixtures';
import { userSchema, postSchema, commentSchema, todoSchema } from '../schemas/schemas';

test.describe('JsonPlaceholder API @api', () => {

  // TC-AMB-001 — API está acessível e respondendo (smoke)
  test('TC-AMB-001 — API está acessível e respondendo', async ({ apiClient, apiRequest }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;
    let durationMs: number;

    await test.step('GET /users e medir tempo de resposta', async () => {
      const start = Date.now();
      response = await apiClient.getAll('/users');
      durationMs = Date.now() - start;
    });

    await test.step('Validar status 200 e tempo < 3000ms', async () => {
      expect(response.status()).toBe(200);
      expect(response.ok()).toBeTruthy();
      expect(durationMs).toBeLessThan(3000);
    });

    await test.step('Validar Content-Type e body não vazio', async () => {
      expect(response.headers()['content-type']).toContain('application/json');
      const body = await response.json();
      expect(Array.isArray(body)).toBeTruthy();
      expect(body.length).toBeGreaterThan(0);
    });
  });

  // TC-USR-001 — Listar todos os usuários
  test('TC-USR-001 — Listar todos os usuários', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('GET /users', async () => {
      response = await apiClient.getAll('/users');
    });

    await test.step('Validar status 200 e 10 usuários', async () => {
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(Array.isArray(body)).toBeTruthy();
      expect(body.length).toBe(10);
      for (const user of body) {
        expect(user).toHaveProperty('id');
        expect(user).toHaveProperty('name');
        expect(user).toHaveProperty('email');
        expect(user).toHaveProperty('username');
      }
    });
  });

  // TC-USR-002 — Buscar usuário existente por ID
  test('TC-USR-002 — Buscar usuário existente por ID', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('GET /users/1', async () => {
      response = await apiClient.getById('/users', 1);
    });

    await test.step('Validar status 200 e dados do usuário', async () => {
      expect(response.status()).toBe(200);
      const user = await response.json();
      expect(user.id).toBe(1);
      expect(user.name).toBe('Leanne Graham');
      expect(user.email).toBe('Sincere@april.biz');
      expect(user.username).toBe('Bret');
    });
  });

  // TC-USR-003 — Buscar usuário inexistente retorna 404
  test('TC-USR-003 — Buscar usuário inexistente retorna 404', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('GET /users/999', async () => {
      response = await apiClient.getById('/users', 999);
    });

    await test.step('Validar status 404 e body vazio', async () => {
      expect(response.status()).toBe(404);
      const body = await response.json();
      expect(Object.keys(body).length).toBe(0);
    });
  });

  // TC-USR-004 — Criar novo usuário
  test('TC-USR-004 — Criar novo usuário', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('POST /users', async () => {
      response = await apiClient.create('/users', {
        name: 'QA Tester',
        username: 'qa_tester',
        email: 'qa@test.com',
      });
    });

    await test.step('Validar status 201 e dados criados', async () => {
      expect(response.status()).toBe(201);
      const body = await response.json();
      expect(body.name).toBe('QA Tester');
      expect(body.id).toBeDefined();
      expect(body.id).not.toBeNull();
    });
  });

  // TC-USR-005 — Atualizar usuário com PUT
  test('TC-USR-005 — Atualizar usuário com PUT', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('PUT /users/1', async () => {
      response = await apiClient.update('/users', 1, {
        id: 1,
        name: 'Leanne Updated',
        username: 'leanne_v2',
        email: 'updated@test.com',
      });
    });

    await test.step('Validar status 200 e dados atualizados', async () => {
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body.name).toBe('Leanne Updated');
      expect(body.id).toBe(1);
    });
  });

  // TC-USR-006 — Atualizar usuário parcialmente com PATCH
  test('TC-USR-006 — Atualizar usuário parcialmente com PATCH', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('PATCH /users/1', async () => {
      response = await apiClient.patch('/users', 1, { name: 'Leanne Patched' });
    });

    await test.step('Validar status 200 e name atualizado', async () => {
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body.name).toBe('Leanne Patched');
    });
  });

  // TC-USR-007 — Deletar usuário
  test('TC-USR-007 — Deletar usuário', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('DELETE /users/1', async () => {
      response = await apiClient.remove('/users', 1);
    });

    await test.step('Validar status 200 e body vazio', async () => {
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(Object.keys(body).length).toBe(0);
    });
  });

  // TC-POST-001 — Listar posts do usuário 1
  test('TC-POST-001 — Listar posts do usuário 1', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('GET /posts?userId=1', async () => {
      response = await apiClient.getWithQuery('/posts', { userId: 1 });
    });

    await test.step('Validar status 200 e posts do userId 1', async () => {
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(Array.isArray(body)).toBeTruthy();
      expect(body.length).toBeGreaterThan(0);
      for (const post of body) {
        expect(post.userId).toBe(1);
        expect(post).toHaveProperty('id');
        expect(post).toHaveProperty('title');
        expect(post).toHaveProperty('body');
        expect(post).toHaveProperty('userId');
      }
    });
  });

  // TC-POST-002 — Buscar post existente por ID
  test('TC-POST-002 — Buscar post existente por ID', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('GET /posts/1', async () => {
      response = await apiClient.getById('/posts', 1);
    });

    await test.step('Validar status 200 e dados do post', async () => {
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body.id).toBe(1);
      expect(body.userId).toBe(1);
      expect(body.title).toBeTruthy();
      expect(body.body).toBeTruthy();
      const validation = postSchema.safeParse(body);
      expect(validation.success, 'Contrato do post deve ser válido').toBeTruthy();
    });
  });

  // TC-POST-003 — Criar novo post
  test('TC-POST-003 — Criar novo post', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('POST /posts', async () => {
      response = await apiClient.create('/posts', {
        title: 'Post de teste',
        body: 'Conteúdo do post',
        userId: 1,
      });
    });

    await test.step('Validar status 201 e dados do post criado', async () => {
      expect(response.status()).toBe(201);
      const body = await response.json();
      expect(body.title).toBe('Post de teste');
      expect(body.userId).toBe(1);
      expect(body.id).toBeDefined();
    });
  });

  // TC-COMM-001 — Listar comentários do post 1
  test('TC-COMM-001 — Listar comentários do post 1', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('GET /comments?postId=1', async () => {
      response = await apiClient.getWithQuery('/comments', { postId: 1 });
    });

    await test.step('Validar status 200 e comentários com campos obrigatórios', async () => {
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(Array.isArray(body)).toBeTruthy();
      expect(body.length).toBeGreaterThan(0);
      for (const comment of body) {
        expect(comment).toHaveProperty('id');
        expect(comment).toHaveProperty('name');
        expect(comment).toHaveProperty('email');
        expect(comment).toHaveProperty('body');
        expect(comment.email).toContain('@');
      }
    });
  });

  // TC-TODO-001 — Buscar todo por ID
  test('TC-TODO-001 — Buscar todo por ID', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('GET /todos/1', async () => {
      response = await apiClient.getById('/todos', 1);
    });

    await test.step('Validar status 200 e dados do todo', async () => {
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body.id).toBe(1);
      expect(body.userId).toBeDefined();
      expect(body.title).toBeTruthy();
      expect(typeof body.completed).toBe('boolean');
      const validation = todoSchema.safeParse(body);
      expect(validation.success, 'Contrato do todo deve ser válido').toBeTruthy();
    });
  });

  // TC-TODO-002 — Filtrar todos concluídos
  test('TC-TODO-002 — Filtrar todos concluídos', async ({ apiClient }) => {
    let response: Awaited<ReturnType<typeof apiClient.getAll>>;

    await test.step('GET /todos?completed=true', async () => {
      response = await apiClient.getWithQuery('/todos', { completed: 'true' as unknown as number });
    });

    await test.step('Validar status 200 e todos com completed == true', async () => {
      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(Array.isArray(body)).toBeTruthy();
      expect(body.length).toBeGreaterThan(0);
      for (const todo of body) {
        expect(todo.completed).toBe(true);
      }
    });
  });

});
