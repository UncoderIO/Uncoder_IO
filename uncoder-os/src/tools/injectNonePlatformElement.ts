import { PlatformData } from '../models/Providers/type';
import { EditorValueTypes } from '../types/editorValueTypes';

const nonePlatform: PlatformData = {
  id: EditorValueTypes.none,
  name: 'Select Platform',
  code: EditorValueTypes.none,
  group_name: 'Select Platform',
  group_id: EditorValueTypes.none,
};

export const injectNonePlatformElement = (platformsData: PlatformData[]): PlatformData[] => {
  return [{ ...nonePlatform }, ...platformsData];
};
