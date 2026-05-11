import { APIRequestContext, APIResponse } from '@playwright/test';
export class ApiClient {
  constructor(private request: APIRequestContext) {}
  async get(url: string): Promise<APIResponse> {
    return this.request.get(url);
  }
}
