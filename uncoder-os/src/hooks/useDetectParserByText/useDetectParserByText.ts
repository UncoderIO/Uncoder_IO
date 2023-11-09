import { useDispatch } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { setPlatformCode } from '../../reduxData/inputEditor';

const isSigma = (text: string): boolean => {
  return text.includes('title:') && text.includes('logsource:') && text.includes('detection:');
};

const isRoota = (text: string): boolean => {
  return text.includes('name:') && text.includes('mitre-attack:') && text.includes('detection:');
};
export const useDetectParserByText = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const detectParser = (text: string) => {
    if (isRoota(text)) {
      dispatch(setPlatformCode('roota'));
      return;
    }

    if (isSigma(text)) {
      dispatch(setPlatformCode('sigma'));
      return;
    }

    dispatch(setPlatformCode('ioc'));
  };

  return {
    detectParser,
  };
};
