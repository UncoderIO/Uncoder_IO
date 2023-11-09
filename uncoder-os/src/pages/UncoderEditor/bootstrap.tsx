import React from 'react';
import { createRoot } from 'react-dom/client';
import { UncoderEditor } from './UncoderEditor';

const mount = (el: HTMLElement, baseApiUrl: string) => {
  const root = createRoot(el);
  root.render(<UncoderEditor apiBaseUrl={baseApiUrl} />);
};

export { mount };
