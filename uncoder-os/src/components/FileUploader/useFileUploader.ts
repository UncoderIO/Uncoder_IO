import { ChangeEvent, createRef } from 'react';

export const useFileUploader = (handleFile: (file: File) => void) => {
  const hiddenFileInput = createRef<HTMLInputElement>();

  const handleClick = () => {
    hiddenFileInput?.current?.click();
  };

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (typeof event?.target?.files === 'undefined' || event?.target?.files === null) {
      return;
    }
    const fileUploaded: File = event.target.files[0];
    handleFile(fileUploaded);
    if (hiddenFileInput?.current) {
      hiddenFileInput.current.value = '';
    }
  };

  return {
    hiddenFileInput,
    handleChange,
    handleClick,
  };
};
