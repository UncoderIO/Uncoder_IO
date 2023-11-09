import { FC } from 'react';
import { Severity } from '../../enums';
import { ReactComponent as CheckedIcon } from '../../assets/svg/CheckedIcon.svg';
import { ReactComponent as InfoIcon } from '../../assets/svg/InfoIcon.svg';

type SnackbarIconType = {
  severity: Severity;
}
export const SnackbarIcon: FC<SnackbarIconType> = ({ severity }) => {
  switch (severity) {
    case Severity.success:
      return <CheckedIcon/>;

    default:
      return <InfoIcon/>;
  }
};
