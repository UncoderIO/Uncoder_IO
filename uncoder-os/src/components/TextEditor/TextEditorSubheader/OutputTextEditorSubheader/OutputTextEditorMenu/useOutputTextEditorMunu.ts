import { useDispatch, useSelector } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { clearText, outputEditorTextSelector } from '../../../../../reduxData/outputEditor';
import { useInfoProvider } from '../../../../Info';

export const useOutputTextEditorMenu = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const text = useSelector(outputEditorTextSelector);
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
