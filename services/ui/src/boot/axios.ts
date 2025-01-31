import { boot } from 'quasar/wrappers';
import axios, { AxiosError, AxiosInstance } from 'axios';
import { join } from 'lodash';
import { z } from 'zod';

declare module 'vue' {
  interface ComponentCustomProperties {
    $axios: AxiosInstance;
    $api: AxiosInstance;
  }
}

const UnprocessableEntityResponse = z.record(z.array(z.string()));

class ErrorMap extends Map<string, string[]> {
  getString(key: string): string {
    return join(super.get(key));
  }
}

class ValidationError {
  errors: ErrorMap = new ErrorMap();

  constructor(err: AxiosError) {
    const result = UnprocessableEntityResponse.safeParse(err.response?.data);
    if (result.success) {
      this.errors = new ErrorMap(Object.entries(result.data));
    }

    // Backwards compatibility with code that doesn't know about the ValidationError class
    Object.assign(this, err);
  }
}

// Be careful when using SSR for cross-request state pollution
// due to creating a Singleton instance here;
// If any client changes this (global) instance, it might be a
// good idea to move this instance creation inside of the
// "export default () => {}" function below (which runs individually
// for each client)
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL, timeout: 5 * 60 * 1000,
  responseType: 'json',
});

export default boot(({ app }) => {
  // for use inside Vue files (Options API) through this.$axios and this.$api

  app.config.globalProperties.$axios = axios;
  // ^ ^ ^ this will allow you to use this.$axios (for Vue Options API form)
  //       so you won't necessarily have to import axios in each vue file

  app.config.globalProperties.$api = api;
  // ^ ^ ^ this will allow you to use this.$api (for Vue Options API form)
  //       so you can easily perform requests against your app's API
});


function registerResponseMappers(http: AxiosInstance) {
  http.interceptors.response.use(undefined, (err) => {
    if (axios.isAxiosError(err) && err.response?.status === 422) {
      return Promise.reject(new ValidationError(err));
    }
    return Promise.reject(err);
  });
}

registerResponseMappers(api);

export { api, ErrorMap, ValidationError };
