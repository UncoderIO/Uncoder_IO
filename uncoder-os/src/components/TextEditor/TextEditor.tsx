import { FC } from 'react';
import AceEditor, { IAceEditorProps } from 'react-ace';

import 'ace-builds/webpack-resolver';
import './Theme/ThemeSocprime';
import './IocMode/IocMode';

import './TextEditor.sass';

export interface TextEditorProps extends IAceEditorProps {
  mode: string | object;
}

export const TextEditor: FC<TextEditorProps> = (props) => (
  <AceEditor
    theme="socprime"
    wrapEnabled
    fontSize={12}
    setOptions={{
      enableBasicAutocompletion: true,
      enableLiveAutocompletion: true,
      enableSnippets: false,
    }}
    showGutter
    width="100%"
    {...props}
  />
);
