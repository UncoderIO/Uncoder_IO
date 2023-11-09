import React from 'react';
import { InputTextEditorHeader } from './InputTextEditorHeader';
import { OutputTextEditorHeader } from './OutputTextEditorHeader';

import { ReactComponent as ArrowRightIcon } from '../../../assets/svg/ArrowRightIcon.svg';

import './TextEditorHeader.sass';

export const TextEditorHeader = () => (
    <div className="text-editor-header-grid">
      <div className="text-editor-header-grid__col text-editor-header-grid__col--left">
        <InputTextEditorHeader />
      </div>
      <div className="text-editor-header-grid__col text-editor-header-grid__col--center">
        <ArrowRightIcon />
      </div>
      <div className="text-editor-header-grid__col text-editor-header-grid__col--right">
        <OutputTextEditorHeader />
      </div>
    </div>
);
