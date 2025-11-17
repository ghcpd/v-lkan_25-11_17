import React from 'react';

const SearchBar = ({ value, onChange, placeholder }) => {
  return (
    <div className="flex justify-center mb-6">
      <div className="relative w-full max-w-md">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full px-6 py-3 rounded-full border-2 border-white bg-white bg-opacity-90 text-gray-800 placeholder-gray-500 font-semibold focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-transparent shadow-lg transition-all"
        />
        <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 text-xl">
          🔍
        </span>
      </div>
    </div>
  );
};

export default SearchBar;
