import { RootStore } from './RootStore';
import inputEditorReducer from './inputEditor/inputEditor';
import outputEditorReducer from './outputEditor/outputEditor';
import platformsReducer from './platforms/platforms';
import iocSettingsReducer from './iocSettings/iocSettings';
import infoReducer from './info/info';
import suggesterReducer from './suggester/suggester';

const reducer: RootStore = {
  inputEditor: inputEditorReducer,
  outputEditor: outputEditorReducer,
  platforms: platformsReducer,
  iocSettings: iocSettingsReducer,
  info: infoReducer,
  suggester: suggesterReducer,
};

export default reducer;
