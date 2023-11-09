import React, { ButtonHTMLAttributes, FC } from 'react';

import './Button.sass';

type ButtonPropsType = ButtonHTMLAttributes<Element> & {
  classes?: string;
};

export const Button: FC<ButtonPropsType> = ({
  children,
  classes = '',
  ...otherProps
}) => (
  <button className={`button ${classes}`} {...otherProps}>
    {children}
  </button>
);
