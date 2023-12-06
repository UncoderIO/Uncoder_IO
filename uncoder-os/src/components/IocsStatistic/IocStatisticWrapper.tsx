import { FC } from 'react';
import { useSelector } from 'react-redux';
import { inputEditorPlatformCodeSelector } from '../../reduxData/inputEditor';
import { IocsStatistic } from './IocsStatistic';
import { EditorValueTypes } from '../../types/editorValueTypes';
import { useIocCountCalculation } from './useIocCountCalculation';

export const IocStatisticWrapper: FC = () => {
  const parser = useSelector(inputEditorPlatformCodeSelector);
  const isIocParser = parser === EditorValueTypes.ioc;
  const { getOneIocTypeCount, totalCountIocs } = useIocCountCalculation();

  if (!isIocParser) {
    return null;
  }

  return <IocsStatistic
    getOneIocTypeCount={getOneIocTypeCount}
    totalIocsCount={totalCountIocs}
  />;
};
