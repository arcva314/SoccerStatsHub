import React, { useState } from 'react';
import './StatsComponent.css';

const StatsComponent = ({ availableStats, onStatsChange }) => {
    const [selectedStats, setSelectedStats] = useState([]);

    const handleCheckboxChange = (event) => {
        const { value, checked } = event.target;
        const newSelectedStats = checked
            ? [...selectedStats, value]
            : selectedStats.filter(stat => stat !== value);
        
        setSelectedStats(newSelectedStats);
        onStatsChange(newSelectedStats);
    };

    const renderColumns = () => {
        const columns = [];
        for (let i = 0; i < availableStats.length; i += 5) {
            columns.push(availableStats.slice(i, i + 5));
        }
        return columns;
    };

    return (
        <div className="stats-component">
            <h3 style={{backgroundColor:'yellow'}}><u>Select Stats</u></h3>
            <div className="checkbox-container">
                {renderColumns().map((column, columnIndex) => (
                    <div className="checkbox-column" key={columnIndex}>
                        {column.map((stat, index) => (
                            <div style={{border: '1px solid black', paddingRight: '10px'}} key={index}>
                                <input
                                    type="checkbox"
                                    id={`stat-${columnIndex}-${index}`}
                                    value={stat}
                                    onChange={handleCheckboxChange}
                                />
                                <label htmlFor={`stat-${columnIndex}-${index}`}>{stat}</label>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default StatsComponent;
