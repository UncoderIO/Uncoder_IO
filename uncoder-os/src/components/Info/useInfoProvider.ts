import { Severity } from '../../enums';
import { useDispatch } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { closeInfoMessage, openInfoMessage } from '../../reduxData/info';
import { DEFAULT_ERROR_TTL, DEFAULT_SUCCESS_TTL } from './constants';

export const useInfoProvider = () => {
  const dispatch = useDispatch<Dispatch<any>>();

  const showMessage = (severity: Severity, message: string, ttl?: number) => {
    dispatch(openInfoMessage({
      severity,
      message,
    }));

    if (ttl) {
      setTimeout(() => {
        dispatch(closeInfoMessage());
      }, ttl);
    }
  };

  const showErrorMessage = (message: string, ttl?: number) => {
    showMessage(Severity.error, message, ttl ?? DEFAULT_ERROR_TTL);
  };

  const showSuccessMessage = (message: string, ttl?: number) => {
    showMessage(Severity.success, message, ttl ?? DEFAULT_SUCCESS_TTL);
  };

  const showWarningMessage = (message: string, ttl?: number) => {
    showMessage(Severity.warning, message, ttl);
  };

  const showInfoMessage = (message: string, ttl?: number) => {
    showMessage(Severity.info, message, ttl);
  };

  const closeMessage = () => {
    dispatch(closeInfoMessage());
  };

  return {
    showErrorMessage,
    showSuccessMessage,
    showWarningMessage,
    showInfoMessage,
    closeMessage,
  };
};
