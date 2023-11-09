import { FC } from 'react';
import { Checkbox } from '../../../FormElements';
import { useReplaceSettings } from './useReplaceSettings';

import './DropdownCheckboxMenu.sass';

type DropdownDefaultMenuPropsType = {
  width?: string;
};

export const ReplaceSettingsMenu: FC<DropdownDefaultMenuPropsType> = ({ width = '180px' }) => {
  const {
    onChangeReplaceSettings,
    onChangeSelectAll,
    replaceSettings,
    isSelectAll,
  } = useReplaceSettings();
  console.log(replaceSettings);
  return (
    <div className="dropdown-menu-checkbox-list" style={{ width }}>
      <div className="dropdown-menu-checkbox-list__item">
        <Checkbox label="Select All" onChange={onChangeSelectAll} checked={isSelectAll}/>
      </div>
      <div className="dropdown-menu-checkbox-list__wrap" onChange={onChangeReplaceSettings}>
        {
          replaceSettings.map((field) => (
            <div className="dropdown-menu-checkbox-list__item" key={field.name}>
              <Checkbox label={field.label} checked={field.checked} name={field.name}/>
            </div>
          ))
        }
      </div>
    </div>
  );
};
