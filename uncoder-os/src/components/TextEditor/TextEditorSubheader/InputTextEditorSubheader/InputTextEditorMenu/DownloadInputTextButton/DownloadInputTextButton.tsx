import React, { FC } from 'react';
import { Button } from '../../../../../Buttons';
import { ReactComponent as DownloadIcon } from '../../../../../../assets/svg/DownloadIcon.svg';
import { useSelector } from 'react-redux';
import { inputEditorTextSelector } from '../../../../../../reduxData/inputEditor';
import { downloadFile } from '../../../../../../tools';

export const DownloadInputTextButton: FC = () => {
  const inputText = useSelector(inputEditorTextSelector);

  const downloadText = () => {
    downloadFile('uncoder-input-content.txt', inputText);
  };

  if (!inputText.length) {
    return null;
  }

  return <Button
    classes="button--icon button--xs button--default m-r-6"
    children={<DownloadIcon />}
    aria-label="input-copy"
    type="button"
    onClick={downloadText}
  />;
};
