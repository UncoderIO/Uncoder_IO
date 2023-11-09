import { BasicIocType, HashIocType } from '../../../../types/iocsTypes';
import { useDispatch, useSelector } from 'react-redux';
import {
  iocSettingsSelector,
  setExceptions,
  setIncludeHashTypes,
  setIncludeIocTypes,
  setIncludeSourceIp,
  setIocPerQuery,
} from '../../../../reduxData/iocSettings';
import { ChangeEvent } from 'react';
import { Dispatch } from '@reduxjs/toolkit';

const iocTypesSettings = [
  {
    name: BasicIocType.Domain,
    label: 'Domain',
    checked: false,
  },
  {
    name: BasicIocType.Ip,
    label: 'IP',
    checked: false,
  },
  {
    name: BasicIocType.Url,
    label: 'URL',
    checked: false,
  },
  {
    name: BasicIocType.Hash,
    label: 'Hash',
    checked: false,
  },
];

const hashTypesSettings = [
  {
    name: HashIocType.Md5,
    label: 'MD5',
    checked: false,
  },
  {
    name: HashIocType.Sha1,
    label: 'SHA-1',
    checked: false,
  },
  {
    name: HashIocType.Sha256,
    label: 'SHA-256',
    checked: false,
  },
  {
    name: HashIocType.Sha512,
    label: 'SHA-512',
    checked: false,
  },
];
export const useIocSettingsMenu = () => {
  const {
    includeIocTypes,
    includeHashTypes,
    exceptions: exceptionsField,
    iocPerQuery: iocsPerQueryField,
    includeSourceIp: includeSourceIpField,
  } = useSelector(iocSettingsSelector);
  const dispatch = useDispatch<Dispatch<any>>();

  const onChangeIocTypes = (event: ChangeEvent<HTMLInputElement>) => {
    const { checked, name } = event.target;
    const newIocTypes = checked
      ? [...includeIocTypes, name]
      : includeIocTypes.filter((item) => item !== name);
    dispatch(setIncludeIocTypes(newIocTypes as BasicIocType[]));
  };

  const onChangeHashTypes = (event: ChangeEvent<HTMLInputElement>) => {
    const { checked, name } = event.target;
    const newHashTypes = checked
      ? [...includeHashTypes, name]
      : includeHashTypes.filter((item) => item !== name);
    dispatch(setIncludeHashTypes(newHashTypes as HashIocType[]));
  };

  const onChangeExceptions = (event: ChangeEvent<HTMLTextAreaElement>) => {
    const { value } = event.target;
    dispatch(setExceptions(value));
  };

  const onChangeIocsPerQuery = (event: ChangeEvent<HTMLInputElement>) => {
    const { value } = event.target;
    dispatch(setIocPerQuery(Number(value)));
  };

  const onChangeIncludeSourceIp = (event: ChangeEvent<HTMLInputElement>) => {
    const { checked } = event.target;
    dispatch(setIncludeSourceIp(checked));
  };

  const iocTypesErrorMessage = (): string | undefined => {
    if (!includeIocTypes.length) {
      return 'Please chose IOC Type';
    }

    return undefined;
  };

  return {
    iocTypesFields: iocTypesSettings.map((item) => ({
      ...item,
      checked: includeIocTypes.includes(item.name),
    })),
    hashTypesFields: hashTypesSettings.map((item) => ({
      ...item,
      checked: includeHashTypes.includes(item.name),
    })),
    exceptionsField,
    iocsPerQueryField,
    includeSourceIpField,
    onChangeIocTypes,
    onChangeHashTypes,
    onChangeExceptions,
    onChangeIocsPerQuery,
    onChangeIncludeSourceIp,
    iocTypeErrorMessage: iocTypesErrorMessage(),
  };
};
