import React, { FC, ReactNode } from 'react';
import { PopperWindow, PopperWindowPropsType } from '../PopperWindow';
import { useDropdown } from './useDropdown';

type DropdownPropsType = {
  children: ReactNode;
  button: ReactNode;
  placement?: PopperWindowPropsType['placement'];
};

export const Dropdown: FC<DropdownPropsType> = ({ children, button, placement }) => {
  const { isOpen, selectRef, handleClick } = useDropdown();

  return (
    <div className="dropdown-grid" ref={selectRef}>
      <PopperWindow
        open={isOpen}
        button={<div onClick={handleClick(true)}>{button}</div>}
        placement={placement}
      >
        {children}
      </PopperWindow>
    </div>
  );
};
