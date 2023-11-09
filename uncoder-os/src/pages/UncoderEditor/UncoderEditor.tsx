import React, { FC } from 'react';
import { Provider } from 'react-redux';
import { getStoreObject } from '../../reduxData/store';
import {
  TextEditorHeader, TextEditorSubheader, InputTextEditor, OutputTextEditor,
} from '../../components/TextEditor';
import { InfoProvider } from '../../components/Info';

import './UncoderEditor.sass';

type UncoderEditorProps = {
  apiBaseUrl: string
}

export const UncoderEditor: FC<UncoderEditorProps> = ({ apiBaseUrl }) => (
  <Provider store={getStoreObject(apiBaseUrl)}>
    <div className="main-grid">
      <div className="main-grid__scroll">
        <div className="main-grid__wrap">
          <TextEditorHeader />
          <TextEditorSubheader />
          <div className="main-grid__row">
            <div className="main-grid__col main-grid__col--left">
              <InputTextEditor />
            </div>
            <div className="main-grid__col main-grid__col--right">
              <OutputTextEditor />
            </div>
          </div>
        </div>
        <InfoProvider />
      </div>
    </div>
  </Provider>
);
