import { APIRequestContext, APIResponse } from '@playwright/test';

export class ApiClient {
  constructor(private request: APIRequestContext) {}

  async getById(path: string, id: string): Promise<APIResponse> {
    return this.request.get(`${path}/${id}/`);
  }

  async getAll(path: string): Promise<APIResponse> {
    return this.request.get(`${path}/`);
  }
}
