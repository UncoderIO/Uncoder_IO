import { useDispatch, useSelector } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { inputEditorSelector, setText } from '../../reduxData/inputEditor';
import { iocSettingsSelector } from '../../reduxData/iocSettings';
import { applyCustomFilterForRawIocs } from '../../tools/applyCustomFilterForRawIocs';
import { EditorValueTypes } from '../../types/editorValueTypes';

export const useInputTextWithFilters = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const { iocParsingRules } = useSelector(iocSettingsSelector);
  const { platformCode: parser } = useSelector(inputEditorSelector);

  const setTextWithFilters = (value: string) => {
    if (iocParsingRules.length && parser === EditorValueTypes.ioc) {
      value = applyCustomFilterForRawIocs(value, iocParsingRules);
    }

    dispatch(setText(value));
  };

  return {
    setText: setTextWithFilters,
  };
};
