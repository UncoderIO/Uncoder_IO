import React, { FC } from 'react';
import { useOutputTextEditor } from './useOutputTextEditor';
import { TextEditor } from '../TextEditor';

import './OutputTextEditor.sass';

export const OutputTextEditor: FC = () => {
  const { outputText, onChangeText } = useOutputTextEditor();

  return (
    <div className="output-text-editor-grid">
        <TextEditor
          mode="text"
          className="ua-text-editor"
          name="ua-text-editor-output"
          value={outputText}
          onChange={onChangeText}
        />
    </div>
  );
};
