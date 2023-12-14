import React, { FC } from 'react';
import { Button } from '../../../../../Buttons';
import { ReplaceSettingsMenu } from '../../../../../Dropdown/DropdownLayouts';
import { Dropdown } from '../../../../../Dropdown';
import { Tooltip } from '../../../../../Tooltip';
import { ReactComponent as FilterIcon } from '../../../../../../assets/svg/FilterIcon.svg';
import { useSelector } from 'react-redux';
import { inputEditorPlatformCodeSelector } from '../../../../../../reduxData/inputEditor';
import { EditorValueTypes } from '../../../../../../types/editorValueTypes';

export const ReplaceSettingsButton: FC = () => {
  const parser = useSelector(inputEditorPlatformCodeSelector);

  if (parser !== EditorValueTypes.ioc) {
    return null;
  }

  return (
    <Dropdown
      button={
      <Tooltip classes="d-block m-r-6" content="Filter">
        <Button
          classes="button--icon button--xs button--default"
          children={<FilterIcon />}
          aria-label="input-copy"
          type="button"
        />
      </Tooltip>
      }
    >
      <ReplaceSettingsMenu width="320px" />
    </Dropdown>
  );
};
