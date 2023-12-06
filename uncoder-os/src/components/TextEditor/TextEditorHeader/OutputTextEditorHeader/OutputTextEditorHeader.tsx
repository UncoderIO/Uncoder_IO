import React, { FC } from 'react';
import { Button, TranslateButton } from '../../../Buttons';
import { Dropdown } from '../../../Dropdown';
import { DropdownIocSettingsMenu } from '../../../Dropdown/DropdownLayouts';
import { SelectSource } from '../../../SelectSource';
import { useOutputTextEditorHeader } from './useOutputTextEditorHeader';

import { ReactComponent as SettingsIcon } from '../../../../assets/svg/SettingsIcon.svg';

export const OutputTextEditorHeader: FC = () => {
  const {
    renderer,
    renderers,
    onChangeRenderer,
    isIocMode,
  } = useOutputTextEditorHeader();

  return <div className="text-editor-header text-editor-header--output">
    <div className="text-editor-header__col">
      <SelectSource
        siemsList={renderers}
        siemSelector={renderer}
        onSelectedSiemChangeHandler={(data) => {
          return () => onChangeRenderer(data?.code ?? '');
        }}
      />
    </div>
    <div className="text-editor-header__col text-editor-header__col--translate">
      <div className="text-editor-header-list">
        <div className="text-editor-header-list__item m-r-8">
          {
            isIocMode
              ? (
                <Dropdown
                  children={<DropdownIocSettingsMenu/>}
                  placement="bottom-end"
                  button={
                    <Button
                      classes="button--icon button--xs button--default button--bg"
                      aria-label="ioc-settings"
                      children={<SettingsIcon/>}
                      type="button"
                    />
                  }
                />
              )
              : null
          }
        </div>
        <div className="text-editor-header-list__item">
          <TranslateButton/>
        </div>
      </div>
    </div>
  </div>;
};
