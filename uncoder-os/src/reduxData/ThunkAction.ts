import { ThunkAction as OriginalThunkAction } from 'redux-thunk';
import { AnyAction } from '@reduxjs/toolkit';
import { ApiProvider } from '../models/Providers/Api';
import { RootState } from './RootStore';

export type ThunkAction = OriginalThunkAction<void, RootState, {
    uncoderApiService: ApiProvider,
}, AnyAction>;
