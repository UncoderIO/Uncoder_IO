import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { parsersSelector, renderersSelector, setPlatforms } from '../../../../reduxData/platforms';
import { Dispatch } from '@reduxjs/toolkit';
import {
  inputEditorPlatformCodeSelector,
  setPlatformCode as setInputPlatformCode,
} from '../../../../reduxData/inputEditor';
import {
  setText as setOutputText,
  setPlatformCode as setOutputPlatformCode, outputEditorPlatformCodeSelector,
} from '../../../../reduxData/outputEditor';
import { EditorValueTypes } from '../../../../types/editorValueTypes';

export const useInputTextEditorHeader = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const renderers = useSelector(renderersSelector);
  const outputPlatform = useSelector(outputEditorPlatformCodeSelector);
  const parsers = useSelector(parsersSelector);
  const parser = useSelector(inputEditorPlatformCodeSelector);

  useEffect(() => {
    dispatch(setPlatforms());
  }, [dispatch]);

  const onChangeParser = (id: EditorValueTypes) => {
    dispatch(setInputPlatformCode(id));
    dispatch(setOutputText(''));
  };

  useEffect(() => {
    if (!renderers.filter((renderer) => renderer.id === outputPlatform).length) {
      dispatch(setOutputPlatformCode(EditorValueTypes.none));
    }
  }, [parser]);

  return {
    parsers,
    onChangeParser,
    parser,
  };
};
