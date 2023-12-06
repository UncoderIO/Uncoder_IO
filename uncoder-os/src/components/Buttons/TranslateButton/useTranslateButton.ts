import { translateIocsFromInputEditor, translateTextFromInputEditor } from '../../../reduxData/outputEditor';
import { useDispatch, useSelector } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { inputEditorPlatformCodeSelector } from '../../../reduxData/inputEditor';
import { EditorValueTypes } from '../../../types/editorValueTypes';
import { iocSettingsSelector } from '../../../reduxData/iocSettings';

export const useTranslateButton = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const parser = useSelector(inputEditorPlatformCodeSelector);
  const { includeIocTypes } = useSelector(iocSettingsSelector);

  const onClickHandler = async () => {
    if (parser === EditorValueTypes.ioc) {
      dispatch(translateIocsFromInputEditor());
      return;
    }

    dispatch(translateTextFromInputEditor());
  };

  const isActive = includeIocTypes.length > 0 || parser !== 'ioc';

  const disabledMessage = 'IOC Types is not specified';

  return {
    isActive,
    disabledMessage,
    onClickHandler,
  };
};
