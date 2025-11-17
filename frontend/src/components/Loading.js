import React from 'react';

const Loading = () => {
  return (
    <div className="flex flex-col items-center justify-center py-16">
      <div className="loading-spinner mb-4"></div>
      <p className="text-white text-xl font-semibold animate-pulse">
        Loading zodiac signs...
      </p>
    </div>
  );
};

export default Loading;
