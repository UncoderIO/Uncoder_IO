const bracketsList = [
  '(.)',
  '[.]',
  '{.}',
];

export function replaceBracketsWithDotFilter(content: string): string {
  bracketsList.forEach((oneReplacement) => {
    content = content.replaceAll(oneReplacement, '.');
  });

  return content;
}
