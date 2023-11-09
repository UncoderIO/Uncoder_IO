import { RefObject } from 'react';
import { SiemsListType } from '../components/SelectSource/Type';

type ItemIdentity = {
  id: string;
  name: string;
};

export type GroupPlatformType = ItemIdentity & {
  code: string;
  firstChoice?: number;
};

export type GroupListType = ItemIdentity & {
  code?: string;
  ref?: RefObject<HTMLDivElement>
  data?: {
    id: string;
    name: string;
    data: GroupPlatformType[]
  }[]
};

const specialNames = ['select platform', 'sigma', 'iocs', 'regular'];

const sortFunction = (sortFieldName: string = 'name') => (a: ItemIdentity, b: ItemIdentity): number => {
  // @ts-ignore
  const fieldA = a[sortFieldName].toLowerCase();
  // @ts-ignore
  const fieldB = b[sortFieldName].toLowerCase();

  if (specialNames.includes(fieldB) && specialNames.includes(fieldA)) {
    return 0;
  }

  if (specialNames.includes(fieldA)) {
    return -1;
  }

  if (specialNames.includes(fieldB)) {
    return 1;
  }

  if (fieldA < fieldB) {
    return -1;
  }
  if (fieldA > fieldB) {
    return 1;
  }
  return 0;
};
export const convertSiemsListToGroupStructure = (platformsData: SiemsListType)
  : GroupListType[] | undefined => {
  if (typeof platformsData === 'undefined') {
    return undefined;
  }

  const groupStructure: GroupListType[] = [];

  platformsData.forEach((platform) => {
    const groupIndex = groupStructure.findIndex((item) => item.id === platform.group_id);
    if (groupIndex < 0) {
      groupStructure.push({
        id: platform.group_id,
        name: platform.group_name,
        data: platform?.platform_id ? [
          {
            id: platform?.platform_id ?? '',
            name: platform?.platform_name ?? '',
            data: [
              {
                id: platform.alt_platform ?? '',
                name: platform.alt_platform_name ?? '',
                code: platform.id ?? '',
                firstChoice: platform.first_choice,
              },
            ],
          },
        ] : undefined,
      });
    } else {
      const platformIndex = groupStructure[groupIndex]
        ?.data
        ?.findIndex((platforItem) => platforItem.id === platform.platform_id);
      if (typeof platformIndex !== 'undefined') {
        if (platformIndex < 0) {
          groupStructure[groupIndex]?.data?.push({
            id: platform.platform_id ?? '',
            name: platform.platform_name ?? '',
            data: [
              {
                id: platform.alt_platform ?? '',
                name: platform.alt_platform_name ?? '',
                code: platform.id ?? '',
                firstChoice: platform.first_choice,
              },
            ],
          });
        } else {
          // @ts-ignore
          groupStructure[groupIndex]?.data[platformIndex]?.data?.push({
            id: platform.alt_platform ?? '',
            name: platform.alt_platform_name ?? '',
            code: platform.id ?? '',
            firstChoice: platform.first_choice,
          });
        }
      }
    }
  });

  groupStructure.forEach((item) => {
    item?.data?.forEach((platformItem) => {
      platformItem.data.sort(sortFunction('id'));
    });
    item?.data?.sort(sortFunction());
  });

  return groupStructure;
};
