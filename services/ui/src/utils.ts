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

export function dueDay(value: string): Date {
  const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(value);
  if (match) {
    return new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]));
  }
  const parsed = new Date(value);
  return new Date(parsed.getFullYear(), parsed.getMonth(), parsed.getDate());
}

/** Monday through Sunday, matching the previous week ending on Sunday. */
export function startOfWeek(date: Date): Date {
  const day = date.getDay();
  const fromMonday = day === 0 ? 6 : day - 1;
  const start = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  start.setDate(start.getDate() - fromMonday);
  return start;
}

export function endOfWeek(date: Date): Date {
  const end = startOfWeek(date);
  end.setDate(end.getDate() + 6);
  return end;
}

export interface DueItem {
  dueDate: string;
}

export function groupByDue<T extends DueItem>(items: T[], now = new Date()) {
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const weekStart = startOfWeek(today);
  const weekEnd = endOfWeek(today);
  const monthStart = new Date(today.getFullYear(), today.getMonth(), 1);
  const monthEnd = new Date(today.getFullYear(), today.getMonth() + 1, 0);
  const pastDue: T[] = [];
  const thisWeek: T[] = [];
  const thisMonth: T[] = [];
  const later: T[] = [];

  for (const item of items) {
    const due = dueDay(item.dueDate);
    if (due < today) {
      pastDue.push(item);
    } else if (due >= weekStart && due <= weekEnd) {
      thisWeek.push(item);
    } else if (due >= monthStart && due <= monthEnd) {
      thisMonth.push(item);
    } else {
      later.push(item);
    }
  }

  return { pastDue, thisWeek, thisMonth, later };
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
