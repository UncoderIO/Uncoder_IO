import { useDispatch, useSelector } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import {
  inputEditorSelector,
  setText,
} from '../../../reduxData/inputEditor';
import { useEffect } from 'react';

import ace from 'ace-builds';
import 'ace-builds/src-noconflict/ext-language_tools';
import { loadSuggesterData, suggesterSelector } from '../../../reduxData/suggester';
import { useEditorSuggestion } from '../useEditorSuggestion';

const defineMode = (parser: string) => {
  if (['sigma', 'roota'].includes(parser)) {
    return 'yaml';
  }

  if (parser === 'ioc') {
    return 'uncodercti';
  }

  return 'text';
};
export const useInputEditor = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const { text: inputText, platformCode: parser, changed } = useSelector(inputEditorSelector);
  const suggestionData = useSelector(suggesterSelector);
  const { languageCompleter } = useEditorSuggestion(suggestionData);

  useEffect(() => {
    const langTools = ace.require('ace/ext/language_tools');
    if (!['sigma', 'roota'].includes(parser)) {
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

  const onChangeInputText = (value: string) => {
    dispatch(setText(value));
  };

  const onFocusInputText = () => {
    if (changed) {
      return;
    }
    dispatch(setText(''));
  };

  return {
    isIoc: parser === 'ioc',
    inputText,
    mode: defineMode(parser),
    onChangeInputText,
    onFocusInputText,
  };
};
