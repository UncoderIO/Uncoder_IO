import { FC, ReactNode } from 'react';
import { useFileUploader } from './useFileUploader';

import './FileUploader.sass';

type FileUploaderPropsType = {
  children?: ReactNode;
  handleFile: (file: File) => void;
  accept?: string;
};

export const FileUploader: FC<FileUploaderPropsType> = ({ children, handleFile, accept }) => {
  const { hiddenFileInput, handleChange, handleClick } = useFileUploader(handleFile);

  return (
    <div className="file-uploader">
      <div onClick={handleClick}>
        {children}
      </div>
      <input
        className="file-uploader__input"
        type="file"
        onChange={handleChange}
        ref={hiddenFileInput}
        accept={accept}
      />
    </div>
  );
};
