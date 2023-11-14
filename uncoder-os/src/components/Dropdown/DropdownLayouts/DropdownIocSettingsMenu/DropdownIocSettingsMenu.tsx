import React, { FC } from 'react';
import {
  Checkbox, HelperText, Label, Textarea, RangeSlider,
} from '../../../FormElements';
import { useIocSettingsMenu } from './useIocSettingsMenu';

import './DropdownIocSettingsMenu.sass';

export const DropdownIocSettingsMenu: FC = () => {
  const {
    iocTypesFields,
    exceptionsField,
    iocsPerQueryField,
    hashTypesFields,
    onChangeIocTypes,
    onChangeExceptions,
    onChangeIocsPerQuery,
    onChangeHashTypes,
    iocTypeErrorMessage,
  } = useIocSettingsMenu();

  return <div className="ioc-settings-menu">
    <div className="ioc-settings-menu__label m-b-10">
      <Label label="Generate Queries by IOC Types"/>
    </div>
    <div className="ioc-settings-menu-list m-b-14" onChange={onChangeIocTypes}>
      {
        iocTypesFields.map((field) => (
          <div className="ioc-settings-menu-list__item m-r-16 m-b-6" key={field.name}>
            <Checkbox label={field.label} checked={field.checked} name={field.name}/>
          </div>
        ))
      }
      {
        (iocTypeErrorMessage?.length) && (
          <HelperText children={iocTypeErrorMessage} />
        )
      }
    </div>
    <div className="ioc-settings-menu__label m-b-10">
      <Label label="Hash Type"/>
    </div>
    <div className="ioc-settings-menu-list m-b-14" onChange={onChangeHashTypes}>
      {
        hashTypesFields.map((field) => (
          <div className="ioc-settings-menu-list__item m-r-16 m-b-6" key={field.name}>
            <Checkbox label={field.label} checked={field.checked} name={field.name}/>
          </div>
        ))
      }
    </div>
    <div className="ioc-settings-menu__label m-b-10">
      <Label label="IOCs per query" />
    </div>
    <div className="ioc-settings-menu__slider m-b-12">
      <RangeSlider
        isCount
        value={iocsPerQueryField}
        onChange={onChangeIocsPerQuery}
        step={25}
        min={25}
        max={300}
      />
    </div>
    <div className="ioc-settings-menu__label m-b-10">
      <Label label="Exceptions" />
    </div>
    <div className="ioc-settings-menu-list__textarea m-b-8">
      <Textarea
        placeholder="Enter text"
        rows={5}
        onChange={onChangeExceptions}
        value={exceptionsField}
      />
    </div>
  </div>;
};
