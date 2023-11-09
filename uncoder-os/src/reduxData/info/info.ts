import type { CaseReducer, PayloadAction } from '@reduxjs/toolkit';
import { createSelector, createSlice } from '@reduxjs/toolkit';
import { RootState, InfoStateType } from '../RootStore';
import { Severity } from '../../enums';
import { ThunkAction } from '../ThunkAction';

type InfoReducers = {
  setSeverity: CaseReducer<InfoStateType, PayloadAction<Severity>>;
  setIsVisible: CaseReducer<InfoStateType, PayloadAction<boolean>>;
  setMessage: CaseReducer<InfoStateType, PayloadAction<string>>;
  openInfoMessage: CaseReducer<InfoStateType, PayloadAction<Omit<InfoStateType, 'isVisible'>>>;
  closeInfoMessage: CaseReducer<InfoStateType>;
};

const initialState: InfoStateType = {
  severity: Severity.info,
  isVisible: false,
  message: '',
};

const infoSlice = createSlice<InfoStateType, InfoReducers>({
  name: 'info',
  initialState,
  reducers: {
    setSeverity: (state, action) => {
      state.severity = action.payload;
    },
    setIsVisible: (state, action) => {
      state.isVisible = action.payload;
    },
    setMessage: (state, action) => {
      state.message = action.payload;
    },
    openInfoMessage: (state, action) => {
      state.severity = action.payload.severity;
      state.isVisible = true;
      state.message = action.payload.message;
    },
    closeInfoMessage: (state) => {
      state.isVisible = false;
    },
  },
});

const { actions, reducer } = infoSlice;

const selectSelf = (state: RootState) => state;

export const infoSelector = createSelector(
  selectSelf,
  (state: RootState): InfoStateType => state.info,
);

export const {
  setSeverity,
  setIsVisible,
  setMessage,
  openInfoMessage,
  closeInfoMessage,
} = actions;

let postponetTimeoutId: any;
export const postponedCloseInfoMessage = (ttl: number)
  : ThunkAction => async (dispatch) => {
  postponetTimeoutId = undefined;
  postponetTimeoutId = setTimeout(() => {
    dispatch(closeInfoMessage());
  }, ttl);
};

export default reducer;
