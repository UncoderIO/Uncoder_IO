import { useDispatch, useSelector } from 'react-redux';
import { Dispatch } from '@reduxjs/toolkit';
import { setPlatformCode } from '../../reduxData/inputEditor';
import { outputEditorPlatformCodeSelector, setPlatformCode as setRenderer } from '../../reduxData/outputEditor';
import { EditorValueTypes } from '../../types/editorValueTypes';
import { renderersSelector } from '../../reduxData/platforms';

const isSigma = (text: string): boolean => {
  return text.includes('title:') && text.includes('logsource:') && text.includes('detection:');
};

const isRoota = (text: string): boolean => {
  return text.includes('name:') && text.includes('mitre-attack:') && text.includes('detection:');
};
export const useDetectParserByText = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const renderers = useSelector(renderersSelector);
  const outputPlatform = useSelector(outputEditorPlatformCodeSelector);

  const resolveRenderer = (): void => {
    if (!renderers.filter((renderer) => renderer.id === outputPlatform).length) {
      dispatch(setRenderer(EditorValueTypes.none));
    }
  };

  const detectParser = (
    text: string,
    defaultPlatform: EditorValueTypes | undefined = undefined,
  ) => {
    if (isRoota(text)) {
      dispatch(setPlatformCode(EditorValueTypes.roota));
      resolveRenderer();
      return;
    }

    if (isSigma(text)) {
      dispatch(setPlatformCode(EditorValueTypes.sigma));
      resolveRenderer();
      return;
    }

    if (defaultPlatform) {
      dispatch(setPlatformCode(defaultPlatform));
      resolveRenderer();
    }
  };

  return {
    detectParser,
  };
};
