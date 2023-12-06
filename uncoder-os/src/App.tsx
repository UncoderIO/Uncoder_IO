import React, { FC, Suspense } from 'react';
import { MainPage } from './pages/MainPage';
import { Spinner } from './components/Spinner';

const App: FC = () => (
    <Suspense fallback={<Spinner />}>
      <MainPage />
    </Suspense>
);

export default App;
