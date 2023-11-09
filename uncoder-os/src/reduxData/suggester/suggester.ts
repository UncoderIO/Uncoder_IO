import type { CaseReducer, PayloadAction } from '@reduxjs/toolkit';
import { createSelector, createSlice } from '@reduxjs/toolkit';
import { RootState, SuggesterStateType } from '../RootStore';
import { SuggesterDictionaryResponse } from '../../models/Providers/type';
import { ThunkAction } from '../ThunkAction';
import { openInfoMessage } from '../info';
import { Severity } from '../../enums';

type SuggesterReducers = {
  setSuggester: CaseReducer<
    SuggesterStateType,
    PayloadAction<{data: SuggesterDictionaryResponse, parser: string}>
  >;
};

const initialState: SuggesterStateType = {
  data: [],
};

const suggesterSlice = createSlice<SuggesterStateType, SuggesterReducers>({
  name: 'suggester',
  initialState,
  reducers: {
    setSuggester: (state, action) => {
      const { data, parser } = action.payload;
      const index = state.data.findIndex((item) => item.parser === parser);
      if (index === -1) {
        state.data.push({ parser, suggesterData: data });
      } else {
        state.data[index].suggesterData = data;
      }
    },
  },
});

const { actions, reducer } = suggesterSlice;

const selectSelf = (state: RootState) => state;

export const suggesterSelector = createSelector(
  selectSelf,
  (state: RootState): SuggesterDictionaryResponse => {
    const selectedParser = state.inputEditor.platformCode;
    const suggester = state.suggester.data.find((item) => item.parser === selectedParser);
    return suggester?.suggesterData || [];
  },
);

export const {
  setSuggester,
} = actions;

export const loadSuggesterData = ()
  : ThunkAction => async (dispatch, getState, { uncoderApiService }) => {
  try {
    const parser = getState().inputEditor.platformCode;
    const result = await uncoderApiService.getSuggestDictionary(parser);
    if (typeof result !== 'undefined') {
      dispatch(
        setSuggester({ parser, data: result }),
      );
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
