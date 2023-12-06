import React, { FC } from 'react';
import { Button } from '../../../../../Buttons';
import { Tooltip } from '../../../../../Tooltip';
import { ReactComponent as DownloadIcon } from '../../../../../../assets/svg/DownloadIcon.svg';
import { useSelector } from 'react-redux';
import { downloadFile } from '../../../../../../tools';
import { outputEditorTextSelector } from '../../../../../../reduxData/outputEditor';

export const DownloadOutputTextButton: FC = () => {
  const output = useSelector(outputEditorTextSelector);

  const downloadText = () => {
    downloadFile('uncoder-output-content.txt', output);
  };

  if (!output?.length) {
    return null;
  }

  return (
    <Tooltip classes="m-r-6" content="Download">
      <Button
        classes="button--icon button--xs button--default"
        children={<DownloadIcon />}
        aria-label="output-download"
        type="button"
        onClick={downloadText}
      />
    </Tooltip>
  );
};
