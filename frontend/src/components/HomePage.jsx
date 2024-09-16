import React from 'react'
import './HomePage.css'
import messi from '../assets/messi.png'
import ronaldo from '../assets/ronaldo.png'
import messistats from '../assets/messi-stats.png'
import ronaldostats from '../assets/ronaldo-stats.png'
const HomePage = () => {
  return (
    <div>
        <div className='messivsronaldo'>
            <img style={{'border': '2px solid red'}} src={messi} alt='Lionel Messi' className='messi-pic'/>
            <div>
              <img style={{'border': '2px solid blue'}} src={messistats} alt='Lionel Messi stats' className='messi-stats'/>
              <img style={{'border': '2px solid orange'}} src={ronaldostats} alt='Cristiano Ronaldo stats' className='ronaldo-stats'/>
            </div>
            <img style={{'border': '2px solid red'}} src={ronaldo} alt='Cristiano Ronaldo' className='ronaldo-pic'/>
        </div>
    </div>
  )
}

export default HomePage