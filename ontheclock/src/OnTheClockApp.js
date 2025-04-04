import React, { useState, useContext } from 'react';
import DraftProvider, { DraftContext } from './context/DraftContext'; // ✅ Fixed import
import Header from './components/Header';
import DraftHistory from './components/DraftHistory';
import ProspectList from './components/ProspectList';
import CircularDraftBoard from './components/CircularDraftBoard';

// Main App Component that wraps everything in the DraftProvider
function OnTheClockApp() {
  const [activeTab, setActiveTab] = useState('draft');
  
  return (
    <DraftProvider>
      <DraftApp activeTab={activeTab} setActiveTab={setActiveTab} />
    </DraftProvider>
  );
}

// Inner component that uses the DraftContext
function DraftApp({ activeTab, setActiveTab }) {
  const { 
    selectedProspect, 
    setSelectedProspect,
    draftHistory,
    currentRound, 
    currentTeam,
    draftPlayer,
    isUsersTurn
  } = useContext(DraftContext);
  
  const [showTrade, setShowTrade] = useState(false);
  
  const toggleTradePanel = () => {
    setShowTrade(!showTrade);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Header is already a component */}
      <Header setActiveTab={setActiveTab} activeTab={activeTab} />
      
      {/* Main content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left sidebar - Draft History */}
        <div className="w-64 bg-white shadow-md overflow-y-auto">
          <DraftHistory />
        </div>
        
        {/* Main draft board */}
        <div className="flex-1 overflow-hidden">
          <CircularDraftBoard />
        </div>
        
        {/* Right sidebar - Prospects */}
        <div className="w-80 bg-white shadow-md overflow-y-auto">
          <ProspectList />
        </div>
      </div>
      
      {/* Prospect detail modal */}
      {selectedProspect && (
        <div className="fixed bottom-0 left-1/2 transform -translate-x-1/2 w-96 bg-white rounded-t-lg shadow-lg p-4 border-t-4 border-blue-500 z-30">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-xl font-bold">{selectedProspect.name}</h3>
              <p className="text-gray-600">{selectedProspect.position} | {selectedProspect.college}</p>
            </div>
            <span className="bg-blue-100 text-blue-800 font-bold rounded-full w-10 h-10 flex items-center justify-center">
              {selectedProspect.grade.toFixed(1)}
            </span>
          </div>
          
          <div className="grid grid-cols-2 gap-2 mt-3 text-sm">
            <div>
              <h4 className="font-bold text-green-700">Strengths</h4>
              <ul className="ml-4 list-disc">
                {(selectedProspect.strengths && selectedProspect.strengths.length > 0) ? (
                  selectedProspect.strengths.map((strength, i) => (
                    <li key={i}>{strength}</li>
                  ))
                ) : (
                  <li>No data available</li>
                )}
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-red-700">Weaknesses</h4>
              <ul className="ml-4 list-disc">
                {(selectedProspect.weaknesses && selectedProspect.weaknesses.length > 0) ? (
                  selectedProspect.weaknesses.map((weakness, i) => (
                    <li key={i}>{weakness}</li>
                  ))
                ) : (
                  <li>No data available</li>
                )}
              </ul>
            </div>
          </div>
          
          <div className="mt-3 flex justify-between">
            <button 
              className="px-3 py-1 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
              onClick={() => setSelectedProspect(null)}
            >
              Close
            </button>
            <button 
              className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
              onClick={() => draftPlayer(selectedProspect.id)}
              disabled={!isUsersTurn}
            >
              Draft {selectedProspect.name}
            </button>
          </div>
        </div>
      )}
      
      {/* Trade panel */}
      {showTrade && (
        <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 bg-white rounded-lg shadow-lg p-4 border-2 border-yellow-500 z-40">
          <h3 className="text-xl font-bold mb-2">Propose Trade</h3>
          
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Your Team</label>
              <select className="w-full p-2 border rounded">
                <option>Select your team</option>
                {/* We'll populate this dynamically later */}
              </select>
              
              <div className="mt-3">
                <label className="block text-sm font-medium mb-1">Send</label>
                <div className="space-y-1">
                  {/* Draft picks will be dynamically populated */}
                  <div className="flex items-center">
                    <input type="checkbox" className="mr-2" />
                    <span className="text-sm">2025 Round 1</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-1">Trade Partner</label>
              <select className="w-full p-2 border rounded">
                <option>Select trade partner</option>
                {/* We'll populate this dynamically later */}
              </select>
              
              <div className="mt-3">
                <label className="block text-sm font-medium mb-1">Receive</label>
                <div className="space-y-1">
                  {/* Draft picks will be dynamically populated */}
                  <div className="flex items-center">
                    <input type="checkbox" className="mr-2" />
                    <span className="text-sm">2025 Round 1</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div className="mt-4 flex justify-between">
            <div className="text-sm">
              <span className="font-bold">Trade Value:</span>
              <span className="text-green-600 ml-1">Calculating...</span>
            </div>
            <div>
              <button 
                className="px-3 py-1 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 mr-2"
                onClick={toggleTradePanel}
              >
                Cancel
              </button>
              <button className="px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600">
                Propose
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default OnTheClockApp;