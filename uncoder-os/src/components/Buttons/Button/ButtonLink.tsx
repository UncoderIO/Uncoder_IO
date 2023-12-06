import React, { AnchorHTMLAttributes, FC } from 'react';

import './Button.sass';

type ButtonLinkPropsType = AnchorHTMLAttributes<Element> & {
  classes?: string;
};

export const ButtonLink: FC<ButtonLinkPropsType> = ({
  children,
  classes = '',
  ...otherProps
}) => (
  <a className={`button ${classes}`} {...otherProps}>
    {children}
  </a>
);
