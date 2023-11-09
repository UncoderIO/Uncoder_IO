import { FC } from 'react';
import { TemplateOption } from '../../../../constants/templates';

import './DropdownDefaultMenu.sass';

type DropdownDefaultMenuPropsType = {
  options: TemplateOption[];
  handleClick: (value: unknown) => () => void;
  width?: string;
};

export const DropdownDefaultMenu: FC<DropdownDefaultMenuPropsType> = (
  {
    options,
    handleClick,
    width = '180px',
  },
) => (
  <div className="dropdown-menu-list" style={{ width }}>
    {
      options?.map(({ value, name }) => (
        <div className="dropdown-menu-list__item" onClick={handleClick(value)} key={value}>
          <span className="three-dots one-line">
            {name}
          </span>
        </div>
      ))
    }
  </div>
);
