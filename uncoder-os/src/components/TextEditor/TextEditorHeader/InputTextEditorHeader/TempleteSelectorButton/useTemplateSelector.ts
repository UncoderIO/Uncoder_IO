import { Dispatch } from '@reduxjs/toolkit';
import { useDispatch } from 'react-redux';
import { setPlatformCode } from '../../../../../reduxData/inputEditor';
import { templates, TemplatesKeys } from '../../../../../constants/templates';
import { useInputTextWithFilters } from '../../../../../hooks/useInputTextWithFilters';
import { EditorValueTypes } from '../../../../../types/editorValueTypes';

const suggestParserByTemplateName = (templateName: TemplatesKeys): EditorValueTypes => {
  switch (templateName) {
    case TemplatesKeys.MinimalRoota:
    case TemplatesKeys.FullRoota:
      return EditorValueTypes.roota;

    case TemplatesKeys.MinimalSigma:
    case TemplatesKeys.FullSigma:
      return EditorValueTypes.sigma;

    default:
      return EditorValueTypes.none;
  }
};

export const useTemplateSelector = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const { setText } = useInputTextWithFilters();

  const onSelectorTemplateHandler = (option: unknown) => (): void => {
    const template = templates.find((t) => t.name === option);
    setText(template?.value || '');
    dispatch(setPlatformCode(suggestParserByTemplateName(option as TemplatesKeys)));
  };

  return {
    onSelectorTemplateHandler,
    options: templates.map((template) => ({
      name: template.name,
      value: template.name,
    })),
  };
};
