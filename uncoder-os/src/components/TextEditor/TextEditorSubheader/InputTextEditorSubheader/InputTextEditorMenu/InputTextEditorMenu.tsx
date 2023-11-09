import React, { FC } from 'react';
import { Button } from '../../../../Buttons';
import { ReplaceSettingsButton } from './ReplaseSettingsButton';
import { useInputTextEditorMenu } from './useInputTextEditorMunu';
import { DownloadInputTextButton } from './DownloadInputTextButton';

import { ReactComponent as CopyIcon } from '../../../../../assets/svg/CopyIcon.svg';
import { ReactComponent as DeleteIcon } from '../../../../../assets/svg/DeleteIcon.svg';

import './InputTextEditorMenu.sass';

export const InputTextEditorMenu: FC = () => {
  const { copyTextHandler, clearTextHandler } = useInputTextEditorMenu();

  return (
    <div className="text-editor-menu-input">
      <Button
        classes="button--icon button--xs button--default m-r-6"
        children={<CopyIcon />}
        onClick={copyTextHandler}
        aria-label="input-copy"
        type="button"
      />
      <DownloadInputTextButton />
      <ReplaceSettingsButton />
      <Button
        classes="button--icon button--xs button--default"
        children={<DeleteIcon />}
        onClick={clearTextHandler}
        aria-label="input-delete"
        type="button"
      />
    </div>
  );
};
