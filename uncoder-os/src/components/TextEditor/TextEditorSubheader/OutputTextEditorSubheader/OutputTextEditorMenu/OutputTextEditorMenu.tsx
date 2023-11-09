import { FC } from 'react';
import { Button } from '../../../../Buttons';
import { useOutputTextEditorMenu } from './useOutputTextEditorMunu';

import { ReactComponent as CopyIcon } from '../../../../../assets/svg/CopyIcon.svg';
import { ReactComponent as DeleteIcon } from '../../../../../assets/svg/DeleteIcon.svg';

import './OutputTextEditorMenu.sass';
import { DownloadOutputTextButton } from './DownloadOutputTextButton';

export const OutputTextEditorMenu: FC = () => {
  const { copyTextHandler, clearTextHandler } = useOutputTextEditorMenu();

  return (
    <div className="text-editor-menu-output">
      <Button
        classes="button--icon button--xs button--default m-r-6"
        children={<CopyIcon/>}
        onClick={copyTextHandler}
        aria-label="input-copy"
        type="button"
      />
      <DownloadOutputTextButton />
      <Button
        classes="button--icon button--xs button--default"
        children={<DeleteIcon/>}
        onClick={clearTextHandler}
        aria-label="input-delete"
        type="button"
      />
    </div>
  );
};
