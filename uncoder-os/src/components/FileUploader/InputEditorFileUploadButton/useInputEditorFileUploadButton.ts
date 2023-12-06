import { useInfoProvider } from '../../Info';
import { useDetectParserByText } from '../../../hooks';
import { useInputTextWithFilters } from '../../../hooks/useInputTextWithFilters';
import { EditorValueTypes } from '../../../types/editorValueTypes';

export const FILE_TYPES_ALLOWED_FOR_UPLOAD = [
  'text/csv',
  'application/json',
  'text/plain',
];

export const MAX_FILE_SIZE_FOR_UPLOAD = 3 * 1024 * 1024;

export const useInputEditorFileUploadButton = () => {
  const { showErrorMessage, showSuccessMessage } = useInfoProvider();
  const { setText } = useInputTextWithFilters();
  const { detectParser } = useDetectParserByText();
  const uploadHandler = async (file: File) => {
    if (!file) {
      return;
    }

    if (!FILE_TYPES_ALLOWED_FOR_UPLOAD.includes(file.type)) {
      showErrorMessage('The file you provided is in an invalid format.');

      return;
    }

    if (file.size > MAX_FILE_SIZE_FOR_UPLOAD) {
      const maxSizeInMb = MAX_FILE_SIZE_FOR_UPLOAD / 1024 / 1024;
      showErrorMessage(`The file you provided is too large. Files up to ${maxSizeInMb} MB allowed`);

      return;
    }

    const fileContent = await file.text();
    setText(fileContent);
    detectParser(fileContent, EditorValueTypes.ioc);
    showSuccessMessage('File uploaded successfully');
  };

  return {
    uploadHandler,
  };
};
