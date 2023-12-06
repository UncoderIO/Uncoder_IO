import { useSelector } from 'react-redux';
import { inputEditorPlatformCodeSelector, inputEditorTextSelector } from '../../reduxData/inputEditor';
import { useEffect, useMemo, useState } from 'react';
import { IocsByTypeCountType, IocsListTypes } from '../../types/iocsTypes';
import { ProcessList } from '../../processes/enums';
import { CalculateIocsMessage } from '../../processes/CalculateIocsMessage';

// @ts-ignore
import Worker from '../../processes/workers/calculateIocs.worker';

export const useIocCountCalculation = () => {
  const inputText = useSelector(inputEditorTextSelector);
  const parser = useSelector(inputEditorPlatformCodeSelector);

  const [inputTextCalculatedIocs, setIocCount] = useState<IocsByTypeCountType>({});
  const [totalCountIocs, setTotalCountIocs] = useState<number>(0);

  const calculateIocsWorker: Worker = useMemo(
    () => new Worker(),
    [],
  );

  useEffect(() => {
    if (window.Worker && parser === 'ioc') {
      calculateIocsWorker?.postMessage(
        JSON.stringify({ action: ProcessList.calculateIocs, iocText: inputText }),
      );
    }
  }, [calculateIocsWorker, inputText, parser]);

  useEffect(() => {
    if (window.Worker && calculateIocsWorker) {
      calculateIocsWorker.onmessage = (e: MessageEvent<string>) => {
        const data = JSON.parse(e.data) as CalculateIocsMessage;
        if (data.action !== ProcessList.calculateIocs) {
          return;
        }
        setIocCount(data.calculatedData || {});
        setTotalCountIocs(data.totalCount || 0);
      };
    }
  }, [calculateIocsWorker]);

  const getOneIocTypeCount = (
    iocType: IocsListTypes,
  ): number => inputTextCalculatedIocs[iocType] ?? 0;

  return {
    getOneIocTypeCount,
    totalCountIocs,
  };
};
