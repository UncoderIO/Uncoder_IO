import React, { FC } from 'react';

import './Label.sass';

type LabelPropsType = {
  label: string;
  classes?: string;
};

export const Label: FC<LabelPropsType> = ({ label, classes }) => (
  <div className={`label-grid ${classes ?? ''}`}>
    {label}
  </div>
);
