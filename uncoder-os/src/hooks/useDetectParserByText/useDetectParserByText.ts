import { useDispatch } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { setPlatformCode } from '../../reduxData/inputEditor';
import { setPlatformCode as setRenderer } from '../../reduxData/outputEditor';
import { EditorValueTypes } from '../../types/editorValueTypes';

const isSigma = (text: string): boolean => {
  return text.includes('title:') && text.includes('logsource:') && text.includes('detection:');
};

const isRoota = (text: string): boolean => {
  return text.includes('name:') && text.includes('mitre-attack:') && text.includes('detection:');
};
export const useDetectParserByText = () => {
  const dispatch = useDispatch<Dispatch<any>>();

  const detectParser = (
    text: string,
    defaultPlatform: EditorValueTypes | undefined = undefined,
  ) => {
    if (isRoota(text)) {
      dispatch(setPlatformCode(EditorValueTypes.roota));
      dispatch(setRenderer(EditorValueTypes.none));
      return;
    }

    if (isSigma(text)) {
      dispatch(setPlatformCode(EditorValueTypes.sigma));
      dispatch(setRenderer(EditorValueTypes.none));
      return;
    }

    if (defaultPlatform) {
      dispatch(setPlatformCode(defaultPlatform));
      dispatch(setRenderer(EditorValueTypes.none));
    }
  };

  return {
    detectParser,
  };
};
