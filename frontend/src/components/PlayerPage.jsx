import React, { useState, useEffect } from 'react';
import ball from '../assets/soccer-ball.png';
import graph from '../assets/graph.png';
import axios from 'axios';
import './PlayerPage.css';
import Navbar from './Navbar';
import SearchBar from './SearchBar';
import SeasonComponent from './SeasonComponent';
import CompetitionComponent from './CompetitionComponent';
import StatsComponent from './StatsComponent';
import VisualizationOptionsComponent from './VisualizationOptionsComponent';
import Visualization from './Visualization';
const PlayerPage = () => {
  const [players, setPlayers] = useState([]);
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [playerName, setPlayerName] = useState('');
  const [seasons, setSeasons] = useState([]);
  const [competitions, setCompetitions] = useState([]);
  const [stats, setStats] = useState([]);
  const [selectedStats, setSelectedStats] = useState([]);
  const [selectedSeasons, setSelectedSeasons] = useState([]);
  const [selectedCompetitions, setSelectedCompetitions] = useState([]);
  const [error, setError] = useState(null);
  const [options, setOptions] = useState(null);
  const [playerInfo, setPlayerInfo] = useState([]);
  const [images, setImages] = useState([]);
  useEffect(() => {
    // Fetch distinct player names when the component mounts
    axios.get('http://localhost:5000/api/players')
      .then(response => {
        setPlayers(response.data);
      }).catch(error => {setError(error.message)});
  }, []);

  useEffect(() => {
    if (playerName) {
      axios.get(`http://localhost:5000/api/seasons?player_name=${playerName}`)
        .then(response => {
          setSeasons(response.data);
        })
        .catch(error => {
          setError(error.message);
        });

      axios.get(`http://localhost:5000/api/competitions?player_name=${playerName}`)
        .then(response => {
          setCompetitions(response.data);
        })
        .catch(error => {
          setError(error.message);
        });
      axios.get(`http://localhost:5000/api/stats`).then(response => {setStats(response.data);}).catch(error => {setError(error.message);});
    }
  }, [playerName]);

  const handlePlayerNameChange = (name) => {
    setPlayerName(name);
    setFilteredPlayers([]);
  };

  const handleSeasonChange = (event) => {
    setSelectedSeasons(event);
  };

  const handleCompetitionChange = (event) => {
    setSelectedCompetitions(event);
  };
  const handleSearch = (data) => {
    setFilteredPlayers(data);
};
  const handleStatsChange = (event) => {
    setSelectedStats(event);
  };
  const handleOptionsChange = (newOptions) => {
    setOptions(newOptions);
  };
  const addPlayer = () => {
    const missingFields = [];

    // Check each field and add the corresponding name to the missingFields array if it's empty or null
    if (selectedSeasons.length === 0) {
        missingFields.push('Seasons');
    }
    if (selectedCompetitions.length === 0) {
        missingFields.push('Competitions');
    }
    if (selectedStats.length === 0) {
        missingFields.push('Stats');
    }
    if (!options) {
        missingFields.push('Visualization Options');
    } else if (!options.colors) {
        missingFields.push('Visualization Color');
    } else if (Object.keys(options.colors).length !== selectedStats.length) {
      missingFields.push('Please ensure that all colors have been selected');
    }

    // If there are any missing fields, show an error message
    if (missingFields.length > 0) {
        alert(`Please fill out the following fields: ${missingFields.join(', ')}.`);
        return;
    }

    // If validation passes, add player info
    setPlayerInfo([
        ...playerInfo, 
        {
            name: playerName, 
            seasons: selectedSeasons, 
            competitions: selectedCompetitions, 
            stats: selectedStats, 
            viz: options
        }
    ]);
    
    // Reset the form fields
    setPlayerName('');
    setSelectedCompetitions([]);
    setSelectedSeasons([]);
    setSelectedStats([]);
    setOptions(null);
  };
  const handleVisualize = async () => {
    const response = await axios.post('/api/visualize', {
      player_info: playerInfo
    });
    setImages(response.data.visualizations);
  };
  const resetSearch = () => {
    setPlayerName('')
    setSelectedCompetitions([]);
    setSelectedSeasons([]);
    setSelectedStats([]);
    setOptions(null);
  }
  const deletePlayer = (index) => {
    const updatedPlayers = playerInfo.filter((_, i) => i !== index);
    setPlayerInfo(updatedPlayers);
  };
  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
        <div className="header">
        <img src={ball} alt='Soccer Ball' className='header-img'/>
        <div className='header-content'>
          <h1>Players</h1>
          <p>Welcome to the Player Data Visualizer! Select any player in Europe's top 5 Leagues + European competitions from 2009/10 onward.</p>
        </div>
        <img src={graph} alt='Graph' className='header-img'/>
      </div>
      <div className='container'>
        <Navbar/>
        <div className='player-information'>
        {playerInfo.length == 0 ? <h2 className='welcome'>Start By Entering a Player's Name</h2> : 
        (<h2 className='welcome'>Add Another Player or Begin Visualization</h2>)}
        <SearchBar players={players} onSearch={handleSearch} playerName={playerName}/>
        {playerName && <button onClick={resetSearch}>Reset Search</button>}
        {!playerName ?
        (<div className="player-results">
                {filteredPlayers.length > 0 ? (
                    <ul>
                        {filteredPlayers.map((player, index)=> (<li key={index} onClick={() => handlePlayerNameChange(player)}>{player}</li>))}
                    </ul>
                ) : (
                    <p>No players found</p>
                )}
            </div>) : (<div className='player-info-components'><SeasonComponent availableSeasons={seasons} onSeasonsChange={handleSeasonChange}/>
        <CompetitionComponent availableCompetitions={competitions} onCompetitionsChange={handleCompetitionChange}/>
        <StatsComponent availableStats={stats} onStatsChange={handleStatsChange}/>
        <VisualizationOptionsComponent keyStats={selectedStats} onOptionsChange={handleOptionsChange}/>
        <div style={{textAlign: 'right'}}>
          <button style={{color: 'white', backgroundColor: 'red'}} onClick={addPlayer}>Add Player</button>
        </div>
        </div>)}
        {playerInfo.length > 0 && <div style={{paddingBottom: '50px'}}><button style={{color: 'white', backgroundColor: 'blue', position: 'absolute', left: '50%', transform: 'translateX(-50%)'}} onClick={handleVisualize}>Visualize</button></div>}
        {images.length > 0 && <Visualization images={images}/>}
        </div>
        <div>
        <h3 className='added'>Players Currently Added:</h3>
        {playerInfo.length == 0 ? <p style={{color: 'black'}}>None</p> : 
        (<><ul>
            {playerInfo.map((player, index)=> (<li key={index} style={{cursor: 'pointer', backgroundColor: 'beige', color: 'black'}} onClick={() => deletePlayer(index)}>{player.name}</li>))}
        </ul>
        <h4 className='added'>Click on a Player to Remove Them</h4></>)
        }
        </div>
      </div>
    </div>
  );
};

export default PlayerPage;
