import type { CaseReducer, PayloadAction } from '@reduxjs/toolkit';
import { createSelector, createSlice } from '@reduxjs/toolkit';
import { OutputEditorStateType, RootState } from '../RootStore';
import { ThunkAction } from '../ThunkAction';
import { TranslateIocRequest, TranslateRequest } from '../../models/Providers/type';
import { openInfoMessage, postponedCloseInfoMessage } from '../info';
import { Severity } from '../../enums';
import { DEFAULT_ERROR_TTL } from '../../components/Info';
import { EditorValueTypes } from '../../types/editorValueTypes';

type OutputEditorReducers = {
  setText: CaseReducer<OutputEditorStateType, PayloadAction<string>>;
  clearText: CaseReducer<OutputEditorStateType>;
  setPlatformCode: CaseReducer<OutputEditorStateType, PayloadAction<EditorValueTypes>>;
};

const initialState: OutputEditorStateType = {
  text: '',
  platformCode: EditorValueTypes.none,
};

const outputEditorSlice = createSlice<OutputEditorStateType, OutputEditorReducers>({
  name: 'outputEditor',
  initialState,
  reducers: {
    setText: (state, action) => {
      state.text = action.payload;
    },
    clearText: (state) => {
      state.text = '';
    },
    setPlatformCode: (state, action) => {
      state.platformCode = action.payload;
    },
  },
});

const { actions, reducer } = outputEditorSlice;

const selectSelf = (state: RootState) => state;
export const outputEditorSelector = createSelector(
  selectSelf,
  (state: RootState): OutputEditorStateType => state.outputEditor,
);

export const outputEditorTextSelector = createSelector(
  selectSelf,
  (state: RootState): string => state.outputEditor.text,
);

export const outputEditorPlatformCodeSelector = createSelector(
  selectSelf,
  (state: RootState): string => state.outputEditor.platformCode,
);

export const {
  setText,
  clearText,
  setPlatformCode,
} = actions;

const getTranslateRequestData = (state: RootState): TranslateRequest | undefined => {
  const {
    inputEditor: { text, platformCode: sourceSiem },
    outputEditor: { platformCode: targetSiem },
    platforms: { data: platforms },
  } = state;

  const platformDataItem = platforms
    ?.find((item) => item.id === sourceSiem)
    ?.renders.find((item) => item.id === targetSiem);

  if (
    typeof platformDataItem?.code === 'undefined'
    || platformDataItem?.code === EditorValueTypes.none
    || !text.length
  ) {
    return undefined;
  }

  return {
    text,
    source_platform_id: sourceSiem,
    target_platform_id: platformDataItem?.code ?? '',
    target_scheme: (platformDataItem?.alt_platform ?? undefined) !== 'regular' ? platformDataItem?.alt_platform : undefined,
  };
};

const getTranslateIocRequestData = (state: RootState): TranslateIocRequest | undefined => {
  const {
    inputEditor: { text },
    outputEditor: { platformCode: targetSiem },
    iocSettings,
    platforms: { data: platforms },
  } = state;

  const platformDataItem = platforms
    ?.find((item) => item.id === EditorValueTypes.ioc)
    ?.renders.find((item) => item.id === targetSiem);

  if (
    typeof platformDataItem?.code === 'undefined'
    || platformDataItem?.code === EditorValueTypes.none
    || !text.length
  ) {
    return undefined;
  }

  return {
    text,
    platform: {
      id: platformDataItem.code,
    },
    iocs_per_query: iocSettings.iocPerQuery,
    include_ioc_types: iocSettings.includeIocTypes,
    include_hash_types: iocSettings.includeHashTypes,
    exceptions: iocSettings.exceptions.split('\n').filter((item) => item.length),
    ioc_parsing_rules: iocSettings.iocParsingRules,
    include_source_ip: iocSettings.includeSourceIp,
  };
};

export const translateTextFromInputEditor = ()
  : ThunkAction => async (dispatch, getState, { uncoderApiService }) => {
  try {
    const requestData = getTranslateRequestData(getState());

    if (!requestData) {
      return;
    }

    const result = await uncoderApiService.translate(requestData);
    if (
      result.status
      && typeof result?.translation !== 'undefined'
    ) {
      dispatch(setText(result.translation));
    }
    if (result.info) {
      dispatch(openInfoMessage(
        {
          message: result.info.message,
          severity: result.info.severity,
        },
      ));
      dispatch(postponedCloseInfoMessage(DEFAULT_ERROR_TTL));
    }
  } catch (e) {
    dispatch(openInfoMessage(
      {
        message: 'Something went wrong',
        severity: Severity.error,
      },
    ));
    dispatch(postponedCloseInfoMessage(DEFAULT_ERROR_TTL));
    // eslint-disable-next-line no-console
    console.log(e);
  }
};

export const translateIocsFromInputEditor = ()
  : ThunkAction => async (dispatch, getState, { uncoderApiService }) => {
  try {
    const translateIocRequestData = getTranslateIocRequestData(getState());

    if (!translateIocRequestData) {
      return;
    }

    const result = await uncoderApiService.translateIoc(translateIocRequestData);
    if (result.status) {
      dispatch(
        setText(result?.translations?.length ? result?.translations.join('\n') : ''),
      );
    }
    if (result.info) {
      dispatch(openInfoMessage(
        {
          message: result.info.message,
          severity: result.info.severity,
        },
      ));
      dispatch(postponedCloseInfoMessage(DEFAULT_ERROR_TTL));
    }
  } catch (e) {
    dispatch(openInfoMessage(
      {
        message: 'Something went wrong',
        severity: Severity.error,
      },
    ));
    dispatch(postponedCloseInfoMessage(DEFAULT_ERROR_TTL));
    // eslint-disable-next-line no-console
    console.log(e);
  }
};

export default reducer;
