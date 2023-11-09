import { createRef, useState } from 'react';
import { useHandleClickOutside } from '../../hooks';

export const useDropdown = () => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const selectRef = createRef<HTMLDivElement>();

  const handleClick = (state: boolean) => () => {
    setIsOpen(state);
  };

  useHandleClickOutside(
    selectRef,
    handleClick(false),
  );

  return {
    isOpen,
    selectRef,
    handleClick,
  };
};
