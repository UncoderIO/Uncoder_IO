import React, { FC, ReactNode } from 'react';
import { Button } from '../Buttons';
import { SnackbarIcon } from './SnackbarIcon';

import { ReactComponent as CloseIcon } from '../../assets/svg/CloseIcon.svg';
import { Severity } from '../../enums';

import './Snackbar.sass';

export type SnackbarPropsType = {
  text?: string | ReactNode;
  severity: Severity;
  isVisible: boolean;
  onClose?: () => void;
};

export const Snackbar: FC<SnackbarPropsType> = ({
  text,
  severity,
  isVisible,
  onClose,
}) => {
  if (!isVisible) {
    return null;
  }

  return (
    <div className={`snackbar-grid ${severity}`}>
      <div className="snackbar-grid__wrapper">
        <div className="snackbar-grid__icon m-r-8">
          <SnackbarIcon severity={severity} />
        </div>
        {
          text && (
            <div className="snackbar-grid__element">
              {text}
            </div>
          )
        }
        {
          onClose && (
            <div className="snackbar-grid__close">
              <Button
                classes="button button--icon button--xs button--default"
                onClick={onClose}
                aria-label="snake-bar-close"
                type="button"
              >
                <CloseIcon/>
              </Button>
            </div>
          )
        }
      </div>
    </div>
  );
};
