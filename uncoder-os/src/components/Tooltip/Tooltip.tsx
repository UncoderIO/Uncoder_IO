import React, { FC, ReactNode } from 'react';

import './Tooltip.sass';

export interface ITooltipProps {
  classes?: string;
  position?: 'top' | 'right' | 'bottom' | 'left';
  title: string | ReactNode;
  children: ReactNode;
  maxWidth?: string;
}

export const Tooltip: FC<ITooltipProps> = ({
  classes,
  title,
  position = 'top',
  maxWidth = '300px',
  children,
}) => (
  <span className={`tooltip-element${classes ?? ''}`}>
    <div className={`tooltip tooltip-${position}`} style={{ maxWidth }}>
      {title}
    </div>
    {children}
  </span>
);
