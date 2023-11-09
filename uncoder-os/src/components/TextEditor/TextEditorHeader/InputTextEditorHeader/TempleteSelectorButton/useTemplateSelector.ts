import { Dispatch } from '@reduxjs/toolkit';
import { useDispatch } from 'react-redux';
import { setPlatformCode, setText } from '../../../../../reduxData/inputEditor';
import { templates, TemplatesKeys } from '../../../../../constants/templates';

const suggestParserByTemplateName = (templateName: TemplatesKeys): string => {
  switch (templateName) {
    case TemplatesKeys.MinimalRoota:
    case TemplatesKeys.FullRoota:
      return 'roota';

    case TemplatesKeys.MinimalSigma:
    case TemplatesKeys.FullSigma:
      return 'sigma';

    default:
      return 'none';
  }
};

export const useTemplateSelector = () => {
  const dispatch = useDispatch<Dispatch<any>>();

  const onSelectorTemplateHandler = (option: unknown) => (): void => {
    const template = templates.find((t) => t.name === option);
    dispatch(setText(template?.value || ''));
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
