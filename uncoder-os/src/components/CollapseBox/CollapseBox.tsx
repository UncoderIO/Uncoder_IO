import React, { FC, ReactNode } from 'react';

import './CollapseBox.sass';

type CollapseBoxPropsTypes = {
  isActive: boolean;
  children: ReactNode;
};

export const CollapseBox: FC<CollapseBoxPropsTypes> = ({ isActive, children }) => (
  <>{isActive && children}</>
);
