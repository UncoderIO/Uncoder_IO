import React, { FC, ReactNode } from 'react';

import './PopperWindow.sass';

export type PopperWindowPropsType = {
  children: ReactNode;
  open: boolean;
  button: ReactNode;
  placement?: 'bottom-start' | 'bottom-end';
};

export const PopperWindow: FC<PopperWindowPropsType> = ({
  children,
  open,
  button,
  placement = 'bottom-start',
}) => (
  <div className={`popper-window-grid${open ? ' is-open' : ''}`}>
    <div className="popper-window-grid__button">
      {button}
    </div>
    <div className={`popper-window-grid__menu ${placement}${open ? ' is-open' : ''}`}>
      {open ? children : null}
    </div>
  </div>
);
