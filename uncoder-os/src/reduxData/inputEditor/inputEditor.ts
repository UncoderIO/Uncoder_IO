import type { CaseReducer, PayloadAction } from '@reduxjs/toolkit';
import { createSelector, createSlice } from '@reduxjs/toolkit';
import { RootState, InputEditorStateType } from '../RootStore';
import { inputTextEditorPlaceholder } from '../../constants/inputTextEditorPlaceholder';
import { EditorValueTypes } from '../../types/editorValueTypes';

type InputEditorReducers = {
  setText: CaseReducer<InputEditorStateType, PayloadAction<string>>;
  clearText: CaseReducer<InputEditorStateType>;
  setPlatformCode: CaseReducer<InputEditorStateType, PayloadAction<EditorValueTypes>>;
};

const initialState: InputEditorStateType = {
  text: inputTextEditorPlaceholder,
  platformCode: EditorValueTypes.none,
  changed: false,
};

const inputEditorSlice = createSlice<InputEditorStateType, InputEditorReducers>({
  name: 'inputEditor',
  initialState,
  reducers: {
    setText: (state, action) => {
      state.text = action.payload;
      state.changed = true;
    },
    clearText: (state) => {
      state.text = '';
      state.changed = true;
    },
    setPlatformCode: (state, action) => {
      state.platformCode = action.payload;
    },
  },
});

const { actions, reducer } = inputEditorSlice;

const selectSelf = (state: RootState) => state;
export const inputEditorSelector = createSelector(
  selectSelf,
  (state: RootState): InputEditorStateType => state.inputEditor,
);

export const inputEditorTextSelector = createSelector(
  selectSelf,
  (state: RootState): string => state.inputEditor.text,
);

export const inputEditorPlatformCodeSelector = createSelector(
  selectSelf,
  (state: RootState): EditorValueTypes => state.inputEditor.platformCode,
);

export const {
  setText,
  clearText,
  setPlatformCode,
} = actions;

export default reducer;
