import React, { FC } from 'react';
import { Button } from '../../../../Buttons';
import { Tooltip } from '../../../../Tooltip';
import { ReplaceSettingsButton } from './ReplaseSettingsButton';
import { DownloadInputTextButton } from './DownloadInputTextButton';
import { useInputTextEditorMenu } from './useInputTextEditorMunu';

import { ReactComponent as CopyIcon } from '../../../../../assets/svg/CopyIcon.svg';
import { ReactComponent as DeleteIcon } from '../../../../../assets/svg/DeleteIcon.svg';

import './InputTextEditorMenu.sass';

export const InputTextEditorMenu: FC = () => {
  const { copyTextHandler, clearTextHandler } = useInputTextEditorMenu();

  return (
    <div className="text-editor-menu-input">
      <Tooltip classes="m-r-6" content="Copy">
        <Button
          classes="button--icon button--xs button--default"
          children={<CopyIcon />}
          onClick={copyTextHandler}
          aria-label="input-copy"
          type="button"
        />
      </Tooltip>
      <DownloadInputTextButton />
      <ReplaceSettingsButton />
      <Tooltip content="Delete">
        <Button
          classes="button--icon button--xs button--default"
          children={<DeleteIcon />}
          onClick={clearTextHandler}
          aria-label="input-delete"
          type="button"
        />
      </Tooltip>
    </div>
  );
};
