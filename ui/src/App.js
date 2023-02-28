
import './App.css';
import { Routes, Route } from 'react-router-dom'

import PageLayout from './Views/PageLayout/PageLayout.tsx';
import CheckList from './Views/CheckListView/CheckList.tsx';
import NotFound from './Views/NotFoundView/NotFound.tsx';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<PageLayout />}>
          <Route index element={<CheckList />} />
          <Route path="checks" element={<CheckList />} />

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;
