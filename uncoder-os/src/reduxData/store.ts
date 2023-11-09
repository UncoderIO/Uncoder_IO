import {
  AnyAction, configureStore, Dispatch, Middleware, Reducer,
} from '@reduxjs/toolkit';
import reducer from './index';
import { RootStore } from './RootStore';
import { ApiProvider } from '../models/Providers/Api';
import { ToolkitStore } from '@reduxjs/toolkit/src/configureStore';

let store: ToolkitStore<Reducer<RootStore>> | undefined;

export const getStoreObject = (baseApiUrl: string): ToolkitStore<Reducer<RootStore>> => {
  if (typeof store !== 'undefined') {
    return store;
  }

  const uncoderApiService = new ApiProvider(baseApiUrl);

  store = configureStore<
    Reducer<RootStore>,
    AnyAction,
    Middleware<NonNullable<unknown>, Reducer<RootStore>, Dispatch<never>>[]
  >({
    reducer,
    middleware: (getDefaultMiddleware) => getDefaultMiddleware({
      thunk: {
        extraArgument: {
          uncoderApiService,
        },
      },
    }),
    devTools: process.env.NODE_ENV === 'development',
  });

  return store;
};
