import React from 'react';
import { Button } from '../../../Buttons';

import { ReactComponent as ArrowDownIcon } from '../../Svg/ArrowDownIcon.svg';
import { ReactComponent as StarIcon } from './Svg/StarIcon.svg';
import { SelectSourceMenuType, SelectSourceType } from '../../Type';
import { GroupListType } from '../../../../tools';

import './SelectSourceMenuItem.sass';

type SelectSourceMenuItemProps = {
  id: number;
  isCheck?: boolean;
  isActive?: boolean;
  option: GroupListType;
  handleClick?: SelectSourceType['onSelectedSiemChangeHandler'];
  handleClickAddFavorite?: SelectSourceMenuType['handleClickAddFavorite'];
  handleToggleSelectMenu?: SelectSourceMenuType['handleToggleSelectMenu'];
  disableAddToFavorite?: boolean;
};

export const SelectSourceMenuItem: React.FC <SelectSourceMenuItemProps> = ({
  id,
  isCheck = false,
  isActive,
  option,
  disableAddToFavorite,
  handleClick,
  handleClickAddFavorite,
  handleToggleSelectMenu,
}) => (
  <div
    className={`source-selector-menu-item${isActive ? ' is-active' : ''}${!disableAddToFavorite ? ' is-default' : ''}`}
    onClick={handleClick?.(option)}
  >
    {
      !disableAddToFavorite && (
        <div
          className={`source-selector-menu-item__star m-r-4 ${isCheck ? 'is-check' : ''}`}
          onClick={(event) => {
            event.stopPropagation();
            handleClickAddFavorite?.(option)();
          }}
        >
          <StarIcon/>
        </div>
      )
    }
    <div className={`source-selector-menu-item__text${!disableAddToFavorite ? ' is-transform' : ''}`}>
      {option.name}
    </div>
    {
      option?.data && (
        <div className="source-selector-menu-item__btn">
          <Button
            classes="button--icon button--xs button--default"
            children={<ArrowDownIcon/>}
            onClick={
              (event) => {
                event.stopPropagation();
                handleToggleSelectMenu?.(id)();
              }
            }
            aria-label="delete"
            type="button"
          />
        </div>
      )
    }
  </div>
);
