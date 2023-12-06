/* eslint-disable no-restricted-globals */
import { ProcessList } from '../enums';
import { CalculateIocsMessage } from '../CalculateIocsMessage';
import { calcIocsInText } from '../../components/IocsStatistic/calcIocsInText';
import { BasicIocType, IocsByTypeCountType, IocsListTypes } from '../../types/iocsTypes';

const getTotalIocsCount = (data: IocsByTypeCountType): number => {
  let total = 0;
  Object.keys(data).forEach((oneIocTypeKey) => {
    const oneIocType: number = data[oneIocTypeKey as IocsListTypes] ?? 0;

    if (oneIocTypeKey !== BasicIocType.Hash) {
      total += oneIocType;
    }
  });

  return total;
};

self.onmessage = (e: MessageEvent<string>) => {
  const data = JSON.parse(e.data) as CalculateIocsMessage;
  if (data.action !== ProcessList.calculateIocs) {
    return;
  }

  const result = calcIocsInText(data.iocText || '');

  self.postMessage(
    JSON.stringify({
      action: ProcessList.calculateIocs,
      calculatedData: result,
      totalCount: getTotalIocsCount(result),
    }),
  );
};

export {};
