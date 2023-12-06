import React, { FC } from 'react';
import { ReactComponent as LogoIcon } from '../../../assets/svg/LogoIcon.svg';

import './Header.sass';

export const Header: FC = () => (
  <div className="header-grid">
    <div className="header-grid__inner inner inner--lg">
      <div className="header-grid__row">
        <div className="header-grid__logo m-r-10">
          <a className="header-grid__link" href="/">
            <LogoIcon />
          </a>
          <div className="header-grid__text">
            powered by SOC Prime, Inc.
          </div>
        </div>
        <div className="header-grid__line" />
      </div>
    </div>
  </div>
);
