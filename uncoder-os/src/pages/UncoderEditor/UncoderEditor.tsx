import React, { FC } from 'react';
import { Provider } from 'react-redux';
import { ErrorBoundary } from 'react-error-boundary';
import { getStoreObject } from '../../reduxData/store';
import {
  TextEditorHeader, TextEditorSubheader, InputTextEditor, OutputTextEditor,
} from '../../components/TextEditor';
import { InfoProvider } from '../../components/Info';
import { ErrorBoundaryFallback } from '../../components/ErrorBoundaryFallback';
import { IocsStatistic } from '../../components/IocsStatistic';

import './UncoderEditor.sass';

type UncoderEditorProps = {
  apiBaseUrl: string
}

export const UncoderEditor: FC<UncoderEditorProps> = ({ apiBaseUrl }) => (
  <ErrorBoundary FallbackComponent={ErrorBoundaryFallback}>
    <Provider store={getStoreObject(apiBaseUrl)}>
      <div className="main-grid">
        <div className="main-grid__scroll">
          <div className="main-grid__wrap">
            <TextEditorHeader />
            <TextEditorSubheader />
            <div className="main-grid__row">
              <div className="main-grid__col main-grid__col--left">
                <InputTextEditor />
                <IocsStatistic />
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
  </ErrorBoundary>
);
