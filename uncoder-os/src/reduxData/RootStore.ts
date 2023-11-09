import { Reducer } from '@reduxjs/toolkit';
import { StateFromReducersMapObject } from 'redux';
import { PlatformsResponse, SuggesterDictionaryResponse } from '../models/Providers/type';
import { BasicIocType, HashIocType, IocParsingRulesType } from '../types/iocsTypes';
import { Severity } from '../enums';

export type UncoderEditorStateType = {
  text: string;
  platformCode: string;
};

export type InputEditorStateType = UncoderEditorStateType & { changed: boolean };
export type OutputEditorStateType = UncoderEditorStateType;
export type PlatformsStateType = {
  data?: PlatformsResponse
};

export type IocSettingsStateType = {
  iocPerQuery: number;
  includeIocTypes: BasicIocType[];
  includeHashTypes: HashIocType[];
  exceptions: string;
  iocParsingRules: IocParsingRulesType[];
  includeSourceIp: boolean;
}

export type InfoStateType = {
  severity: Severity;
  isVisible: boolean;
  message: string;
}

export type SuggesterStateType = {
  data: {
    parser: string;
    suggesterData: SuggesterDictionaryResponse
  }[]
};

export type RootStore = {
  inputEditor: Reducer<InputEditorStateType>;
  outputEditor: Reducer<OutputEditorStateType>;
  platforms: Reducer<PlatformsStateType>;
  iocSettings: Reducer<IocSettingsStateType>;
  info: Reducer<InfoStateType>;
  suggester: Reducer<SuggesterStateType>;
};

export type RootState = StateFromReducersMapObject<RootStore>;
