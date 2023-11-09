import { useInfo } from './useInfo';
import { Snackbar } from '../Snackbar';
import { FC } from 'react';

export const InfoProvider: FC = () => {
  const {
    severity,
    message,
    isVisible,
    onClose,
  } = useInfo();

  return <Snackbar severity={severity} isVisible={isVisible} text={message} onClose={onClose}/>;
};
