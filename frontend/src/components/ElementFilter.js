import React from 'react';

const ElementFilter = ({ elements, selectedElement, onFilter }) => {
  return (
    <div className="flex flex-wrap justify-center gap-3">
      <button
        onClick={() => onFilter('')}
        className={`px-4 py-2 rounded-full font-bold shadow-md transition-all ${
          selectedElement === ''
            ? 'bg-white text-purple-700 shadow-lg scale-105'
            : 'bg-white bg-opacity-70 text-gray-700 hover:bg-opacity-90'
        }`}
      >
        All Signs
      </button>
      {elements.map((element) => {
        const elementColors = {
          'Fire': 'bg-red-400 hover:bg-red-500 text-white',
          'Earth': 'bg-amber-700 hover:bg-amber-800 text-white',
          'Air': 'bg-blue-400 hover:bg-blue-500 text-white',
          'Water': 'bg-blue-600 hover:bg-blue-700 text-white',
        };

        return (
          <button
            key={element}
            onClick={() => onFilter(element)}
            className={`px-4 py-2 rounded-full font-bold shadow-md transition-all ${
              selectedElement === element
                ? `${elementColors[element]} shadow-lg scale-105`
                : `${elementColors[element]} opacity-70`
            }`}
          >
            {element}
          </button>
        );
      })}
    </div>
  );
};

export default ElementFilter;
