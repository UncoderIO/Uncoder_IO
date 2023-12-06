import React, { FC } from 'react';
import { Button } from '../Button';
import { Tooltip } from '../../Tooltip';
import { useTranslateButton } from './useTranslateButton';

import './TranslateButton.sass';

export const TranslateButton: FC = () => {
  const { isActive, disabledMessage, onClickHandler } = useTranslateButton();

  if (!isActive) {
    return (
      <Tooltip anchor="translate-button-disabled" content={disabledMessage} positionStrategy="fixed">
        <Button
          classes="button--upper button--semi button--green button--m"
          children="Translate"
          aria-label="translate"
          type="button"
          disabled={!isActive}
        />
      </Tooltip>
    );
  }

  return (
    <Button
      classes="button--upper button--semi button--green button--m"
      children="Translate"
      onClick={onClickHandler}
      aria-label="translate"
      type="button"
    />
  );
};
