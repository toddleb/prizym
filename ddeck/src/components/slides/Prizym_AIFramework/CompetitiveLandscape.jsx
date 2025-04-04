import React from 'react';

const CompetitiveLandscape = () => {
  // Define the quadrant positioning data
  const competitors = [
    { 
      name: "KPMG/Prizym",
      x: 85, 
      y: 82,
      size: 18,
      color: "#6A3DB8", // Joint purple/blue
      description: "Comprehensive AI Framework + Operational Excellence"
    },
    { 
      name: "Deloitte AI", 
      x: 80, 
      y: 65, 
      size: 16,
      color: "#0073C6", // Blue
      description: "Strong consulting, moderate AI capability"
    },
    { 
      name: "Accenture",
      x: 70, 
      y: 72, 
      size: 16,
      color: "#0073C6", // Blue
      description: "Good implementation skills with partner AI models"
    },
    { 
      name: "Boutique AI Firms",
      x: 88, 
      y: 35, 
      size: 12,
      color: "#7B3FC4", // Purple
      description: "Advanced AI but limited operational scale"
    },
    { 
      name: "Big Tech AI",
      x: 95, 
      y: 50, 
      size: 14,
      color: "#7B3FC4", // Purple 
      description: "Powerful models with minimal consulting"
    },
    { 
      name: "Traditional ERP",
      x: 30, 
      y: 75, 
      size: 14,
      color: "#888888", // Grey
      description: "Strong process, limited AI capabilities"
    },
    { 
      name: "DIY Solutions",
      x: 55, 
      y: 30, 
      size: 10,
      color: "#888888", // Grey
      description: "Medium capabilities across both dimensions"
    },
    { 
      name: "Point Solutions",
      x: 63, 
      y: 45, 
      size: 8,
      color: "#888888", // Grey
      description: "Narrow focus, moderate capabilities"
    }
  ];

  // Define the key differentiators
  const differentiators = [
    "Proprietary decision engines (Layer 1)",
    "Domain-specific custom LLMs",
    "Best-in-class operational implementation",
    "Joint IP ownership model",
    "Full-stack capabilities from AI to domain applications"
  ];

  return (
    <div className="w-full h-full bg-white p-4 font-sans">
      <h1 className="text-2xl font-bold mb-4 text-center">Competitive Landscape</h1>
      
      <div className="flex flex-row h-4/5 space-x-4">
        {/* Left: Quadrant Chart */}
        <div className="w-3/5 border-2 border-gray-300 rounded-lg p-4 relative">
          {/* Axis Labels */}
          <div className="absolute top-0 left-1/2 transform -translate-x-1/2">
            <span className="font-bold">High AI Sophistication</span>
          </div>
          <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2">
            <span className="font-bold">Low AI Sophistication</span>
          </div>
          <div className="absolute left-0 top-1/2 transform -translate-y-1/2 -rotate-90">
            <span className="font-bold">Low Operational Expertise</span>
          </div>
          <div className="absolute right-0 top-1/2 transform -translate-y-1/2 rotate-90">
            <span className="font-bold">High Operational Expertise</span>
          </div>
          
          {/* Quadrant Grid */}
          <div className="w-full h-full flex flex-col">
            <div className="flex flex-row h-1/2 border-b border-gray-400">
              <div className="w-1/2 border-r border-gray-400 p-2 bg-gray-50">
                <span className="text-xs text-gray-500">AI Specialists</span>
              </div>
              <div className="w-1/2 p-2 bg-blue-50">
                <span className="text-xs text-gray-500">Market Leaders</span>
              </div>
            </div>
            <div className="flex flex-row h-1/2">
              <div className="w-1/2 border-r border-gray-400 p-2 bg-gray-100">
                <span className="text-xs text-gray-500">Niche Players</span>
              </div>
              <div className="w-1/2 p-2 bg-green-50">
                <span className="text-xs text-gray-500">Process Experts</span>
              </div>
            </div>
          </div>
          
          {/* Plot the competitors */}
          {competitors.map((comp, index) => (
            <div 
              key={index}
              className="absolute rounded-full flex items-center justify-center font-bold text-white shadow-md"
              style={{
                left: `${comp.x}%`,
                top: `${100 - comp.y}%`, // Reverse Y-axis for plotting
                width: `${comp.size * 2}px`,
                height: `${comp.size * 2}px`,
                backgroundColor: comp.color,
                transform: 'translate(-50%, -50%)',
                border: comp.name === "KPMG/Prizym" ? "3px solid black" : "none",
                zIndex: comp.name === "KPMG/Prizym" ? 10 : 5
              }}
              title={comp.description}
            >
              {comp.size > 10 ? comp.name.split(" ")[0] : ""}
            </div>
          ))}
        </div>
        
        {/* Right: Key Differentiators */}
        <div className="w-2/5 border-2 border-gray-300 rounded-lg p-4">
          <h2 className="text-xl font-bold mb-4">Partnership Advantages</h2>
          
          <div className="mb-4">
            <h3 className="font-bold text-lg mb-2">Key Differentiators</h3>
            <ul className="list-disc pl-5 space-y-2">
              {differentiators.map((diff, index) => (
                <li key={index}>{diff}</li>
              ))}
            </ul>
          </div>
          
          <div className="bg-gray-100 p-3 rounded-lg">
            <h3 className="font-bold text-lg mb-2">Unique Value Proposition</h3>
            <p>The KPMG/Prizym partnership combines cutting-edge AI technologies with enterprise-grade consulting and implementation capabilities, delivering solutions that are both technically advanced and operationally effective.</p>
            <p className="mt-2">This partnership addresses the critical gap between AI potential and business results that many competitors struggle to bridge.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompetitiveLandscape;
