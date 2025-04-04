import React from 'react';

const CoverSlide = () => {
  const colors = {
    prizm: {
      primary: "#7B3FC4",
      light: "#EEDDFF",
      border: "#5A2CA0"
    },
    kpmg: {
      primary: "#0073C6",
      light: "#DCE8F7",
      border: "#0B5EA8"
    },
    joint: {
      primary: "#6A3DB8",
      light: "#E5E0EE",
      border: "#000000"
    }
  };
  
  return (
    <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-white via-gray-50 to-gray-100 p-4 font-sans">
      <div className="w-4/5 flex flex-col items-center">
        {/* Logo & Branding Area */}
        <div className="flex items-center justify-center mb-8">
          <div className="h-20 w-20 rounded-full bg-purple-600 flex items-center justify-center text-white text-3xl font-bold mr-4">P</div>
          <div className="h-20 w-20 rounded-full bg-blue-600 flex items-center justify-center text-white text-3xl font-bold">K</div>
        </div>
        
        {/* Title */}
        <h1 className="text-5xl font-bold text-center mb-4" style={{ color: colors.prizm.primary }}>
          AI-Powered Decision Framework
        </h1>
        
        <h2 className="text-3xl text-center mb-12" style={{ color: colors.kpmg.primary }}>
          A Joint KPMG & Prizym.ai Partnership
        </h2>
        
        {/* Horizontal Line */}
        <div className="w-3/4 h-1 bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 mb-12"></div>
        
        {/* Subtitle */}
        <p className="text-2xl text-center mb-12 text-gray-700 max-w-3xl">
          Delivering AI-Driven Insights Across Industries Through Our Three-Layer Architecture
        </p>
        
        {/* Domain Icons */}
        <div className="flex justify-center space-x-8 mb-12">
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 rounded-full bg-purple-100 flex items-center justify-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke={colors.prizm.primary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="20" x2="18" y2="10"></line>
                <line x1="12" y1="20" x2="12" y2="4"></line>
                <line x1="6" y1="20" x2="6" y2="14"></line>
              </svg>
            </div>
            <p className="text-sm font-bold">Sales Performance</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke={colors.kpmg.primary} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
              </svg>
            </div>
            <p className="text-sm font-bold">Career Planning</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 rounded-full bg-green-100 flex items-center justify-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2e7d32" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="22 12 16 12 14 15 10 15 8 12 2 12"></polyline>
                <path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"></path>
              </svg>
            </div>
            <p className="text-sm font-bold">Lead Generation</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="w-16 h-16 rounded-full bg-yellow-100 flex items-center justify-center mb-2">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#f57c00" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <p className="text-sm font-bold">Workforce Optimization</p>
          </div>
        </div>
        
        {/* Date & Presenter */}
        <div className="text-center">
          <p className="text-xl font-bold text-gray-800">February 28, 2025</p>
          <p className="text-lg text-gray-600">Presented by: [Your Name]</p>
        </div>
      </div>
    </div>
  );
};

export default CoverSlide;