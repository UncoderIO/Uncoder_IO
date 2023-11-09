import { useDispatch, useSelector } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { closeInfoMessage, infoSelector } from '../../reduxData/info';

export const useInfo = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const { severity, message, isVisible } = useSelector(infoSelector);

  const onClose = () => {
    dispatch(closeInfoMessage());
  };

  return {
    severity,
    message,
    isVisible,
    onClose,
  };
};
