import { FC } from 'react';
import { InputEditorFileUploadButton } from '../../../FileUploader/InputEditorFileUploadButton';
import { useInputTextEditorHeader } from './useInputTextEditorHeader';
import { SelectSource } from '../../../SelectSource';
import { TemplateSelectorButton } from './TempleteSelectorButton';

export const InputTextEditorHeader: FC = () => {
  const {
    parsers, parser, onChangeParser,
  } = useInputTextEditorHeader();
  return (
  <div className="text-editor-header text-editor-header--input">
    <div className="text-editor-header__col text-editor-header__col--buttons">
      <InputEditorFileUploadButton/>
      <TemplateSelectorButton/>
    </div>
    <div className="text-editor-header__col">
      <SelectSource
        siemsList={parsers}
        siemSelector={parser}
        onSelectedSiemChangeHandler={(data) => () => onChangeParser(data.id)}
      />
    </div>
  </div>
  );
};
