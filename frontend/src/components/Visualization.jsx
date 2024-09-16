import React from 'react';
import './Visualization.css';

const Visualization = ({ images }) => {
    if (!images || images.length === 0) return null;

    // Calculate grid template columns based on the number of images
    const columns = 1;

    const gridStyle = {
        display: 'grid',
        gridTemplateColumns: `repeat(${columns}, 1fr)`,
        gap: '10px',
    };

    return (
        <div className="visualization-container" style={gridStyle}>
            {images.map((imgBase64, index) => (
                <img
                    key={index}
                    src={`data:image/png;base64,${imgBase64}`}
                    alt={`Visualization ${index + 1}`}
                    style={{ width: '100%', height: 'auto' }}
                />
            ))}
        </div>
    );
};

export default Visualization;
