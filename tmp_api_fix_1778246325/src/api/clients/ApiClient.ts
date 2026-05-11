import { APIRequestContext, APIResponse } from '@playwright/test';

const BASE = 'https://swapi.dev/api';

export class ApiClient {
  constructor(private request: APIRequestContext) {}

  async getById(resource: string, id: string): Promise<APIResponse> {
    return this.request.get(`${BASE}/${resource}/${id}/`);
  }

  async getAll(resource: string): Promise<APIResponse> {
    return this.request.get(`${BASE}/${resource}/`);
  }
}
