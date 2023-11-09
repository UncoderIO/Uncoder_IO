import { ApiCoreProvider } from './ApiCoreProvider';
import {
  TranslateAllRequest,
  TranslateRequest,
  PlatformsResponse,
  TranslateAllResponse,
  TranslateResponse,
  TranslateIocRequest,
  TranslateIocResponse,
  SuggesterDictionaryResponse,
} from '../type';

export class ApiProvider extends ApiCoreProvider {
  async translate(requestData: TranslateRequest): Promise<TranslateResponse> {
    return this.postJsonResource<TranslateResponse, TranslateRequest>('/translate', requestData);
  }

  async translateAll(requestData: TranslateAllRequest): Promise<TranslateAllResponse> {
    return this.postJsonResource<TranslateAllResponse, TranslateAllRequest>('/translate/all', requestData);
  }

  async translateIoc(requestData: TranslateIocRequest): Promise<TranslateIocResponse> {
    return this.postJsonResource<TranslateIocResponse, TranslateIocRequest>('/iocs/translate', requestData);
  }

  async getPlatforms(): Promise<PlatformsResponse> {
    return this.getResource<PlatformsResponse>('/all_platforms');
  }

  async getSuggestDictionary(parser: string): Promise<SuggesterDictionaryResponse> {
    return this.getResource<SuggesterDictionaryResponse>(`/suggestions/${parser}`);
  }
}
