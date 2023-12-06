import React, { FC, ReactNode } from 'react';
import { Tooltip as ReactTooltip, ITooltip } from 'react-tooltip';
import { getRandomId } from '../../tools';

import './Tooltip.sass';

export interface ITooltipProps extends ITooltip {
  classes?: string;
  variant?: ITooltip['variant'];
  anchor?: string;
  place?: ITooltip['place'];
  children: ReactNode;
}

export const Tooltip: FC<ITooltipProps> = ({
  classes = '',
  anchor = 'tooltip',
  variant = 'dark',
  place = 'top',
  children,
  ...props
}) => {
  const tooltipAnchor = getRandomId(anchor);

  return (
    <span className={`tooltip-element ${classes}`} id={tooltipAnchor}>
      <ReactTooltip className="tooltip-popup" anchorSelect={`#${tooltipAnchor}`} place={place} variant={variant} {...props} />
      {children}
    </span>
  );
};
