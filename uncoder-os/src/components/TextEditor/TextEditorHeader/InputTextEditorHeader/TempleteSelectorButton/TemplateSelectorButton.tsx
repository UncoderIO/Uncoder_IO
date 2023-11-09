import { FC } from 'react';
import { Button } from '../../../../Buttons';
import { DropdownDefaultMenu } from '../../../../Dropdown/DropdownLayouts';
import { Dropdown } from '../../../../Dropdown';
import { useTemplateSelector } from './useTemplateSelector';
import { ReactComponent as TemplateIcon } from '../../../../../assets/svg/TemplateIcon.svg';

export const TemplateSelectorButton: FC = () => {
  const { onSelectorTemplateHandler, options } = useTemplateSelector();

  return <Dropdown
    button={
      <Button
        classes="button--icon button--xs button--default button--bg"
        children={<TemplateIcon />}
        aria-label="input-roota"
        type="button"
      />
    }
  >
    <DropdownDefaultMenu options={options} handleClick={onSelectorTemplateHandler} />
  </Dropdown>;
};
