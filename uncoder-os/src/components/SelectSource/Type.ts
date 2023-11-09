import { RefObject } from 'react';
import { GroupListType, GroupPlatformType } from '../../tools';
import { PlatformData } from '../../models/Providers/type';

export type SelectSourceType = {
    siemsList: SiemsListType;
    siemSelector: string;
    onSelectedSiemChangeHandler: (newSiem: GroupPlatformType | GroupListType) => () => void;
    error?: boolean;
    helperText?: string | boolean;
};

export type SelectedMenuState = number | null;

export type SelectSourceMenuType = {
    selectRef: RefObject<HTMLDivElement>,
    selectOpen: boolean;
    selectMenuOpen: SelectedMenuState;
    handleToggleSelect: (state: boolean) => () => void;
    handleToggleSelectMenu: (selected: SelectedMenuState) => () => void;
    handleClickAddFavorite: (newSiem: GroupListType) => () => void;
    onSelectedGroupHandler: (newSiem: GroupListType) => () => void;
};

export type SelectedItems = {
    selectedGroup: string,
    selectedPlatform: string,
};

export type SiemsListType = PlatformData[];
