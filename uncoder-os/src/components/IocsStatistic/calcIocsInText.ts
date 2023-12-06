import {
  BasicIocType, IocsListTypes, ParsedIocsType, hashTypes, IocsByTypeCountType,
} from '../../types/iocsTypes';
import { IOCS_REGEXP, TOP_LEVEL_DOMAIN_LIST } from '../../constants/IocsInputEditorConstats';

const extractMatchesFromMatchAll = (iocType: IocsListTypes, match: RegExpMatchArray): string[] => {
  const result: string[] = [];

  switch (iocType) {
    case BasicIocType.Emails:
      if (typeof match[0] === 'string') {
        result.push(match[0]);
      } else if (typeof match[1] === 'string') {
        result.push(match[1]);
      }
      break;

    default:
      if (typeof match[1] === 'string') {
        result.push(match[1]);
      } else if (typeof match[0] === 'string') {
        result.push(match[0]);
      }
      break;
  }

  return result;
};

const filterFilesByWhiteList = (domains: string[]) => domains.filter(
  (domain) => !TOP_LEVEL_DOMAIN_LIST.includes(
    (domain.match(/[^.]+$/ui) || [])[0] || '',
  ),
);

const filterDomainsByWhiteList = (domains: string[]) => domains.filter(
  (domain) => TOP_LEVEL_DOMAIN_LIST.includes(
    (domain.match(/[^.]+$/ui) || [])[0] || '',
  ),
);
export const calcIocsInText = (text: string): IocsByTypeCountType => {
  const result: ParsedIocsType = {};

  for (let i = 0; i < Object.entries(IOCS_REGEXP).length; i++) {
    const [iocType, value] = Object.entries(IOCS_REGEXP)[i];
    result[iocType as IocsListTypes] = [];
    if (value instanceof RegExp) {
      [...(text || '').matchAll(value)].forEach((match) => {
        const matches = extractMatchesFromMatchAll(iocType as IocsListTypes, match);
        if (matches.length) {
          result[iocType as IocsListTypes] = result[iocType as IocsListTypes]
            ? result[iocType as IocsListTypes]
            : [];
          result[iocType as IocsListTypes]?.push(...matches);
        }
      });
    }

    if (iocType === BasicIocType.Domain) {
      result[iocType] = filterDomainsByWhiteList(result[iocType] || []);
    }

    if (iocType === BasicIocType.Files) {
      result[iocType] = filterFilesByWhiteList(result[iocType] || []);
    }
  }

  for (let i = 0; i < Object.entries(result).length; i++) {
    const [iocType] = Object.entries(result)[i];
    result[iocType as IocsListTypes] = result[iocType as IocsListTypes]
      ?.filter((value, index, self) => self.indexOf(value) === index);
    result[iocType as IocsListTypes] = result[iocType as IocsListTypes]
      ?.map((ioc) => ioc.trim());
  }

  result[BasicIocType.Hash] = [];
  hashTypes.forEach((hasType) => {
    if (Array.isArray(result[hasType])) {
      result[BasicIocType.Hash] = result[BasicIocType.Hash]?.concat(result[hasType] || []);
    }
  });
  result[BasicIocType.Hash] = result[BasicIocType.Hash]
    .filter((value, index, self) => self.indexOf(value) === index);

  const countResult: IocsByTypeCountType = {};

  for (let i = 0; i < Object.entries(result).length; i++) {
    const [iocType, value] = Object.entries(result)[i];
    countResult[iocType as IocsListTypes] = value?.length || 0;
  }

  return countResult;
};
