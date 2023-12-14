import React, { FC } from 'react';
import { Button } from '../../../../../Buttons';
import { Tooltip } from '../../../../../Tooltip';
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

  return (
    <Tooltip classes="d-block m-r-6" content="Download">
      <Button
        classes="button--icon button--xs button--default"
        children={<DownloadIcon />}
        aria-label="input-download"
        type="button"
        onClick={downloadText}
      />
    </Tooltip>
  );
};
