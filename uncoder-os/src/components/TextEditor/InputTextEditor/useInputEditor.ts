import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { clearText, inputEditorSelector } from '../../../reduxData/inputEditor';

import ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/ext-language_tools';
import { loadSuggesterData, suggesterSelector } from '../../../reduxData/suggester';
import { useEditorSuggestion } from '../useEditorSuggestion';
import { EditorValueTypes } from '../../../types/editorValueTypes';
import { useDetectParserByText } from '../../../hooks';
import { useInputTextWithFilters } from '../../../hooks/useInputTextWithFilters';
import { iocParsingRulesSelector } from '../../../reduxData/iocSettings';

const defineMode = (parser: EditorValueTypes) => {
  if ([EditorValueTypes.sigma, EditorValueTypes.roota].includes(parser)) {
    return 'yaml';
  }

  if (parser === EditorValueTypes.ioc) {
    return 'uncodercti';
  }

  return 'text';
};

export const useInputEditor = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const { text: inputText, platformCode: parser, changed } = useSelector(inputEditorSelector);
  const suggestionData = useSelector(suggesterSelector);
  const iocParsingRules = useSelector(iocParsingRulesSelector);
  const { languageCompleter } = useEditorSuggestion(suggestionData);
  const { detectParser } = useDetectParserByText();
  const { setText } = useInputTextWithFilters();

  useEffect(() => {
    const langTools = ace.require('ace/ext/language_tools');
    if (![EditorValueTypes.sigma, EditorValueTypes.roota].includes(parser)) {
      langTools.setCompleters([langTools.textCompleter]);
      return;
    }

    if (suggestionData.length) {
      langTools.setCompleters([langTools.textCompleter, languageCompleter]);
    } else {
      dispatch(loadSuggesterData());
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [parser, suggestionData.toString()]);

  const isIoc = parser === EditorValueTypes.ioc;

  const onChangeInputText = (value: string) => {
    setText(value);
  };

  const onFocusInputText = () => {
    if (changed) {
      return;
    }
    dispatch(clearText());
  };

  const onPasteInputText = (value: string) => {
    detectParser(value);
  };

  useEffect(
    () => {
      if (changed && isIoc) {
        setText(inputText);
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [iocParsingRules.toString(), isIoc],
  );

  return {
    isIoc,
    inputText,
    mode: defineMode(parser),
    onChangeInputText,
    onFocusInputText,
    onPasteInputText,
  };
};
