import { useSelector, useDispatch } from 'react-redux';
import { renderersSelector } from '../../../../reduxData/platforms';
import { Dispatch } from '@reduxjs/toolkit';

import {
  outputEditorPlatformCodeSelector,
  setPlatformCode as setOutputPlatformCode,
} from '../../../../reduxData/outputEditor';
import { inputEditorPlatformCodeSelector } from '../../../../reduxData/inputEditor';
import { EditorValueTypes } from '../../../../types/editorValueTypes';

export const useOutputTextEditorHeader = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const renderers = useSelector(renderersSelector);
  const renderer = useSelector(outputEditorPlatformCodeSelector);
  const parser = useSelector(inputEditorPlatformCodeSelector);

  const onChangeRenderer = (id: string) => {
    dispatch(setOutputPlatformCode(id as EditorValueTypes));
  };

  return {
    renderers,
    onChangeRenderer,
    renderer,
    isIocMode: parser === EditorValueTypes.ioc,
  };
};
