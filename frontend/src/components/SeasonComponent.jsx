import React, { useState } from 'react';
import './SeasonComponent.css';

const SeasonComponent = ({ availableSeasons, onSeasonsChange }) => {
    const [selectedSeasons, setSelectedSeasons] = useState([]);

    const handleCheckboxChange = (event) => {
        const { value, checked } = event.target;
        const newSelectedSeasons = checked
            ? [...selectedSeasons, value]
            : selectedSeasons.filter(season => season !== value);
        
        setSelectedSeasons(newSelectedSeasons);
        onSeasonsChange(newSelectedSeasons);
    };

    const renderColumns = () => {
        const columns = [];
        for (let i = 0; i < availableSeasons.length; i += 5) {
            columns.push(availableSeasons.slice(i, i + 5));
        }
        return columns;
    };

    return (
        <div className="season-component">
            <h3 style={{backgroundColor:'yellow'}}><u>Select Seasons (Single Year Values Represent a Major International Trophy)</u></h3>
            <div className="checkbox-container">
                {renderColumns().map((column, columnIndex) => (
                    <div className="checkbox-column" key={columnIndex}>
                        {column.map((season, index) => (
                            <div style={{border: '1px solid black', paddingRight: '10px'}} key={index}>
                                <input
                                    type="checkbox"
                                    id={`season-${columnIndex}-${index}`}
                                    value={season}
                                    onChange={handleCheckboxChange}
                                />
                                <label htmlFor={`season-${columnIndex}-${index}`}>{season}</label>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SeasonComponent;
