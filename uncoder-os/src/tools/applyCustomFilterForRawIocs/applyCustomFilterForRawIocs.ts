import { inputTextForRawIocsFilters } from './inputTextFilters';

export const applyCustomFilterForRawIocs = (value: string, filters: string[]): string => {
  filters.forEach((name) => {
    inputTextForRawIocsFilters.forEach((filter) => {
      if (filter.id === name && value) {
        value = filter.filterHandler(value);
      }
    });
  });

  return value;
};
