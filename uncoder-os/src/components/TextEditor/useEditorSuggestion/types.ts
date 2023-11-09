import { SuggesterDictionaryItem } from '../../../models/Providers/type';

export type GetSuggestionListType = {
  title: string,
  dictionary: SuggesterDictionaryItem[],
};

export enum NodeType {
  item = 'item',
  field = 'field',
  root = 'root',
}

export type YamlNodeItem = {
  type: NodeType,
  value: string,
  rowNumber: number,
  offset: number,
  suggestions?: GetSuggestionListType,
}
