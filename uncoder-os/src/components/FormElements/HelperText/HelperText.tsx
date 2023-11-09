import React, { FC, ReactNode } from 'react';

import './HelperTex.sass';

export type HelperTextPropsType = {
  variant?: 'error' | 'success';
  classes?: string;
  children: ReactNode;
};

export const HelperText: FC<HelperTextPropsType> = ({ variant = 'error', classes, children }) => (
  <div className={`helper-text ${variant} ${classes ?? ''}`}>
    {children}
  </div>
);
