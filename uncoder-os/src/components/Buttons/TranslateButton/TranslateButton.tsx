import React, { FC } from 'react';
import { Button } from '../Button';
import { useTranslateButton } from './useTranslateButton';

export const TranslateButton: FC = () => {
  const { onClickHandler } = useTranslateButton();

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
