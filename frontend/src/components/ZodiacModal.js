import React from 'react';

const ZodiacModal = ({ zodiac, onClose }) => {
  const getElementColor = (element) => {
    const colors = {
      'Fire': 'from-red-50 to-orange-50',
      'Earth': 'from-amber-50 to-yellow-50',
      'Air': 'from-blue-50 to-cyan-50',
      'Water': 'from-blue-50 to-teal-50',
    };
    return colors[element] || 'from-purple-50 to-indigo-50';
  };

  const getElementAccentColor = (element) => {
    const colors = {
      'Fire': 'border-red-300 bg-red-50',
      'Earth': 'border-amber-300 bg-amber-50',
      'Air': 'border-blue-300 bg-blue-50',
      'Water': 'border-blue-400 bg-blue-50',
    };
    return colors[element] || 'border-purple-300 bg-purple-50';
  };

  const getElementTextColor = (element) => {
    const colors = {
      'Fire': 'text-red-700',
      'Earth': 'text-amber-900',
      'Air': 'text-blue-700',
      'Water': 'text-blue-700',
    };
    return colors[element] || 'text-purple-700';
  };

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50 modal-backdrop"
      onClick={onClose}
    >
      <div
        className={`bg-gradient-to-br ${getElementColor(zodiac.element)} rounded-2xl max-w-2xl w-full shadow-2xl transform transition-all duration-300 animate-slideUp`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className={`${getElementAccentColor(zodiac.element)} p-8 border-b-4 border-opacity-30`}>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-4">
              <span className="text-6xl">{zodiac.symbol}</span>
              <div>
                <h2 className={`text-4xl font-bold ${getElementTextColor(zodiac.element)}`}>
                  {zodiac.name}
                </h2>
                <p className={`text-lg ${getElementTextColor(zodiac.element)} opacity-75`}>
                  {zodiac.dateRange}
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-2xl font-bold hover:opacity-70 transition-opacity"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-8 max-h-96 overflow-y-auto">
          {/* Element and Ruling Planet */}
          <div className="grid grid-cols-2 gap-6 mb-8">
            <div>
              <h3 className="text-sm font-bold text-gray-600 mb-2">ELEMENT</h3>
              <span className="element-badge" style={{
                backgroundColor: zodiac.element === 'Fire' ? '#FEE2E2' : zodiac.element === 'Earth' ? '#F4EEEA' : zodiac.element === 'Air' ? '#E0F2FE' : '#E1EAEF',
                color: zodiac.element === 'Fire' ? '#B91C1C' : zodiac.element === 'Earth' ? '#78350F' : zodiac.element === 'Air' ? '#0369A1' : '#1D4ED8'
              }}>
                {zodiac.element}
              </span>
            </div>
            <div>
              <h3 className="text-sm font-bold text-gray-600 mb-2">RULING PLANET</h3>
              <p className="text-lg font-semibold text-gray-800">{zodiac.rulingPlanet}</p>
            </div>
          </div>

          {/* Personality Traits */}
          <div className="mb-8">
            <h3 className="text-sm font-bold text-gray-600 mb-3">PERSONALITY TRAITS</h3>
            <div className="flex flex-wrap gap-2">
              {zodiac.personality.map((trait, idx) => (
                <span
                  key={idx}
                  className="px-3 py-1 bg-white border-2 border-gray-300 rounded-full text-sm font-semibold text-gray-700 hover:border-gray-400 transition-all"
                >
                  {trait}
                </span>
              ))}
            </div>
          </div>

          {/* Strengths and Weaknesses */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div className="bg-white bg-opacity-60 p-4 rounded-lg border-l-4 border-green-500">
              <h3 className="text-sm font-bold text-gray-600 mb-2">STRENGTHS</h3>
              <p className="text-gray-700 font-semibold">{zodiac.strengths}</p>
            </div>
            <div className="bg-white bg-opacity-60 p-4 rounded-lg border-l-4 border-red-500">
              <h3 className="text-sm font-bold text-gray-600 mb-2">WEAKNESSES</h3>
              <p className="text-gray-700 font-semibold">{zodiac.weaknesses}</p>
            </div>
          </div>

          {/* Compatibility */}
          <div className="mb-8">
            <h3 className="text-sm font-bold text-gray-600 mb-3">COMPATIBLE WITH</h3>
            <div className="flex flex-wrap gap-2">
              {zodiac.compatibility.map((sign, idx) => (
                <span
                  key={idx}
                  className="px-4 py-2 bg-gradient-to-r from-purple-400 to-pink-400 text-white rounded-full font-semibold text-sm shadow-md"
                >
                  {sign}
                </span>
              ))}
            </div>
          </div>

          {/* Origin */}
          <div className="bg-white bg-opacity-70 p-4 rounded-lg border-l-4 border-blue-500">
            <h3 className="text-sm font-bold text-gray-600 mb-2">ORIGIN & HISTORY</h3>
            <p className="text-gray-700 leading-relaxed">{zodiac.origin}</p>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-gray-300 flex justify-end gap-4">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-gray-500 hover:bg-gray-600 text-white font-bold rounded-lg shadow-md hover:shadow-lg transition-all"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default ZodiacModal;
