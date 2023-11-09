import { ChangeEventHandler, FC } from 'react';
import { PlatformItem } from '../../models/Providers/type';

import './SelectSource.sass';

export type SelectSourceSimpleInputType = {
  onChange: ChangeEventHandler<HTMLSelectElement>;
  value?: string;
  options?: PlatformItem[];
}
export const SelectSourceSimpleInput: FC<SelectSourceSimpleInputType> = ({
  options,
  onChange,
  value,
}) => (
  <div className="source-selector">
    <select value={value} onChange={onChange}>
      {options?.map((item) => (
        <option value={item.id} key={item.id}>{item.name}</option>
      ))}
    </select>
  </div>
);
