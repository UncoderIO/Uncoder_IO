import React, { FC } from 'react';
import { Banner } from '../../../components/Banner';
import { AdditionalButtons } from '../../../components/AdditionalButtons';

import './Footer.sass';

export const Footer: FC = () => (
  <div className="footer-grid">
    <div className="footer-grid__col footer-grid__col--left">
      <Banner />
    </div>
    <div className="footer-grid__col footer-grid__col--right">
      <AdditionalButtons/>
    </div>
  </div>
);
