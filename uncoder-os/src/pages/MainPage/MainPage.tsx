import React, { FC } from 'react';
import { Header } from './Header';
import { UncoderEditor } from '../UncoderEditor';
import { Footer } from './Footer';

import './MainPage.sass';

export const MainPage: FC = () => (
  <div className="page-grid">
    <Header />
    <div className="page-grid__inner inner inner--lg">
      <UncoderEditor apiBaseUrl={process.env.UNCODER_API_BASE_URL ?? ''}/>
      <Footer />
    </div>
  </div>
);
