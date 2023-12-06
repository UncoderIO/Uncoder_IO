import App from './App';
import { createRoot } from 'react-dom/client';
import { disableReactDevTools } from '@fvilers/disable-react-devtools';

import './assets/sass/index.sass';

if (process.env.NODE_ENV === 'production') {
  disableReactDevTools();
}

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('Root element not found');
}

const root = createRoot(rootElement);
root.render(<App />);
