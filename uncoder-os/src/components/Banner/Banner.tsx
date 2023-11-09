import React, { FC } from 'react';

import './Banner.sass';

export const Banner: FC = () => (
  <div className="banner-grid">
    <div className="banner-grid__title">
      SaaS
    </div>
    <div className="banner-grid__text">
      Get even more capabilities in Uncoder AI with the Solo plan for only $11.99
    </div>
    <a
      className="banner-grid__link link link--underline link--green"
      href="https://tdm.socprime.com/uncoder-ai"
      target="_blank"
    >
      Try Now
    </a>
  </div>
);
