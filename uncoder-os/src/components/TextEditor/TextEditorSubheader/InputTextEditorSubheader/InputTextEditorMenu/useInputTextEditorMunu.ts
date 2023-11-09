import { useDispatch, useSelector } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { setText, inputEditorTextSelector } from '../../../../../reduxData/inputEditor';
import { useInfoProvider } from '../../../../Info';

export const useInputTextEditorMenu = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const text = useSelector(inputEditorTextSelector);
  const { showSuccessMessage } = useInfoProvider();
  const copyTextHandler = async () => {
    await navigator.clipboard.writeText(text);
    showSuccessMessage('Text copied to clipboard');
  };

  const clearTextHandler = () => {
    dispatch(setText(''));
  };

  return {
    copyTextHandler,
    clearTextHandler,
  };
};
