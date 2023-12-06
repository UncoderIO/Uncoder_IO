import { useDispatch, useSelector } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { clearText, inputEditorTextSelector } from '../../../../../reduxData/inputEditor';
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
    dispatch(clearText());
  };

  return {
    copyTextHandler,
    clearTextHandler,
  };
};
