import {
  createRef, RefObject, SyntheticEvent, useEffect, useRef, useState,
} from 'react';
import {
  SelectedItems, SelectedMenuState, SelectSourceType, SiemsListType,
} from '../Type';
import { useHandleClickOutside } from '../../../hooks';
import { convertSiemsListToGroupStructure, GroupListType } from '../../../tools';
import { PlatformData } from '../../../models/Providers/type';

const favoritePlatforms: any[] = [];

const getActiveItemsIds = (siemsList: SiemsListType, siemSelector: string): SelectedItems => {
  const selectedItem = siemsList.find((item) => item.id === siemSelector);

  if (!selectedItem) {
    return {
      selectedGroup: 'none',
      selectedPlatform: 'none',
    };
  }

  return {
    selectedGroup: selectedItem.group_id,
    selectedPlatform: siemSelector,
  };
};

export const getSiemTitleById = (platformData?: PlatformData[]) => (id: string): string => {
  const platformDataItem = platformData?.find((item) => item.id === id);

  if (['none', 'ioc', 'sigma', 'roota'].includes(id)) {
    return platformDataItem?.group_name ?? '';
  }

  return `${platformDataItem?.group_name} ${platformDataItem?.platform_name}${platformDataItem?.alt_platform !== 'regular' ? (` ${platformDataItem?.alt_platform_name}`) : ''}`;
};

export const useSelectSource = (
  siemsList: SiemsListType,
  siemSelector: string,
  onSelectedSiemChangeHandler: SelectSourceType['onSelectedSiemChangeHandler'],
) => {
  const [selectOpen, setSelectOpen] = useState<boolean>(false);
  const [selectMenuOpen, setSelectMenuOpen] = useState<SelectedMenuState>(null);
  const [inputValue, setInputValue] = useState('');
  const [filterValue, setFilterValue] = useState<string | undefined>(undefined);
  const [elRefs, setElRefs] = useState<RefObject<HTMLDivElement>[]>([]);
  const [cursor, setCursor] = useState<number | undefined>();
  const scrollRef = useRef<HTMLDivElement>(null);
  const selectRef = createRef<HTMLDivElement>();

  const valueLabel = getSiemTitleById(siemsList)(siemSelector);

  useEffect(() => {
    setInputValue(valueLabel);
  }, [valueLabel]);

  const handleInput = (e: SyntheticEvent) => {
    // @ts-ignore
    setInputValue(e.target?.value);
    // @ts-ignore
    setFilterValue(e.target?.value);
  };

  useEffect(() => {
    setSelectMenuOpen(null);
  }, [siemSelector]);

  const handleToggleSelect = (state: boolean) => () => {
    if (!state) {
      setSelectMenuOpen(null);
      setFilterValue(undefined);
      // setInputValue(valueLabel);
      setCursor(undefined);
    }
    setSelectOpen(state);
  };

  const handleToggleSelectMenu = (selected: SelectedMenuState) => () => {
    setSelectMenuOpen((state) => (state === selected ? null : selected));
  };

  const handleClickAddFavorite = () => () => {
    // todo: implement favorite logic
  };
  const onSelectedGroupHandler = (value: GroupListType) => () => {
    setSelectMenuOpen(null);
    setFilterValue(undefined);

    if (value.data) {
      const [groupId, platformId] = value.data.reduce((acc, item, currentIndex) => {
        if (item.data.length) {
          const currentPlatformId = item
            .data
            .reduce((result: undefined | number, platformItem, currentPlatformIndex) => {
              if (platformItem.firstChoice) {
                return currentPlatformIndex;
              }

              return result;
            }, undefined);

          if (typeof currentPlatformId !== 'undefined') {
            return [currentIndex, currentPlatformId];
          }
        }
        return acc;
      }, [0, 0]);

      onSelectedSiemChangeHandler(value.data[groupId].data[platformId])();

      return;
    }
    onSelectedSiemChangeHandler({ id: value.id, name: value.name, code: value.id })();
  };

  useHandleClickOutside(
    selectRef,
    handleToggleSelect(false),
  );

  const filterGroup = ():SiemsListType => {
    if (typeof filterValue === 'undefined') {
      return siemsList;
    }

    return siemsList?.filter((item) => (
      item.group_name.toLowerCase().includes(filterValue?.toLowerCase())
      || item?.platform_name?.toLowerCase().includes(filterValue?.toLowerCase())
      || item?.alt_platform_name?.toLowerCase().includes(filterValue?.toLowerCase())
    )
      && item.group_id !== 'none');
  };

  const groupStructure = convertSiemsListToGroupStructure(filterGroup());

  const structureLength = groupStructure?.length;

  useEffect(() => {
    // add or remove refs
    setElRefs((elRefsItem) => Array(structureLength)
      .fill(undefined)
      .map((_, i) => elRefsItem[i] || createRef()));
  }, [structureLength]);

  const favoriteGroupList = groupStructure?.filter((item) => favoritePlatforms.includes(item.id))
    .map((item, index) => {
      item.ref = elRefs[index];

      return item;
    });

  const favoriteCount = favoriteGroupList?.length ?? 0;

  const groupList = groupStructure?.filter((item) => !favoritePlatforms.includes(item.id))
    .map((item, index) => {
      item.ref = elRefs[index + favoriteCount];

      return item;
    });

  const handleOnHoover = (elementIndex: number) => () => { setCursor(elementIndex); };

  return {
    selectRef,
    selectOpen,
    selectMenuOpen,
    activeItems: getActiveItemsIds(siemsList, siemSelector),
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
  };
};
