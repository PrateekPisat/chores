import { AxiosError } from 'axios';
import { ErrorMap, ValidationError } from './boot/axios';
import { format, parseISO } from 'date-fns';

export function handleError(err: AxiosError | ValidationError): ErrorMap {
  if (err instanceof ValidationError) {
    return err.errors;
  } else {
    throw err;
  }
}

export function endOfWeek(date: Date): Date {
  const lastday = date.getDate() - (date.getDay() - 1) + 6;
  return new Date(date.setDate(lastday));
}

export function datetimeFormat(
  date: string | Date | null,
  formatString: string
): string {
  if (!date) {
    return 'Invalid';
  }

  if (typeof date === 'string') {
    date = parseISO(date);
  }
  return format(date, formatString);
}

export function fluentFormatDatetime(date: string | Date | null): string {
  return datetimeFormat(date, 'PPPP');
}
