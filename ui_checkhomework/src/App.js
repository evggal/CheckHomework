import { Routes, Route } from 'react-router-dom'
import './App.css';
import MainPage from './pages/mainPage/MainPage';
import CheckSolutionPage from './pages/checkSolutionPage/CheckSolutionPage';
import CorrectAndRecognizedSolutionPage from './pages/correctAndRecognizedSolutionPage/CorrectAndRecognizedSolutionPage';

function App() {
  return (
    <Routes>
      <Route path='/' element={<MainPage />}></Route>
      <Route path='/checkSolution' element={<CheckSolutionPage />}></Route>
      <Route path='/correctAndRecognizedSolution' element={<CorrectAndRecognizedSolutionPage />}></Route>
    </Routes>
  );
}

export default App;
