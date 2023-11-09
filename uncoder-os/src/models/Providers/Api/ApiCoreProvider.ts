export class ApiCoreProvider {
  private readonly baseUrl: string | undefined;

  private readonly clientConfig: RequestInit;

  constructor(baseUrl: string | undefined) {
    this.baseUrl = baseUrl;

    this.clientConfig = {
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
    };
  }

  private makeUrlString(url: string, queryParams?: Record<string, string>): string {
    if (queryParams) {
      const params = new URLSearchParams(queryParams);
      return `${this.baseUrl}${url}?${params.toString()}`;
    }

    return `${this.baseUrl}${url}`;
  }

  // eslint-disable-next-line class-methods-use-this
  private handleError(err: Error): Error {
    return err;
  }

  async getResource<T = never>(url: string, queryParams?: Record<string, string>): Promise<T> {
    try {
      const response = await fetch(this.makeUrlString(url, queryParams), {
        ...this.clientConfig,
        headers: {
          Accept: 'application/json',
        },
        method: 'GET',
      });

      return await response.json() as unknown as Promise<T>;
    } catch (err: any) {
      throw (this.handleError(err));
    }
  }

  async postJsonResource<T = never, D = never>(url: string, dataObj?: D): Promise<T> {
    try {
      const response = await fetch(this.makeUrlString(url), {
        ...this.clientConfig,
        method: 'POST',
        body: JSON.stringify(dataObj),
      });

      return await response.json() as T;
    } catch (err: any) {
      throw (this.handleError(err));
    }
  }

  async putJsonResource<T = never, D = never>(url: string, dataObj?: D): Promise<T> {
    try {
      const response = await fetch(this.makeUrlString(url), {
        ...this.clientConfig,
        method: 'PUT',
        body: JSON.stringify(dataObj),
      });

      return await response.json() as T;
    } catch (err: any) {
      throw (this.handleError(err));
    }
  }

  async patchJsonResource<T = never, D = never>(url: string, dataObj?: D): Promise<T> {
    try {
      const response = await fetch(this.makeUrlString(url), {
        ...this.clientConfig,
        method: 'PATCH',
        body: JSON.stringify(dataObj),
      });

      return await response.json() as T;
    } catch (err: any) {
      throw (this.handleError(err));
    }
  }

  async deleteResource<T = never>(url: string): Promise<T> {
    try {
      const response = await fetch(this.makeUrlString(url), {
        ...this.clientConfig,
        method: 'DELETE',
      });

      return await response.json() as T;
    } catch (e: any) {
      throw (this.handleError(e));
    }
  }
}
