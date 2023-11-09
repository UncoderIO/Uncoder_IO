import { useDispatch, useSelector } from 'react-redux';
import { outputEditorTextSelector, setText } from '../../../reduxData/outputEditor';
import { Dispatch } from '@reduxjs/toolkit';

export const useOutputTextEditor = () => {
  const outputText = useSelector(outputEditorTextSelector);
  const dispatch = useDispatch<Dispatch<any>>();
  const onChangeText = (value: string) => {
    dispatch(setText(value));
  };

  return {
    outputText,
    onChangeText,
  };
};
