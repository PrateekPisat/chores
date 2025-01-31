import { AxiosError } from 'axios';
import { ErrorMap, ValidationError } from './boot/axios';

export function handleError(err: AxiosError | ValidationError): ErrorMap {
  if (err instanceof ValidationError) {
    return err.errors;
  } else {
    throw err;
  }
}
