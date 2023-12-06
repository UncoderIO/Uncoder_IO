import React, { FC } from 'react';
import { useInputEditorFileUploadButton } from './useInputEditorFileUploadButton';
import { FileUploader } from '../FileUploader';
import { Button } from '../../Buttons';
import { Tooltip } from '../../Tooltip';
import { ReactComponent as UploadIcon } from '../../../assets/svg/UploadIcon.svg';

export const InputEditorFileUploadButton: FC = () => {
  const { uploadHandler } = useInputEditorFileUploadButton();

  return (
    <FileUploader
      handleFile={uploadHandler}
      accept=".csv,.json,.txt"
    >
      <Tooltip content="Upload IOCs" positionStrategy="fixed">
        <Button classes="button--icon button--xs button--default button--bg m-r-6" aria-label="input-upload" type="button">
          <UploadIcon />
        </Button>
      </Tooltip>
    </FileUploader>
  );
};
