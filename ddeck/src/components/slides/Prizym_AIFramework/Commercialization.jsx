import React from 'react';

const Commercialization = () => {
  const sectionStyles = {
    container: "p-6 rounded-lg border-2 m-2",
    purpleSection: {
      bg: "#EEDDFF",
      border: "#5A2CA0"
    },
    blueSection: {
      bg: "#DCE8F7",
      border: "#0B5EA8"
    },
    jointSection: {
      bg: "#F0F0F0",
      border: "#000000"
    }
  };

  return (
    <div className="w-full h-full bg-white p-4 font-sans">
      <h1 className="text-2xl font-bold mb-6 text-center">Partnership Commercialization Strategy</h1>
      
      <div className="flex flex-col md:flex-row w-full">
        {/* Left Side: Partnership Structure */}
        <div className="w-full md:w-1/2 p-2">
          <h2 className="text-xl font-bold mb-4">Partnership Structure</h2>
          
          <div className={`${sectionStyles.container}`} 
               style={{backgroundColor: sectionStyles.purpleSection.bg, borderColor: sectionStyles.purpleSection.border}}>
            <h3 className="text-lg font-bold mb-2">Prizym Responsibilities</h3>
            <ul className="list-disc pl-5 space-y-1">
              <li>Develop and maintain LENS AI Framework (Layer 1)</li>
              <li>Build and train custom domain-specific LLMs</li>
              <li>Provide technical AI expertise and engine development</li>
              <li>Manage third-party LLM integrations and relationships</li>
              <li>Handle AI operations and infrastructure scaling</li>
            </ul>
          </div>
          
          <div className={`${sectionStyles.container}`} 
               style={{backgroundColor: sectionStyles.blueSection.bg, borderColor: sectionStyles.blueSection.border}}>
            <h3 className="text-lg font-bold mb-2">KPMG Responsibilities</h3>
            <ul className="list-disc pl-5 space-y-1">
              <li>Lead client relationships and enterprise sales</li>
              <li>Deliver operational expertise (Layer 2)</li>
              <li>Provide domain knowledge and consulting services</li>
              <li>Handle project management and implementation</li>
              <li>Ensure compliance and risk management</li>
            </ul>
          </div>
          
          <div className={`${sectionStyles.container}`} 
               style={{backgroundColor: sectionStyles.jointSection.bg, borderColor: sectionStyles.jointSection.border}}>
            <h3 className="text-lg font-bold mb-2">Joint IP & Deliverables</h3>
            <ul className="list-disc pl-5 space-y-1">
              <li>Co-owned domain specific applications (Layer 3)</li>
              <li>Shared go-to-market for vertical solutions</li>
              <li>Joint case studies and success metrics</li>
              <li>Collaborative roadmap for domain expansions</li>
            </ul>
          </div>
        </div>
        
        {/* Right Side: Revenue & Implementation*/}
        <div className="w-full md:w-1/2 p-2">
          <h2 className="text-xl font-bold mb-4">Revenue Model</h2>
          
          <div className="bg-gray-100 p-4 rounded-lg border-2 border-gray-300 mb-4">
            <h3 className="text-lg font-bold mb-2">Revenue Streams</h3>
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-white p-3 rounded border border-gray-300">
                <p className="font-bold">Implementation Fees</p>
                <p className="text-sm">70/30 split KPMG/Prizym</p>
              </div>
              <div className="bg-white p-3 rounded border border-gray-300">
                <p className="font-bold">Software Licensing</p>
                <p className="text-sm">30/70 split KPMG/Prizym</p>
              </div>
              <div className="bg-white p-3 rounded border border-gray-300">
                <p className="font-bold">Managed Services</p>
                <p className="text-sm">50/50 split</p>
              </div>
              <div className="bg-white p-3 rounded border border-gray-300">
                <p className="font-bold">Custom Development</p>
                <p className="text-sm">Based on resource allocation</p>
              </div>
            </div>
          </div>
          
          <h2 className="text-xl font-bold mb-4">Implementation Roadmap</h2>
          <div className="bg-gray-100 p-4 rounded-lg border-2 border-gray-300">
            <div className="flex flex-col space-y-2">
              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold mr-2">1</div>
                <div>
                  <p className="font-bold">Pilot Project (SPM)</p>
                  <p className="text-sm">Q1-Q2: First joint delivery with flagship client</p>
                </div>
              </div>
              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold mr-2">2</div>
                <div>
                  <p className="font-bold">Framework Refinement</p>
                  <p className="text-sm">Q2: Optimize based on pilot learnings</p>
                </div>
              </div>
              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold mr-2">3</div>
                <div>
                  <p className="font-bold">Expansion to Additional Domains</p>
                  <p className="text-sm">Q3-Q4: Career Planning & Lead Generation</p>
                </div>
              </div>
              <div className="flex items-center">
                <div className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold mr-2">4</div>
                <div>
                  <p className="font-bold">Full Market Launch</p>
                  <p className="text-sm">Q4: Formalized offering in KPMG portfolio</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Commercialization;
