import React from 'react';

const ZodiacCard = ({ zodiac, onClick }) => {
  const getElementColor = (element) => {
    const colors = {
      'Fire': 'bg-gradient-to-br from-red-400 to-orange-500 hover:from-red-500 hover:to-orange-600',
      'Earth': 'bg-gradient-to-br from-amber-700 to-yellow-600 hover:from-amber-800 hover:to-yellow-700',
      'Air': 'bg-gradient-to-br from-blue-400 to-cyan-500 hover:from-blue-500 hover:to-cyan-600',
      'Water': 'bg-gradient-to-br from-blue-600 to-teal-500 hover:from-blue-700 hover:to-teal-600',
    };
    return colors[element] || 'bg-gradient-to-br from-purple-500 to-indigo-600';
  };

  const getElementBadgeColor = (element) => {
    const colors = {
      'Fire': 'element-fire',
      'Earth': 'element-earth',
      'Air': 'element-air',
      'Water': 'element-water',
    };
    return colors[element] || 'bg-gray-500 text-white';
  };

  return (
    <div
      onClick={onClick}
      className={`zodiac-card ${getElementColor(zodiac.element)} rounded-xl p-6 text-white shadow-xl cursor-pointer transform hover:scale-105 transition-all duration-300`}
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-2xl font-bold">{zodiac.name}</h3>
        <span className="text-4xl">{zodiac.symbol}</span>
      </div>

      <div className="mb-4">
        <p className="text-sm font-semibold opacity-90">
          {zodiac.dateRange}
        </p>
      </div>

      <div className="mb-4">
        <span className={`element-badge ${getElementBadgeColor(zodiac.element)}`}>
          {zodiac.element}
        </span>
      </div>

      <div className="mb-4">
        <p className="text-sm opacity-90 line-clamp-3">
          {zodiac.personality.join(', ')}
        </p>
      </div>

      <div className="pt-4 border-t border-white border-opacity-20">
        <p className="text-xs opacity-75 font-semibold">
          Click to view details →
        </p>
      </div>
    </div>
  );
};

export default ZodiacCard;
