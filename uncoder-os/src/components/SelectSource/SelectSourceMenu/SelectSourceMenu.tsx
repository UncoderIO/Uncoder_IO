import React, { RefObject } from 'react';
import SimpleBar from 'simplebar-react';
import { SelectSourceMenuItem } from './SelectSourceMenuItem';
import { SelectSourceSubMenu } from '../SelectSourceSubMenu';
import { GroupListType } from '../../../tools';

import { SelectedItems, SelectSourceMenuType, SelectSourceType } from '../Type';

import 'simplebar-react/dist/simplebar.min.css';
import './SelectSourceMenu.sass';

interface SourceSelectorMenuProps extends Omit<SelectSourceType, 'siemSelector' | 'siemsList'> {
  selectMenuOpen: SelectSourceMenuType['selectMenuOpen'];
  handleToggleSelectMenu: SelectSourceMenuType['handleToggleSelectMenu'];
  handleClickAddFavorite: SelectSourceMenuType['handleClickAddFavorite'];
  onSelectedGroupHandler: SelectSourceMenuType['onSelectedGroupHandler'];
  activeItems: SelectedItems;
  favoriteGroupList: GroupListType[] | undefined;
  groupList: GroupListType[] | undefined;
  handleOnHoover: (index: number) => () => void;
  cursor?: number
  hotkeyHandler?: (event: KeyboardEvent | React.KeyboardEvent<HTMLElement>) => void;
  scrollRef?: RefObject<HTMLDivElement>;
}

export const SelectSourceMenu: React.FC <SourceSelectorMenuProps> = ({
  groupList,
  selectMenuOpen,
  handleToggleSelectMenu,
  handleClickAddFavorite,
  onSelectedSiemChangeHandler,
  onSelectedGroupHandler,
  activeItems,
  favoriteGroupList,
  handleOnHoover,
  cursor,
  hotkeyHandler,
  scrollRef,
}) => {
  if (!groupList?.length && !favoriteGroupList?.length) {
    return null;
  }

  const favoriteLength = favoriteGroupList?.length ?? 0;

  return (
    <div
      className="source-selector-menu"
      onMouseMove={() => {
        if (typeof scrollRef?.current?.style.pointerEvents !== 'undefined') {
          scrollRef.current.style.pointerEvents = 'inherit';
        }
      }}
    >
      <SimpleBar
        className="source-selector-menu__scroll"
        onKeyDown={hotkeyHandler}
        scrollableNodeProps={{
          ref: scrollRef,
        }}
      >
        {
          !!favoriteGroupList?.length && (
            <div className="source-selector-menu__list">
              <div className="source-selector-menu__title m-b-2">
                Favorite platforms (${favoriteGroupList.length})
              </div>
              {
                favoriteGroupList?.map((item, index) => (
                  <div
                    className={`
                      source-selector-menu__item
                      ${(activeItems.selectedGroup === item.id || selectMenuOpen === index) ? ' is-active' : ''}
                      ${cursor === index ? ' is-hovered' : ''}
                    `}
                    onMouseOver={handleOnHoover(index)}
                    key={item.id}
                    ref={item?.ref}
                  >
                    <SelectSourceMenuItem
                      id={index}
                      isActive={selectMenuOpen === (index)}
                      option={item}
                      isCheck
                      handleClickAddFavorite={handleClickAddFavorite}
                      handleToggleSelectMenu={handleToggleSelectMenu}
                      handleClick={onSelectedGroupHandler}
                    />
                    {
                      item?.data && (
                        <SelectSourceSubMenu
                          id={index}
                          isActive={selectMenuOpen === (index)}
                          handleClick={onSelectedSiemChangeHandler}
                          data={item.data}
                        />
                      )
                    }
                  </div>
                ))
              }
            </div>
          )
        }
        {
          groupList?.map((item, index) => (
            <div
              className={`
                source-selector-menu__item
                ${(activeItems.selectedGroup === item.id || selectMenuOpen === (index + favoriteLength)) ? ' is-active' : ''}
                ${cursor === (index + favoriteLength) ? ' is-hovered' : ''}
              `}
              onMouseOver={handleOnHoover(index + favoriteLength)}
              key={item.id}
              ref={item?.ref}
            >
              <SelectSourceMenuItem
                id={index + favoriteLength}
                isActive={selectMenuOpen === (index + favoriteLength)}
                option={item}
                handleClickAddFavorite={handleClickAddFavorite}
                handleToggleSelectMenu={handleToggleSelectMenu}
                handleClick={onSelectedGroupHandler}
                disableAddToFavorite
              />
              {
                item?.data && (
                  <SelectSourceSubMenu
                    id={index + favoriteLength}
                    isActive={selectMenuOpen === (index + favoriteLength)}
                    handleClick={onSelectedSiemChangeHandler}
                    data={item.data}
                  />
                )
              }
            </div>
          ))
        }
      </SimpleBar>
    </div>
  );
};
