import { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { parsersSelector, setPlatforms } from '../../../../reduxData/platforms';
import { Dispatch } from '@reduxjs/toolkit';
import {
  inputEditorPlatformCodeSelector,
  setPlatformCode as setInputPlatformCode,
} from '../../../../reduxData/inputEditor';
import {
  setText as setOutputText,
  setPlatformCode as setOutputPlatformCode,
} from '../../../../reduxData/outputEditor';

export const useInputTextEditorHeader = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const parsers = useSelector(parsersSelector);
  const parser = useSelector(inputEditorPlatformCodeSelector);

  useEffect(() => {
    dispatch(setPlatforms());
  }, [dispatch]);

  const onChangeParser = (id: string) => {
    dispatch(setInputPlatformCode(id));
    dispatch(setOutputPlatformCode('none'));
    dispatch(setOutputText(''));
  };

  return {
    parsers,
    onChangeParser,
    parser,
  };
};
