import React from 'react';

const SlideContainer = ({ children }) => (
  <div className="relative w-full overflow-y-auto bg-white rounded-lg shadow-lg p-4">
    {children}
  </div>
);

export default SlideContainer;
