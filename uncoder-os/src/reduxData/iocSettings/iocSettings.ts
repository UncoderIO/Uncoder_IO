import type { CaseReducer, PayloadAction } from '@reduxjs/toolkit';
import { createSelector, createSlice } from '@reduxjs/toolkit';
import { IocSettingsStateType, RootState } from '../RootStore';
import { BasicIocType, IocParsingRulesType } from '../../types/iocsTypes';

type IocSettingsReducers = {
  setIocPerQuery: CaseReducer<IocSettingsStateType, PayloadAction<number>>;
  setIncludeIocTypes: CaseReducer<IocSettingsStateType, PayloadAction<IocSettingsStateType['includeIocTypes']>>;
  setIncludeHashTypes: CaseReducer<IocSettingsStateType, PayloadAction<IocSettingsStateType['includeHashTypes']>>;
  setExceptions: CaseReducer<IocSettingsStateType, PayloadAction<IocSettingsStateType['exceptions']>>;
  setParsingRules: CaseReducer<IocSettingsStateType, PayloadAction<IocSettingsStateType['iocParsingRules']>>;
  setIncludeSourceIp: CaseReducer<IocSettingsStateType, PayloadAction<IocSettingsStateType['includeSourceIp']>>;
  setIocsSettings: CaseReducer<IocSettingsStateType, PayloadAction<IocSettingsStateType>>;
  setToDefault: CaseReducer<IocSettingsStateType>;
};

const initialState: IocSettingsStateType = {
  iocPerQuery: 25,
  includeIocTypes: [
    BasicIocType.Domain,
    BasicIocType.Ip,
    BasicIocType.Url,
    BasicIocType.Hash,
  ],
  includeHashTypes: [],
  exceptions: '',
  iocParsingRules: [
    IocParsingRulesType.RemovePrivateAndReservedIps,
    IocParsingRulesType.ReplaseHXXP,
    IocParsingRulesType.ReplaseDots,
  ],
  includeSourceIp: false,
};

const iocSettingsSlice = createSlice<IocSettingsStateType, IocSettingsReducers>({
  name: 'iocSettings',
  initialState,
  reducers: {
    setIocPerQuery: (state, action) => {
      state.iocPerQuery = action.payload;
    },
    setIncludeIocTypes: (state, action) => {
      state.includeIocTypes = action.payload;
    },
    setIncludeHashTypes: (state, action) => {
      state.includeHashTypes = action.payload;
    },
    setExceptions: (state, action) => {
      state.exceptions = action.payload;
    },
    setIncludeSourceIp: (state, action) => {
      state.includeSourceIp = action.payload;
    },
    setParsingRules: (state, action) => {
      state.iocParsingRules = action.payload;
    },
    setIocsSettings: (state, action) => {
      state.iocPerQuery = action.payload.iocPerQuery;
      state.includeIocTypes = action.payload.includeIocTypes;
      state.includeHashTypes = action.payload.includeHashTypes;
      state.exceptions = action.payload.exceptions;
      state.iocParsingRules = action.payload.iocParsingRules;
    },
    setToDefault: () => initialState,
  },
});

const { actions, reducer } = iocSettingsSlice;

const selectSelf = (state: RootState) => state;
export const iocSettingsSelector = createSelector(
  selectSelf,
  (state: RootState): IocSettingsStateType => state.iocSettings,
);

export const {
  setIocPerQuery,
  setIncludeIocTypes,
  setIncludeHashTypes,
  setExceptions,
  setIncludeSourceIp,
  setParsingRules,
  setIocsSettings,
} = actions;

export default reducer;
