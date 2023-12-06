import React from 'react';
import { Tooltip } from '../../Tooltip';
import { BasicIocType } from '../../../types/iocsTypes';
import { useIocsStatistic } from '../useIocsStatistic';

import './IocOneElement.sass';

export type OneIocElementPropsType = {
  value?: string | number;
  iocCurrentType: BasicIocType;
};

export const OneIocElement: React.FC<OneIocElementPropsType> = ({ value, iocCurrentType }) => {
  const { getCurrentIocConfig, convertValue } = useIocsStatistic();
  const currentIocConfig = getCurrentIocConfig(iocCurrentType);

  if (!currentIocConfig) {
    return null;
  }

  const { className, name } = currentIocConfig;

  return (
    <div className="one-ioc-element">
      <Tooltip content={`${value ?? 0}`}>
        <span>
          <span className="one-ioc-element__count m-r-4">
            {convertValue(value)}
          </span>
          <span className={`one-ioc-element--${className}`}>
            {name}
          </span>
        </span>
      </Tooltip>
    </div>
  );
};
