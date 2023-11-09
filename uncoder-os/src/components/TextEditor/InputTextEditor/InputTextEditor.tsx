import { FC } from 'react';
import { TextEditor } from '../TextEditor';
import { useInputEditor } from './useInputEditor';

import './InputTextEditor.sass';

export const InputTextEditor: FC = () => {
  const {
    inputText,
    mode,
    onChangeInputText,
    onFocusInputText,
    onPasteInputText,
  } = useInputEditor();

  return (
    <div className="input-text-editor-grid">
      <TextEditor
        className={'ua-text-editor'}
        mode={mode}
        value={inputText}
        name="ua-text-editor-input"
        onChange={onChangeInputText}
        onFocus={onFocusInputText}
        onPaste={onPasteInputText}
      />
    </div>
  );
};
