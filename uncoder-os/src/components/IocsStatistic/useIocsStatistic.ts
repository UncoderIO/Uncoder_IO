import { BasicIocType } from '../../types/iocsTypes';

export const useIocsStatistic = () => {
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
    const convertedValue: number = parseInt((value ?? 0).toString(), 10);

    if (convertedValue >= 1000) {
      return `${Math.floor(convertedValue / 1000)}k`;
    }

    return convertedValue.toString();
  };

  return {
    convertValue,
    getCurrentIocConfig,
  };
};
