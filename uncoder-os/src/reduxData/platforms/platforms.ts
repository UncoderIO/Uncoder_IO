import type { CaseReducer, PayloadAction } from '@reduxjs/toolkit';
import { createSelector, createSlice } from '@reduxjs/toolkit';
import { RootState, PlatformsStateType } from '../RootStore';
import {
  PlatformData, PlatformsResponse,
} from '../../models/Providers/type';
import { ThunkAction } from '../ThunkAction';
import { injectNonePlatformElement } from '../../tools';
import { Severity } from '../../enums';
import { openInfoMessage } from '../info';
import { EditorValueTypes } from '../../types/editorValueTypes';

type PlatformsReducers = {
  setPlatformsData: CaseReducer<PlatformsStateType, PayloadAction<PlatformsResponse>>;
};

const initialState: PlatformsStateType = {
  data: undefined,
};

const platformsSlice = createSlice<PlatformsStateType, PlatformsReducers>({
  name: 'platforms',
  initialState,
  reducers: {
    setPlatformsData: (state, action) => {
      state.data = action.payload;
    },
  },
});

const { actions, reducer } = platformsSlice;

const selectSelf = (state: RootState) => state;

export const parsersSelector = createSelector(
  selectSelf,
  (state: RootState): PlatformData[] => injectNonePlatformElement(state.platforms.data || []),
);

export const renderersSelector = createSelector(
  selectSelf,
  (state: RootState): PlatformData[] => {
    const selectedParser = state.inputEditor.platformCode;
    if (typeof selectedParser === 'undefined' || selectedParser === EditorValueTypes.none) {
      return injectNonePlatformElement([]);
    }
    const parser = state.platforms.data?.find((item) => item.id === selectedParser);

    return injectNonePlatformElement(parser?.renders || []);
  },
);

export const {
  setPlatformsData,
} = actions;

export const setPlatforms = ()
  : ThunkAction => async (dispatch, getState, { uncoderApiService }) => {
  try {
    const result = await uncoderApiService.getPlatforms();
    if (typeof result !== 'undefined') {
      dispatch(setPlatformsData(result));
    }
  } catch (e) {
    dispatch(openInfoMessage(
      {
        message: 'Something went wrong',
        severity: Severity.error,
      },
    ));

    // eslint-disable-next-line no-console
    console.log(e);
  }
};

export default reducer;
