export function replaceHxxpWithHttp(content: string): string {
  return content.replaceAll(/hxxp/img, 'http');
}
