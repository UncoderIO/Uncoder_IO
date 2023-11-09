import { PlatformData } from '../models/Providers/type';

const nonePlatform: PlatformData = {
  id: 'none',
  name: 'Select Platform',
  code: 'none',
  group_name: 'Select Platform',
  group_id: 'none',
};

export const injectNonePlatformElement = (platformsData: PlatformData[]): PlatformData[] => {
  return [{ ...nonePlatform }, ...platformsData];
};
