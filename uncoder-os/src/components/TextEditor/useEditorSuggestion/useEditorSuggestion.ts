import { Ace } from 'ace-builds';
import { SuggesterDictionaryItem, SuggesterDictionaryResponse } from '../../../models/Providers/type';
import { GetSuggestionListType } from './types';
import { SuggestionHierarchyBuilder } from './SuggestionHierarchyBuilder';

const getSuggestionList = (
  suggestionRow: number,
  editorSession: Ace.EditSession,
  editorSuggestion: SuggesterDictionaryResponse,
): GetSuggestionListType => {
  const suggestionHierarchyBuilder = new SuggestionHierarchyBuilder(editorSuggestion);
  for (let i = suggestionRow; i >= 0; i--) {
    suggestionHierarchyBuilder.addRow(editorSession.getLine(i), i);
  }

  return suggestionHierarchyBuilder.getSuggestions();
};

export const useEditorSuggestion = (suggestionList: SuggesterDictionaryResponse) => {
  const languageCompleter = {
    getCompletions: (
      editor: Ace.Editor,
      session: Ace.EditSession,
      pos: Ace.Point,
      prefix: string,
      callback: Ace.CompleterCallback,
    ): void => {
      const suggester = getSuggestionList(pos.row, session, suggestionList);

      if (suggester?.dictionary?.length) {
        callback(
          null,
          suggester.dictionary.map((table: SuggesterDictionaryItem) => ({
            caption: `${table.name}: ${table.description}`,
            value: table.name,
            meta: suggester.title,
            score: 10000,
          } as Ace.Completion)),
        );
      } else {
        callback(
          null,
          // @ts-ignore
          suggester?.dictionary,
        );
      }
    },
  };

  return {
    languageCompleter,
  };
};
