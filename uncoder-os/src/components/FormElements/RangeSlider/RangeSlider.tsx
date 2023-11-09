import React, { FC } from 'react';
import { InputPropsType } from '../types';

import './RangeSlider.sass';

interface RangeSliderPropsType extends InputPropsType {
  classes?: string;
  isCount?: boolean;
}

export const RangeSlider: FC<RangeSliderPropsType> = ({
  classes = '',
  isCount = false,
  ...props
}) => {
  return (
    <div className={`range-slider-grid ${classes}`}>
      <input type="range" {...props} />
      {
        isCount && (
          <div className="range-slider-grid__count">
            {props.value}
          </div>
        )
      }
    </div>
  );
};
