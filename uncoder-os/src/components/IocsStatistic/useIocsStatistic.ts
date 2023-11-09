import { useSelector } from 'react-redux';
import { parseInt } from 'lodash';
import { BasicIocType, IocsListTypes } from '../../types/iocsTypes';
import { calcIocsInText } from './calcIocsInText';
import { inputEditorTextSelector } from '../../reduxData/inputEditor';
// import { getIocPerQueryCount } from '../../service/limitationSettings';

export const useIocsStatistic = () => {
  const inputText = useSelector(inputEditorTextSelector);
  const inputTextCalculatedIocs = calcIocsInText(inputText);

  const getOneIocTypeCount = (
    iocType: IocsListTypes,
  ): number => (inputTextCalculatedIocs[iocType] || []).length;

  const getTotalIocsCount = (): number => {
    let total = 0;
    Object.keys(inputTextCalculatedIocs).forEach((oneIocTypeKey) => {
      const oneIocType: string[] = inputTextCalculatedIocs[oneIocTypeKey as IocsListTypes] || [];

      if (oneIocTypeKey !== BasicIocType.Hash) {
        total += oneIocType.length;
      }
    });

    return total;
  };

  const getCurrentIocConfig = (
    type: BasicIocType,
  ): { className: string; name: string } | undefined => {
    switch (type) {
      case BasicIocType.Hash:
        return {
          className: BasicIocType.Hash,
          name: 'Hashes',
        };
      case BasicIocType.Domain:
        return {
          className: BasicIocType.Domain,
          name: 'Domains',
        };
      case BasicIocType.Url:
        return {
          className: BasicIocType.Url,
          name: 'URLs',
        };
      case BasicIocType.Ip:
        return {
          className: BasicIocType.Ip,
          name: 'IPs',
        };
      case BasicIocType.Emails:
        return {
          className: BasicIocType.Emails,
          name: 'Emails',
        };
      case BasicIocType.Files:
        return {
          className: BasicIocType.Files,
          name: 'Files',
        };

      default:
        return undefined;
    }
  };

  const convertValue = (value?: string | number): string => {
    const convertedValue: number = parseInt((value ?? 0).toString());

    if (convertedValue >= 1000) {
      return `${Math.floor(convertedValue / 1000)}k`;
    }

    return convertedValue.toString();
  };

  return {
    convertValue,
    getOneIocTypeCount,
    getTotalIocsCount,
    getCurrentIocConfig,
    iocPerQueryCount: 10,
    // iocPerQueryCount: getIocPerQueryCount(),
  };
};
