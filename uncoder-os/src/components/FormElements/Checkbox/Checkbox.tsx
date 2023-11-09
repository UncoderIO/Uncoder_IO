import React, { FC, ReactNode } from 'react';
import { HelperText } from '../HelperText';
import { InputPropsType } from '../types';

import { ReactComponent as CheckIcon } from './Svg/CheckIcon.svg';

import './Checkbox.sass';

interface CheckboxPropsType extends InputPropsType {
  label: string;
  error?: boolean;
  helperText?: string | ReactNode;
}

export const Checkbox: FC<CheckboxPropsType> = ({
  label,
  checked,
  error,
  helperText,
  ...props
}) => {
  return (
    <div className={`checkbox-grid${checked ? ' is-checked' : ''}`}>
      <label className="checkbox-grid__label">
        <input
          className="checkbox-grid__input"
          type="checkbox"
          checked={checked}
          {...props}
        />
        <span className="checkbox-grid__icon m-r-8">
          <CheckIcon />
        </span>
        <span className="checkbox-grid__text">
          {label}
        </span>
      </label>
      {
        (error && helperText) && (
          <HelperText children={helperText} />
        )
      }
    </div>
  );
};
