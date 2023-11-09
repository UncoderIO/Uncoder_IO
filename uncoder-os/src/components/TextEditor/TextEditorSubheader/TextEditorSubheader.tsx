import React from 'react';
import { InputTextEditorSubheader } from './InputTextEditorSubheader';
import { OutputTextEditorSubheader } from './OutputTextEditorSubheader';

import './TextEditorSubheader.sass';

export const TextEditorSubheader = () => (
  <div className="text-editor-subheader-grid">
    <div className="text-editor-subheader-grid__col text-editor-subheader-grid__col--left">
      <InputTextEditorSubheader />
    </div>
    <div className="text-editor-subheader-grid__col text-editor-subheader-grid__col--right">
      <OutputTextEditorSubheader />
    </div>
  </div>
);
