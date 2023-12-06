import { FC } from 'react';
import { BasicIocType } from '../../types/iocsTypes';
import { OneIocElement } from './IocOneElement';

import './IocsStatistic.sass';

type IocsStatisticProps = {
  getOneIocTypeCount: (iocType: BasicIocType) => number;
  totalIocsCount: number;
}

export const IocsStatistic: FC<IocsStatisticProps> = (
  {
    getOneIocTypeCount,
    totalIocsCount,
  },
) => (
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
      {<div className="iocs-stat__count">
        {`${totalIocsCount}/10000`}
      </div>}
    </div>
);
