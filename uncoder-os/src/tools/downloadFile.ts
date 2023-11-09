export const downloadFile = (fileName: string, content: string): void => {
  const a = document.createElement('a');
  document.body.appendChild(a);
  const blob = new Blob([content], { type: 'octet/stream' });
  const url = window.URL.createObjectURL(blob);
  a.href = url;
  a.download = fileName;
  a.click();
  window.URL.revokeObjectURL(url);
  a.remove();
};
