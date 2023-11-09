import { GetSuggestionListType, NodeType, YamlNodeItem } from './types';

export class YamlNode {
  private readonly nodeItem: YamlNodeItem;

  constructor(row: string, rowNumber: number) {
    this.nodeItem = {
      type: NodeType.item,
      value: row,
      rowNumber,
      offset: 0,
    };

    this.defineNodeType();
    this.defineNodeOffset();
  }

  get node(): YamlNodeItem {
    return this.nodeItem;
  }

  get type(): NodeType {
    return this.nodeItem.type;
  }

  get value(): string {
    return this.nodeItem.value;
  }

  get rowNumber(): number {
    return this.nodeItem.rowNumber;
  }

  get offset(): number {
    return this.nodeItem.offset;
  }

  get suggestions(): GetSuggestionListType | undefined {
    return this.nodeItem.suggestions;
  }

  set suggestions(suggestions: GetSuggestionListType | undefined) {
    this.nodeItem.suggestions = suggestions;
  }

  private defineNodeType = (): void => {
    if (this.nodeItem.value.search(/^([^\s-])/) === 0) {
      this.nodeItem.type = NodeType.root;
      return;
    }

    if (this.nodeItem.value.search(/^\s+\w+:/) === 0) {
      this.nodeItem.type = NodeType.field;
      return;
    }

    this.nodeItem.type = NodeType.item;
  };

  private defineNodeOffset = (): void => {
    this.nodeItem.offset = this.nodeItem.value.search(/\S/);
  };
}
