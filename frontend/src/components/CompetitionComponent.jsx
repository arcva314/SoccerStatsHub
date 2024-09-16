import React, { useState } from 'react';
import './CompetitionComponent.css';

const CompetitionComponent = ({ availableCompetitions, onCompetitionsChange }) => {
    const [selectedCompetitions, setSelectedCompetitions] = useState([]);

    const handleCheckboxChange = (event) => {
        const { value, checked } = event.target;
        const newSelectedCompetitions = checked
            ? [...selectedCompetitions, value]
            : selectedCompetitions.filter(competition => competition !== value);
        
        setSelectedCompetitions(newSelectedCompetitions);
        onCompetitionsChange(newSelectedCompetitions);
    };

    const renderColumns = () => {
        const columns = [];
        for (let i = 0; i < availableCompetitions.length; i += 5) {
            columns.push(availableCompetitions.slice(i, i + 5));
        }
        return columns;
    };

    return (
        <div className="competition-component">
            <h3 style={{backgroundColor:'yellow'}}><u>Select Competitions</u></h3>
            <div className="checkbox-container">
                {renderColumns().map((column, columnIndex) => (
                    <div className="checkbox-column" key={columnIndex}>
                        {column.map((competition, index) => (
                            <div style={{border: '1px solid black', paddingRight: '10px'}} key={index}>
                                <input
                                    type="checkbox"
                                    id={`competition-${columnIndex}-${index}`}
                                    value={competition}
                                    onChange={handleCheckboxChange}
                                />
                                <label htmlFor={`competition-${columnIndex}-${index}`}>{competition}</label>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default CompetitionComponent;
