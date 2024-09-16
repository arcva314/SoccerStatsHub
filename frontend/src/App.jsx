import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Home from './components/Home';
import Navbar from './components/Navbar';
import PlayerPage from './components/PlayerPage';
import ManagerPage from './components/ManagerPage';
function App() {
  return (
      <Router>
      <head><meta name="viewport" content="width=device-width, initial-scale=1.0"></meta></head>  
      <div className='app'>
        <Routes>
          <Route path='/' element={<Home/>}/>
          <Route path='/players' element={<PlayerPage/>}/>
          <Route path='/managers' element={<ManagerPage/>}/>
        </Routes>
      </div>
      </Router>
  );
}

export default App;