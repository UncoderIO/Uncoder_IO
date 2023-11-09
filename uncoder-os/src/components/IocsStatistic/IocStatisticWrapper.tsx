import { FC } from 'react';
import { useSelector } from 'react-redux';
import { inputEditorPlatformCodeSelector } from '../../reduxData/inputEditor';
import { IocsStatistic } from './IocsStatistic';

export const IocStatisticWrapper: FC = () => {
  const parser = useSelector(inputEditorPlatformCodeSelector);
  const isIocParser = parser === 'ioc';

  if (!isIocParser) {
    return null;
  }

  return <IocsStatistic />;
};
