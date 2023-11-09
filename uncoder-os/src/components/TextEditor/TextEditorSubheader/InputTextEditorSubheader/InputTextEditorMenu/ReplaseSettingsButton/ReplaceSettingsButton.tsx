import React, { FC } from 'react';
import { Button } from '../../../../../Buttons';
import { ReplaceSettingsMenu } from '../../../../../Dropdown/DropdownLayouts';
import { Dropdown } from '../../../../../Dropdown';
import { ReactComponent as FilterIcon } from '../../../../../../assets/svg/FilterIcon.svg';
import { useSelector } from 'react-redux';
import { inputEditorPlatformCodeSelector } from '../../../../../../reduxData/inputEditor';

export const ReplaceSettingsButton: FC = () => {
  const parser = useSelector(inputEditorPlatformCodeSelector);

  if (parser !== 'ioc') {
    return null;
  }

  return <Dropdown
            button={
              <Button
                classes="button--icon button--xs button--default m-r-6"
                children={<FilterIcon />}
                aria-label="input-copy"
                type="button"
              />
            }
          >
            <ReplaceSettingsMenu width="320px" />
          </Dropdown>;
};
