import React from 'react';
import { SelectSourceInput } from './SelectSourceInput';
import { SelectSourceMenu } from './SelectSourceMenu';
import { PopperWindow } from '../PopperWindow';
import { useSelectSource } from './Hooks';
import { SelectSourceType } from './Type';

import './SelectSource.sass';

export const SelectSource: React.FC<SelectSourceType> = ({
  siemsList,
  siemSelector,
  onSelectedSiemChangeHandler,
}) => {
  const {
    selectRef,
    selectOpen,
    selectMenuOpen,
    activeItems,
    inputValue,
    favoriteGroupList,
    groupList,
    cursor,
    scrollRef,
    handleToggleSelect,
    handleToggleSelectMenu,
    handleClickAddFavorite,
    onSelectedGroupHandler,
    handleInput,
    handleOnHoover,
  } = useSelectSource(siemsList, siemSelector, onSelectedSiemChangeHandler);

  return (
    <div className="source-selector" ref={selectRef}>
      <PopperWindow
        button={(
          <SelectSourceInput
            isOpen={selectOpen}
            inputValue={inputValue}
            handleClick={handleToggleSelect}
            handleInput={handleInput}
          />
        )}
        placement="bottom-start"
        open={selectOpen}
      >
        <SelectSourceMenu
          groupList={groupList}
          favoriteGroupList={favoriteGroupList}
          selectMenuOpen={selectMenuOpen}
          activeItems={activeItems}
          cursor={cursor}
          handleToggleSelectMenu={handleToggleSelectMenu}
          handleClickAddFavorite={handleClickAddFavorite}
          onSelectedSiemChangeHandler={onSelectedSiemChangeHandler}
          onSelectedGroupHandler={onSelectedGroupHandler}
          handleOnHoover={handleOnHoover}
          scrollRef={scrollRef}
        />
      </PopperWindow>
    </div>
  );
};
