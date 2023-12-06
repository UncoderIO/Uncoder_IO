import { IocParsingRulesType } from '../../types/iocsTypes';

type InputTextFilterType = {
  name: string,
};

export type InputTextFilterRawType = {
  filterHandler: (value: string) => string,
  id: IocParsingRulesType,
} & InputTextFilterType;

export type InputTextFiltersType = InputTextFilterType[];
