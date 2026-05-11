import { APIRequestContext, APIResponse } from '@playwright/test';

export class ApiClient {
  constructor(private request: APIRequestContext) {}

  async getAll(path: string): Promise<APIResponse> {
    return this.request.get(path);
  }

  async getById(path: string, id: string | number): Promise<APIResponse> {
    return this.request.get(`${path}/${id}`);
  }

  async create(path: string, data: Record<string, unknown>): Promise<APIResponse> {
    return this.request.post(path, { data });
  }

  async update(path: string, id: string | number, data: Record<string, unknown>): Promise<APIResponse> {
    return this.request.put(`${path}/${id}`, { data });
  }

  async patch(path: string, id: string | number, data: Record<string, unknown>): Promise<APIResponse> {
    return this.request.patch(`${path}/${id}`, { data });
  }

  async remove(path: string, id: string | number): Promise<APIResponse> {
    return this.request.delete(`${path}/${id}`);
  }

  async getWithQuery(path: string, params: Record<string, string | number>): Promise<APIResponse> {
    const query = Object.entries(params).map(([k, v]) => `${k}=${v}`).join('&');
    return this.request.get(`${path}?${query}`);
  }
}
