import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Create a CSS file for styling

const Navbar = () => {
  return (
    <div style={{'border': '2px solid black'}} className="navbar">
        <Link to='/' className='nav-link'>Home</Link>
        <Link to='/players' className='nav-link'>Players</Link>
        <Link to='/managers' className='nav-link'>Managers</Link>
    </div>
  );
};

export default Navbar;
