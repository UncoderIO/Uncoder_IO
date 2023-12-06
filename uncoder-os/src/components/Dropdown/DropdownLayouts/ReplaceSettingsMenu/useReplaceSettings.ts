import { ChangeEvent } from 'react';
import { Dispatch } from '@reduxjs/toolkit';
import { IocParsingRulesType } from '../../../../types/iocsTypes';
import { iocSettingsSelector, setParsingRules } from '../../../../reduxData/iocSettings';
import { useDispatch, useSelector } from 'react-redux';

const replaceSettings = [
  {
    name: IocParsingRulesType.ReplaseDots,
    label: 'Replace (.) [.] {.} with dot',
    checked: false,
  },
  {
    name: IocParsingRulesType.ReplaseHXXP,
    label: 'Replace hxxp with http',
    checked: false,
  },
  {
    name: IocParsingRulesType.RemovePrivateAndReservedIps,
    label: 'Exclude Private & Reserved networks',
    checked: false,
  },
];

export const useReplaceSettings = () => {
  const dispatch = useDispatch<Dispatch<any>>();
  const { iocParsingRules } = useSelector(iocSettingsSelector);

  const onChangeReplaceSettings = (event: ChangeEvent<HTMLInputElement>) => {
    const { checked, name } = event.target;
    const newReplaceSettings = checked
      ? [...iocParsingRules, name]
      : iocParsingRules.filter((item) => item !== name);
    dispatch(setParsingRules(newReplaceSettings as IocParsingRulesType[]));
  };

  const onChangeSelectAll = (event: ChangeEvent<HTMLInputElement>) => {
    const { checked } = event.target;
    const newReplaceSettings = checked
      ? replaceSettings.map((item) => item.name)
      : [];
    dispatch(setParsingRules(newReplaceSettings as IocParsingRulesType[]));
  };

  return {
    onChangeReplaceSettings,
    onChangeSelectAll,
    replaceSettings: replaceSettings.map((item) => ({
      ...item,
      checked: iocParsingRules.includes(item.name),
    })),
    isSelectAll: replaceSettings.length === iocParsingRules.length,
  };
};
