import React, { SyntheticEvent } from 'react';
import { Button } from '../../Buttons';
import { ReactComponent as ArrowDownIcon } from '../Svg/ArrowDownIcon.svg';
import { SelectSourceMenuType } from '../Type';

import './SelectSourceInput.sass';

type SourceSelectorInputProps = {
  isOpen: boolean;
  placeholder?: string;
  handleClick: SelectSourceMenuType['handleToggleSelect'];
  handleInput: (e: SyntheticEvent) => void;
  inputValue: string;
};

export const SelectSourceInput: React.FC <SourceSelectorInputProps> = ({
  isOpen,
  placeholder = 'Select Platform',
  handleClick,
  handleInput,
  inputValue,
}) => (
  <div className={`source-selector-input${isOpen ? ' is-open' : ''}`} onClick={handleClick(true)}>
    <input placeholder={placeholder} value={inputValue} onChange={handleInput}/>
    <div className="source-selector-input__btn">
      <Button
        classes="button--icon button--xs button--default"
        children={<ArrowDownIcon />}
        aria-label="toggle"
        type="button"
      />
    </div>
  </div>
);
