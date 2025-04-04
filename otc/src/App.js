import React, { useState, useContext } from 'react';
import { DraftProvider, DraftContext } from './context/DraftContext';
import Header from './components/Header';
import DraftHistory from './components/DraftHistory';
import ProspectList from './components/ProspectList';
import CircularDraftBoard from './components/CircularDraftBoard';

// Simplified version of the history sidebar
const DraftHistorySidebar = () => {
  const { draftHistory } = useContext(DraftContext);
  
  return (
    <div className="w-64 bg-white shadow-md p-4 overflow-y-auto">
      <h2 className="font-bold text-lg mb-2 border-b pb-2">Draft History</h2>
      
      {draftHistory && draftHistory.length > 0 ? (
        <div className="space-y-2">
          {draftHistory.map((pick, index) => (
            <div key={index} className="p-2 text-sm border-b">
              <div className="font-medium">{pick.pick}. {pick.prospect.name}</div>
              <div className="text-xs text-gray-600">
                Round {pick.round}, {pick.team} - {pick.prospect.position}, {pick.prospect.college}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-gray-500 text-sm">No selections yet</div>
      )}
    </div>
  );
};

function AppContent() {
  const [activeTab, setActiveTab] = useState('draft');
  const [selectedProspect, setSelectedProspect] = useState(null);
  const { draftPlayer } = useContext(DraftContext);

  // Handle drafting a player
  const handleDraftPlayer = () => {
    if (selectedProspect) {
      draftPlayer(selectedProspect.id);
      setSelectedProspect(null);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <Header setActiveTab={setActiveTab} activeTab={activeTab} />
      
      {activeTab === 'history' ? (
        <div className="flex-1 p-4">
          <DraftHistory />
        </div>
      ) : activeTab === 'teams' ? (
        <div className="flex-1 p-4">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold mb-4">Teams</h2>
            <p>Team information will be displayed here</p>
          </div>
        </div>
      ) : (
        <div className="flex flex-1 overflow-hidden">
          {/* Left sidebar - Draft History */}
          <DraftHistorySidebar />
          
          {/* Main draft board (center) */}
          <div className="flex-1 overflow-hidden">
            <CircularDraftBoard 
              selectedProspect={selectedProspect} 
              setSelectedProspect={setSelectedProspect}
            />
          </div>
          
          {/* Right sidebar - Prospects */}
          <div className="w-80 overflow-hidden">
            <ProspectList 
              setSelectedProspect={setSelectedProspect} 
            />
          </div>
        </div>
      )}
      
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
          
          <div className="mt-3 flex justify-between">
            <button 
              className="px-3 py-1 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
              onClick={() => setSelectedProspect(null)}
            >
              Close
            </button>
            <button 
              className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600"
              onClick={handleDraftPlayer}
            >
              Draft {selectedProspect.name}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <DraftProvider>
      <AppContent />
    </DraftProvider>
  );
}

export default App;