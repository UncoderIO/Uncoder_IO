import { ProcessList } from './enums';
import { IocsByTypeCountType } from '../types/iocsTypes';

export type CalculateIocsMessage = {
  action: ProcessList;
  iocText?: string;
  calculatedData?: IocsByTypeCountType;
  totalCount?: number;
};
