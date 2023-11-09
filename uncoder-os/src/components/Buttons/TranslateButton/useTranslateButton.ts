import { translateIocsFromInputEditor, translateTextFromInputEditor } from '../../../reduxData/outputEditor';
import { useDispatch, useSelector } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { inputEditorPlatformCodeSelector } from '../../../reduxData/inputEditor';

export const useTranslateButton = () => {
  const parser = useSelector(inputEditorPlatformCodeSelector);
  const dispatch = useDispatch<Dispatch<any>>();
  const onClickHandler = async () => {
    if (parser === 'ioc') {
      dispatch(translateIocsFromInputEditor());
      return;
    }

    dispatch(translateTextFromInputEditor());
  };

  return {
    onClickHandler,
  };
};
