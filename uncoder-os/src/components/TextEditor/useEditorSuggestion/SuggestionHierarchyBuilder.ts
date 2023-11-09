import { YamlNode } from './YamlNode';
import { SuggesterDictionaryResponse } from '../../../models/Providers/type';
import { GetSuggestionListType } from './types';

const emptySuggestionList: GetSuggestionListType = {
  title: '',
  dictionary: [],
};

export class SuggestionHierarchyBuilder {
  private nodeHierarchyStorage: YamlNode[] = [];

  private previousNode: YamlNode | undefined;

  private suggestionList: SuggesterDictionaryResponse;

  // eslint-disable-next-line no-useless-constructor
  constructor(suggestionList: SuggesterDictionaryResponse) {
    this.suggestionList = suggestionList;
  }

  public addRow = (row: string, rowNumber: number): void => {
    const currentNode = new YamlNode(row, rowNumber);
    if (
      this.nodeHierarchyStorage.length === 0
      || (
        this.previousNode
        && this.previousNode.offset > currentNode.offset
      )
    ) {
      this.nodeHierarchyStorage.push(currentNode);
      this.previousNode = currentNode;
    }
  };

  private addSuggestionsToNodes = (): void => {
    this.nodeHierarchyStorage.forEach((node) => {
      for (let i = 0; i < this.suggestionList.length; i++) {
        const oneSuggestion = this.suggestionList[i];
        if (node.value.search(new RegExp(oneSuggestion.sectionRegExp)) === 0) {
          node.suggestions = {
            title: oneSuggestion.title,
            dictionary: oneSuggestion.dictionary,
          };
        }
      }
    });
  };

  public getSuggestions = (): GetSuggestionListType => {
    this.addSuggestionsToNodes();
    for (let i = 0; i < this.nodeHierarchyStorage.length; i++) {
      if (this.nodeHierarchyStorage[i].suggestions) {
        return this.nodeHierarchyStorage[i].suggestions as GetSuggestionListType;
      }
    }

    return emptySuggestionList;
  };
}
