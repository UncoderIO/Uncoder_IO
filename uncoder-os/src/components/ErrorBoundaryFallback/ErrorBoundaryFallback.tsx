import React, { FC } from 'react';
import { FallbackProps } from 'react-error-boundary';
import { ButtonLink } from '../Buttons';

import { ReactComponent as LittleDownIcon } from '../../assets/svg/LittleDownIcon.svg';

import './ErrorBoundaryFallback.sass';

interface IErrorBoundaryFallbackPropsType extends FallbackProps {}

export const ErrorBoundaryFallback: FC <IErrorBoundaryFallbackPropsType> = () => (
  <div className="error-boundary-page">
    <div className="error-boundary-page__wrap">
      <div className="error-boundary-page__body">
        <div className="error-boundary-page__icon m-b-32">
          <LittleDownIcon />
        </div>
        <h1 className="error-boundary-page__title m-b-16">
          Something Went Wrong
        </h1>
        <div className="error-boundary-page__description m-b-24">
          <h3 className="m-b-16">
            Please, try again or reach out to us
            on <a className="link link--underline link--green" href="https://discord.com/invite/yYd47bA2XV" target="_blank">Discord</a>.
          </h3>
        </div>
        <div className="error-boundary-page__button">
          <ButtonLink className="button button--upper button--semi button--green button--m button--inline" href="/">
            TRY AGAIN
          </ButtonLink>
        </div>
      </div>
    </div>
  </div>
);
