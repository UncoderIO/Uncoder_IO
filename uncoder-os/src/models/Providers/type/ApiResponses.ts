import { Severity } from '../../../enums';

export type InfoMessage = {
  message: string,
  severity: Severity,
};

export type ResultStatusContext = {
  status: boolean,
  info: InfoMessage | null,
};

export type TranslateItem = ResultStatusContext & {
  translation: string,
  target_siem_type: string,
  target_siem_name: string
};

export type PlatformItem = {
  id: string,
  name: string,
};

export type TranslateResponse = TranslateItem;

export type TranslateAllResponse = TranslateItem[];

export type PlatformData = {
  id: string;
  name: string;
  code: string;
  group_name: string;
  group_id: string;
  platform_name?: string;
  platform_id?: string;
  alt_platform?: string;
  alt_platform_name?: string;
  first_choice?: number;
};

export type ParserPlatformData = PlatformData & {
  renders: PlatformData[],
  parsers?: PlatformData[] | null,
};

export type PlatformsResponse = ParserPlatformData[];

export type IocTranslationData = {
  target_siem_type: string,
  translations: string[],
}

export type TranslateIocResponse = ResultStatusContext & IocTranslationData;

export type SuggesterDictionaryItem = {
  name: string,
  description: string,
};

export type SuggesterDictionaryResponse = {
  title: string,
  sectionRegExp: string,
  dictionary: SuggesterDictionaryItem[]
}[]
