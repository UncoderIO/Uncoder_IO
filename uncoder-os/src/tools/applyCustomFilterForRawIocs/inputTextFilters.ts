import { InputTextFilterRawType, InputTextFiltersType } from './InputTextFiltersType';
import { replaceBracketsWithDotFilter } from './filtersHandler/replace-brackets-with-dot';
import { replaceHxxpWithHttp } from './filtersHandler/replace-hxxp-with-http';
import { IocParsingRulesType } from '../../types/iocsTypes';

export const inputTextForRawIocsFilters: InputTextFilterRawType[] = [{
  name: 'Replace (.) [.] {.} with dot',
  id: IocParsingRulesType.ReplaseDots,
  filterHandler: replaceBracketsWithDotFilter,
}, {
  name: 'Replace hxxp with http',
  id: IocParsingRulesType.ReplaseHXXP,
  filterHandler: replaceHxxpWithHttp,
}];

export const inputTextFilters: InputTextFiltersType = inputTextForRawIocsFilters
  .map(({ name }) => ({ name }));
