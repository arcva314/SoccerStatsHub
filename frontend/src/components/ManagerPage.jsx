import React, { useEffect, useState } from 'react'
import ball from '../assets/soccer-ball.png'
import graph from '../assets/graph.png'
import axios from 'axios';
import './ManagerPage.css'
import Navbar from './Navbar';
import SearchBar from './SearchBar';
import SeasonComponent from './SeasonComponent';
import StatsComponent from './StatsComponent';
import VisualizationOptionsComponent from './VisualizationOptionsComponent';
import Visualization from './Visualization';
const ManagerPage = () => {
  const [managers,setManagers] = useState([]);
  const [filteredManagers, setFilteredManagers] = useState([]);
  const [managerName, setManagerName] = useState('');
  const [managerSeasons, setManagerSeasons] = useState([]);
  const [managerStats, setManagerStats] = useState([]);
  const [selectedManagerStats, setSelectedManagerStats] = useState([]);
  const [selectedManagerSeasons, setSelectedManagerSeasons] = useState([]);
  const [ManagerInfo, setManagerInfo] = useState([]);
  const [managerOptions, setManagerOptions] = useState([]);
  const [images, setImages] = useState([]);
  useEffect(() => {
    axios.get('http://localhost:5000/api/managers').then(response => {setManagers(response.data);});
  }, []);
  const handleManagerSearch = (data) => {
    setFilteredManagers(data);
  };
  useEffect(() => {
    if (managerName) {
      axios.get(`http://localhost:5000/api/manager_seasons?manager_name=${managerName}`)
        .then(response => {
          setManagerSeasons(response.data);
        });
      axios.get(`http://localhost:5000/api/manager_stats`).then(response => {setManagerStats(response.data);});
    }
  }, [managerName]);
  const handleManagerNameChange = (name) => {
    setManagerName(name);
    setFilteredManagers([]);
  };
  const handleManagerSeasonChange = (event) => {
    setSelectedManagerSeasons(event);
  };
  const handleManagerStatsChange = (event) => {
    setSelectedManagerStats(event);
  };
  const handleManagerOptionsChange = (newOptions) => {
    setManagerOptions(newOptions);
  };
  const addManager = () => {
    const missingFields = [];
    if (selectedManagerSeasons.length === 0) {
      missingFields.push('Seasons');
  }
  if (selectedManagerStats.length === 0) {
      missingFields.push('Stats');
  }
  if (!managerOptions) {
      missingFields.push('Visualization Options');
  } else if (!managerOptions.colors) {
      missingFields.push('Visualization Color');
  } else if (Object.keys(managerOptions.colors).length !== selectedManagerStats.length) {
    missingFields.push('Please ensure that all colors have been selected');
  }

  // If there are any missing fields, show an error message
  if (missingFields.length > 0) {
      alert(`Please fill out the following fields: ${missingFields.join(', ')}.`);
      return;
  }
    setManagerInfo([...ManagerInfo, {'name': managerName, 'seasons': selectedManagerSeasons, 'stats': selectedManagerStats, 'viz': managerOptions}]);
    setManagerName('');
    setSelectedManagerStats([]);
    setSelectedManagerSeasons([]);
    setManagerOptions(null)
  };
  const handleVisualize = async () => {
    const response = await axios.post('/api/visualize_manager', {
      manager_info: ManagerInfo
    });
    setImages(response.data.visualizations);
  };
  const resetManagerSearch = () => {
    setManagerName('')
    setManagerSeasons([]);
    setManagerStats([]);
    setManagerOptions(null);
  }
  const deleteManager = (index) => {
    const updatedManagers = ManagerInfo.filter((_, i) => i !== index);
    setManagerInfo(updatedManagers);
  };
  return (
    <div>
        <div className="header">
        <img src={ball} alt='Soccer Ball' className='header-img'/>
        <div className='header-content'>
          <h1>Managers</h1>
          <p>Welcome to the Manager Data Visualizer! Visualize Data from Prominent Managers in Europe's Top 5 Leagues!</p>
        </div>
        <img src={graph} alt='Graph' className='header-img'/>
      </div>
      <div className='container'>
        <Navbar/>
        <div className='manager-information'>
        {ManagerInfo.length == 0 ? <h2 className='welcome'>Start By Entering a Manager's Name</h2> : 
        (<h2 className='welcome'>Add Another Manager or Begin Visualization</h2>)}
          <SearchBar players={managers} onSearch={handleManagerSearch} playerName={managerName}/>
          {managerName && <button onClick={resetManagerSearch}>Reset Search</button>}
          {!managerName ?
          (<div className="manager-results">
                {filteredManagers.length > 0 ? (
                    <ul>
                        {filteredManagers.map((player, index)=> (<li key={index} onClick={() => handleManagerNameChange(player)}>{player}</li>))}
                    </ul>
                ) : (
                    <p>No managers found</p>
                )}
            </div>) : (<><SeasonComponent availableSeasons={managerSeasons} onSeasonsChange={handleManagerSeasonChange}/>
            <StatsComponent availableStats={managerStats} onStatsChange={handleManagerStatsChange}/>
            <VisualizationOptionsComponent keyStats={selectedManagerStats} onOptionsChange={handleManagerOptionsChange}/>
            <div style={{textAlign: 'center'}}>
              <button style={{color: 'white', backgroundColor: 'red'}} onClick={addManager}>Add Manager</button>
            </div></>)}
            {ManagerInfo.length > 0 && <div style={{paddingBottom: '50px'}}><button style={{color: 'white', backgroundColor: 'blue', position: 'absolute', left: '50%', transform: 'translateX(-50%)'}} onClick={handleVisualize}>Visualize</button></div>}
            {images.length > 0 && <Visualization images={images}/>}
        </div>
        <div>
        <h3 className='added'>Managers Currently Added:</h3>
        {ManagerInfo.length == 0 ? <p style={{color: 'black'}}>None</p> : 
        (<><ul>
            {ManagerInfo.map((player, index)=> (<li key={index} style={{cursor: 'pointer', backgroundColor: 'beige', color: 'black'}} onClick={() => deleteManager(index)}>{player.name}</li>))}
        </ul>
        <h4 className='added'>Click on a Manager to Remove Them</h4></>)
        }
        </div>
      </div>
    </div>
  );
}

export default ManagerPage