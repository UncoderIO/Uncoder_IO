import React, { FC } from 'react';
import { BasicIocType } from '../../types/iocsTypes';
import { useIocsStatistic } from './useIocsStatistic';
import { OneIocElement } from './IocOneElement';

import './IocsStatistic.sass';

export const IocsStatistic: FC = () => {
  const {
    getOneIocTypeCount,
  } = useIocsStatistic();

  return (
    <div className="iocs-stat">
      <div className="iocs-stat__list">
        <OneIocElement
          iocCurrentType={BasicIocType.Hash}
          value={getOneIocTypeCount(BasicIocType.Hash)}
        />
        <OneIocElement
          iocCurrentType={BasicIocType.Domain}
          value={getOneIocTypeCount(BasicIocType.Domain)}
        />
        <OneIocElement
          iocCurrentType={BasicIocType.Url}
          value={getOneIocTypeCount(BasicIocType.Url)}
        />
        <OneIocElement
          iocCurrentType={BasicIocType.Ip}
          value={getOneIocTypeCount(BasicIocType.Ip)}
        />

{/*
//todo: should be implemented on the backand side
<OneIocElement
          iocCurrentType={BasicIocType.Emails}
          value={getOneIocTypeCount(BasicIocType.Emails)}
        />
        <OneIocElement
          iocCurrentType={BasicIocType.Files}
          value={getOneIocTypeCount(BasicIocType.Files)}
        /> */}
      </div>
      {/* <div className="iocs-stat__count">
        {`${getTotalIocsCount()}/${iocPerQueryCount}`}
      </div> */}
    </div>
  );
};
