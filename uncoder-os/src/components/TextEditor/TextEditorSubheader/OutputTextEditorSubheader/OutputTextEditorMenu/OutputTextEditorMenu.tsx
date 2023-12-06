import { FC } from 'react';
import { Button } from '../../../../Buttons';
import { DownloadOutputTextButton } from './DownloadOutputTextButton';
import { Tooltip } from '../../../../Tooltip';
import { useOutputTextEditorMenu } from './useOutputTextEditorMunu';

import { ReactComponent as CopyIcon } from '../../../../../assets/svg/CopyIcon.svg';
import { ReactComponent as DeleteIcon } from '../../../../../assets/svg/DeleteIcon.svg';

import './OutputTextEditorMenu.sass';

export const OutputTextEditorMenu: FC = () => {
  const { copyTextHandler, clearTextHandler } = useOutputTextEditorMenu();

  return (
    <div className="text-editor-menu-output">
      <Tooltip classes="m-r-6" content="Copy">
        <Button
          classes="button--icon button--xs button--default"
          children={<CopyIcon />}
          onClick={copyTextHandler}
          aria-label="output-copy"
          type="button"
        />
      </Tooltip>
      <DownloadOutputTextButton />
      <Tooltip content="Delete">
        <Button
          classes="button--icon button--xs button--default"
          children={<DeleteIcon />}
          onClick={clearTextHandler}
          aria-label="output-delete"
          type="button"
        />
      </Tooltip>
    </div>
  );
};
