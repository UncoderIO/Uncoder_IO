import React, { FC } from 'react';
import { AdditionalButton } from './AdditionalButton';
import { additionalConfig } from './additionalConfig';

import './AdditionalButtons.sass';

export const AdditionalButtons: FC = () => (
  <div className="additional-buttons-grid">
    {
      additionalConfig?.map(({
        icon,
        text,
        classes,
        href,
        target,
        disabled = false,
      }) => (
        <div className={`additional-buttons-grid__item${disabled ? ' is-disabled' : ''}`} key={text}>
          <AdditionalButton
            icon={icon}
            text={text}
            classes={classes}
            target={target}
            href={href}
            disabled={disabled}
          />
        </div>
      ))
    }
  </div>
);
