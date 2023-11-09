import { BasicIocType, HashIocType, IocParsingRulesType } from '../../../types/iocsTypes';

export type TranslateAllRequest = {
  source_siem: string,
  source_scheme?: string,
  text: string,
}

export type TranslateRequest = TranslateAllRequest & {
  target_siem: string,
  target_scheme?: string,
}

export type PlatformForIoc = {
  name: string,
}

export type TranslateIocRequest = {
  text: string,
  platform: PlatformForIoc,
  iocs_per_query: number,
  include_ioc_types: BasicIocType[],
  include_hash_types: HashIocType[],
  exceptions: string[],
  ioc_parsing_rules: IocParsingRulesType[],
  include_source_ip: boolean,
}
