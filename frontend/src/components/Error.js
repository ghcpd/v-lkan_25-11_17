import React from 'react';

const Error = ({ message }) => {
  return (
    <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-6 rounded-lg mb-8 shadow-lg">
      <div className="flex items-center">
        <span className="text-2xl mr-4">⚠️</span>
        <div>
          <p className="font-bold text-lg">Error</p>
          <p className="text-sm">{message}</p>
        </div>
      </div>
    </div>
  );
};

export default Error;
