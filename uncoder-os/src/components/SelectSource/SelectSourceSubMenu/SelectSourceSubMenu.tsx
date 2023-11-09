import React from 'react';
import { SelectSourceMenuItem } from '../SelectSourceMenu/SelectSourceMenuItem';
import { CollapseBox } from '../../CollapseBox';

import { SelectSourceType } from '../Type';
import { GroupListType } from '../../../tools';

import './SelectSourceSubMenu.sass';

type SelectSourceSubMenuProps = {
  id: number;
  data: GroupListType['data'];
  isActive?: boolean;
  handleClick: SelectSourceType['onSelectedSiemChangeHandler'];
};

export const SelectSourceSubMenu: React.FC <SelectSourceSubMenuProps> = ({
  id,
  data,
  isActive = false,
  handleClick,
}) => (
  <CollapseBox isActive={isActive}>
    <div className="select-source-sub-menu">
      {
        data?.length && (
          data.map((platformItem) => (
            <div className="select-source-sub-menu__list" key={platformItem.id}>
              <div className="select-source-sub-menu__title m-b-2">
                {platformItem.name}
              </div>
              {
                platformItem.data.map((item) => (
                  <SelectSourceMenuItem
                    id={id}
                    option={item}
                    handleClick={handleClick}
                    key={item.name}
                  />
                ))
              }
            </div>
          ))
        )
      }
    </div>
  </CollapseBox>
);
