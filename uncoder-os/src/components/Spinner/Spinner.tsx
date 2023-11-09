import React from 'react';

import './Spinner.sass';

export type SpinnerProps = {
  variant?: 'fixed' | 'absolute' | 'default';
};

export const Spinner: React.FC <SpinnerProps> = ({ variant = 'default' }) => (
  <div className={`square-spinner ${variant}`}>
    <div className="square-spinner__main">
      <div className="square-spinner__square">
        <span />
        <span />
        <span />
      </div>
      <div className="square-spinner__square">
        <span />
        <span />
        <span />
      </div>
      <div className="square-spinner__square">
        <span />
        <span />
        <span />
      </div>
    </div>
  </div>
);
