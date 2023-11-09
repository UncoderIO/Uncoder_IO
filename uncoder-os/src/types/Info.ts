import React from 'react';

export type Messages = React.ReactNode | React.ReactNode[];

export enum SnackbarSeverity {
  error = 'error',
  info = 'info',
  success = 'success',
  warning = 'warning',
}

export type InfoMessage = {
  isVisible: boolean;
  severity?: SnackbarSeverity;
  messages?: Messages;
};

export type Action = { type: 'set'; payload: InfoMessage };

export type Dispatch = (action: Action) => void;

export interface Info {
  state: InfoMessage;
  dispatch(action: Action): void;
}

export type SetFieldError = (field: string, message: string | undefined) => void;
