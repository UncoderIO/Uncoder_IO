export enum BasicIocType {
    Hash = 'hash',
    Domain = 'domain',
    Emails = 'emails',
    Files = 'files',
    Url = 'url',
    Ip = 'ip',
}

export enum HashIocType {
    Md5 = 'md5',
    Sha1 = 'sha1',
    Sha256 = 'sha256',
    Sha512 = 'sha512',
}

export enum IocParsingRulesType {
  ReplaseDots = 'replace_dots',
  RemovePrivateAndReservedIps = 'remove_private_and_reserved_ips',
  ReplaseHXXP = 'replace_hxxp',
}

export type IocsListTypes = 'total'
  | BasicIocType.Hash
  | BasicIocType.Ip
  | BasicIocType.Domain
  | BasicIocType.Url
  | BasicIocType.Emails
  | BasicIocType.Files
  | HashIocType.Md5
  | HashIocType.Sha1
  | HashIocType.Sha256
  | HashIocType.Sha512;

export const hashTypes: Array<HashIocType> = Object.values(HashIocType);

export type ParsedIocsType = {
    [type in IocsListTypes]?: string[]
};

export type IocsRegexpType = {
    [type in IocsListTypes]?: RegExp
};

export type IocsByTypeCountType = {
    [type in IocsListTypes]?: number
};

export const EmtyIocObject: ParsedIocsType = {
  total: [],
  [BasicIocType.Hash]: [],
  [BasicIocType.Ip]: [],
  [BasicIocType.Domain]: [],
  [BasicIocType.Url]: [],
  [BasicIocType.Emails]: [],
  [BasicIocType.Files]: [],
  [HashIocType.Md5]: [],
  [HashIocType.Sha1]: [],
  [HashIocType.Sha256]: [],
  [HashIocType.Sha512]: [],
};
