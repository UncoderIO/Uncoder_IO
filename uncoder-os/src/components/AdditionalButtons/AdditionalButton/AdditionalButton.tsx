import React, { FC } from 'react';
import { AdditionalType } from '../additionalConfig';

import './AdditionalButton.sass';

export const AdditionalButton: FC <AdditionalType> = ({
  href = undefined,
  icon,
  text,
  target = undefined,
  handleClick = () => {},
  disabled = false,
}) => {
  const element = (
    <div
      className={`additional-button ${text.toLowerCase()}${disabled ? ' is-disabled' : ''}`}
      onClick={handleClick}
    >
      <div className="additional-button__icon m-b-4">
        {icon}
      </div>
      <div className="additional-button__text">
        {text}
      </div>
    </div>
  );

  return (
    href
      ? (
        <a className="additional-link" href={href} target={target}>
          {element}
        </a>
      )
      : element
  );
};
