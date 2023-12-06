import { ChangeEvent, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { parsersSelector, renderersSelector, setPlatforms } from '../../../reduxData/platforms';
import { Dispatch } from '@reduxjs/toolkit';
import {
  inputEditorPlatformCodeSelector,
  setPlatformCode as setInputPlatformCode,
} from '../../../reduxData/inputEditor';
import {
  outputEditorPlatformCodeSelector,
  setPlatformCode as setOutputPlatformCode,
} from '../../../reduxData/outputEditor';
import { EditorValueTypes } from '../../../types/editorValueTypes';

export const useTextEditorHeader = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const parsers = useSelector(parsersSelector);
  const renderers = useSelector(renderersSelector);
  const parser = useSelector(inputEditorPlatformCodeSelector);
  const renderer = useSelector(outputEditorPlatformCodeSelector);

  useEffect(() => {
    dispatch(setPlatforms());
  }, [dispatch]);

  const onChangeParser = (event: ChangeEvent) => {
    dispatch(setInputPlatformCode((event.target as HTMLInputElement).value as EditorValueTypes));
  };

  const onChangeRenderer = (event: ChangeEvent) => {
    dispatch(setOutputPlatformCode((event.target as HTMLInputElement).value as EditorValueTypes));
  };

  return {
    parsers: [...parsers, { id: EditorValueTypes.ioc, name: 'IOC' }],
    renderers,
    onChangeParser,
    onChangeRenderer,
    parser,
    renderer,
  };
};
