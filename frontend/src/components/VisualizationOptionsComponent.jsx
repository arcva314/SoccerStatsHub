import React, { useState } from 'react';
import './VisualizationOptionsComponent.css'
const VisualizationOptionsComponent = ({ keyStats, onOptionsChange }) => {
  const [graphType, setGraphType] = useState('progression');
  const [plotType, setPlotType] = useState('multiple');
  const [message, setMessage] = useState('');
  const [colors, setColors] = useState(() => {
    return keyStats.reduce((acc, stat) => {
      acc[stat] = '#000000';
      return acc;
    }, {});
  });
  const handleGraphTypeChange = (event) => {
    setGraphType(event.target.value);
  };

  const handlePlotTypeChange = (event) => {
    setPlotType(event.target.value);
  };

  const handleColorChange = (stat, event) => {
    setColors({
      ...colors,
      [stat]: event.target.value
    });
  };

  const handleMessageChange = (event) => {
    setMessage(event.target.value);
  };

  const handleSubmit = () => {
    onOptionsChange({
      graphType,
      plotType,
      colors,
      message
    });
  };

  return (
    <div className="visualization-options">
      <h3 style={{backgroundColor:'lightblue'}}>Select Visualization Options</h3>
      
      <div className="option-group">
        <label htmlFor="graphType">Graph Type:</label>
        <select id="graphType" value={graphType} onChange={handleGraphTypeChange}>
          <option value="progression">Progression Graph (value of stats across selected seasons)</option>
          <option value="bar">Bar Chart (bar graph with the value of key stats. Selecting multiple seasons will average the value)</option>
        </select>
      </div>
      
      <div className="option-group">
        <label htmlFor="plotType">Plot Type:</label>
        <select id="plotType" value={plotType} onChange={handlePlotTypeChange}>
          <option value="multiple">Multiple Plots (separate subplots for each competition)</option>
          <option value="aggregated">Aggregated Plot (sum the stats from all competitions and put them in one graph)</option>
          <option value="averaged">Average Plot (average the stats from all competitions and put them in one graph)</option>
        </select>
      </div>
      
      {keyStats.map(stat => (
        <div className="option-group" key={stat}>
          <label htmlFor={`color-${stat}`}>{stat} Color:</label>
          <input 
            type="color" 
            id={`color-${stat}`} 
            value={colors[stat]} 
            onChange={(e) => handleColorChange(stat, e)} 
          />
        </div>
      ))}
      
      <div className="option-group">
        <label htmlFor="message">Message for LLM:</label>
        <textarea 
          id="message" 
          value={message} 
          onChange={handleMessageChange}
          rows="4"
          cols="50"
        />
      </div>
      
      <button onClick={handleSubmit}>Submit Visualization Options</button>
    </div>
  );
};

export default VisualizationOptionsComponent;
