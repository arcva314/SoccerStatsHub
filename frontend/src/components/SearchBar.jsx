import React, { useState, useEffect } from 'react';
import './SearchBar.css'
const SearchBar = ({ players, onSearch, playerName}) => {
    const [query, setQuery] = useState('');
    useEffect(() => {
        if (playerName) {
            setQuery('')
        }
        if (query.trim() !== '') {
            const filteredPlayers = players.filter(player =>
                player.toLowerCase().includes(query.toLowerCase())
            );
            onSearch(filteredPlayers.slice(0,15));
        } else {
            onSearch([]);
        }
    }, [query, players, playerName]);
    const handleInputChange = (event) => {
        setQuery(event.target.value);
    };
    return (
        <div className="search-bar">
            {!playerName ? (<input
                type="text"
                value={query}
                onChange={handleInputChange}
                placeholder="Enter a name..."
            />) : (<input
                type="text"
                value={playerName}
                onChange={handleInputChange}
                placeholder="Enter a name..."
            />)}
        </div>
    );
};

export default SearchBar;
