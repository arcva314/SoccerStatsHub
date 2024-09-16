import React from 'react';
import ball from '../assets/soccer-ball.png'
import graph from '../assets/graph.png'
import './Home.css'; // Create a CSS file for styling
import Navbar from './Navbar';
import HomePage from './HomePage';
const Home = () => {
  return (
    <div className="home">
      <div className="header">
        <img src={ball} alt='Soccer Ball' className='header-img'/>
        <div className='header-content'>
          <h1>Soccer Stats Hub</h1>
          <p>Explore the World of Soccer Through Custom AI-Powered Visualizations!</p>
        </div>
        <img src={graph} alt='Graph' className='header-img'/>
      </div>
      <div className='container'>
        <Navbar/>
        <HomePage/>
      </div>
    </div>
  );
};

export default Home;