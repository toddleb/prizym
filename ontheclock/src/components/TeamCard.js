import React, { useState, useContext } from 'react';
import { DraftContext } from '../context/DraftContext';

const TeamCard = ({ team, onClose }) => {
  const { draftHistory } = useContext(DraftContext);
  const [activeTab, setActiveTab] = useState('needs');
  
  // Make sure team exists before accessing properties
  if (!team || !team.id) {
    return null;
  }
  
  // Get team-specific draft history
  const teamDraftHistory = draftHistory.filter(pick => pick.team === team.name);
  
  // Get the appropriate tab content
  const renderTabContent = () => {
    switch(activeTab) {
      case 'needs':
        return (
          <div className="p-3">
            <h3 className="font-bold text-lg mb-2">Team Needs</h3>
            <div className="space-y-2">
              {team.needs.map((need, idx) => (
                <div key={idx} className="p-2 border-b">
                  <div className="flex justify-between">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      idx === 0 ? 'bg-red-100 text-red-800' :
                      idx <= 2 ? 'bg-orange-100 text-orange-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {need}
                    </span>
                    <span className="text-sm text-gray-500">
                      {idx === 0 ? 'High' : idx <= 2 ? 'Medium' : 'Low'} Priority
                    </span>
                  </div>
                  <p className="text-sm mt-1">
                    {idx === 0 
                      ? `Looking for an impact player at ${need}` 
                      : `Need added talent at ${need} position`}
                  </p>
                </div>
              ))}
            </div>
          </div>
        );
      case 'picks':
        return (
          <div className="p-3">
            <h3 className="font-bold text-lg mb-2">Current Draft Picks</h3>
            <div className="space-y-2">
              {team.picks.map((pick, idx) => (
                <div key={idx} className="p-2 bg-gray-50 rounded flex justify-between items-center">
                  <div>
                    <span className="font-medium">Round {Math.floor(pick / 32) + 1}, Pick {pick % 32 || 32}</span>
                  </div>
                </div>
              ))}
            </div>
            
            <h3 className="font-bold text-lg mt-4 mb-2">Draft History</h3>
            <div className="space-y-1">
              {teamDraftHistory.length > 0 ? (
                teamDraftHistory.map((pick, idx) => (
                  <div key={idx} className="text-sm">
                    <span className="font-medium">Round {pick.round}, Pick {pick.pick}: </span>
                    <span>{pick.prospect.name}, {pick.prospect.position}</span>
                  </div>
                ))
              ) : (
                <div className="text-sm text-gray-500">No picks made yet in this draft</div>
              )}
            </div>
          </div>
        );
      case 'details':
        return (
          <div className="p-3">
            <h3 className="font-bold text-lg mb-2">Team Details</h3>
            
            <div className="mb-4">
              <h4 className="font-medium text-sm text-gray-500">Front Office</h4>
              <p className="text-sm">
                <span className="font-medium">Owner:</span> {team.ownership || 'Not specified'}
              </p>
              <p className="text-sm">
                <span className="font-medium">GM:</span> {team.generalManager || 'Not specified'}
              </p>
              <p className="text-sm">
                <span className="font-medium">Head Coach:</span> {team.headCoach || 'Not specified'}
              </p>
            </div>
            
            <div className="mb-4">
              <h4 className="font-medium text-sm text-gray-500">Draft Strategy</h4>
              <p className="text-sm">{team.trade_tendencies || 'No information available'}</p>
            </div>
            
            <div>
              <h4 className="font-medium text-sm text-gray-500">Recent Draft History</h4>
              <p className="text-sm">{team.recent_draft_history || 'No information available'}</p>
            </div>
          </div>
        );
      default:
        return null;
    }
  };
  
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div 
        className="bg-white rounded-lg shadow-lg w-full max-w-md max-h-screen overflow-hidden"
        style={{
          borderTop: `8px solid ${team.colors?.primary || '#0085CA'}`,
          borderBottom: `8px solid ${team.colors?.secondary || '#101820'}`
        }}
      >
        {/* Team header */}
        <div className="p-4 flex items-center">
          <div 
            className="w-16 h-16 rounded-full flex items-center justify-center mr-3"
            style={{ 
              backgroundColor: team.colors?.secondary || '#101820',
              borderColor: team.colors?.primary || '#0085CA',
              borderWidth: '2px'
            }}
          >
            <img 
              src={`/assets/logos/${team.abbreviation.toLowerCase()}.png`} 
              alt={`${team.name} logo`} 
              className="w-10 h-10"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = '/api/placeholder/32/32';
              }}
            />
          </div>
          <div>
            <h2 className="text-2xl font-bold">{team.name}</h2>
            <p className="text-gray-600">
              Pick #{team.picks[0]} | 2025 NFL Draft
            </p>
          </div>
          <button 
            className="ml-auto text-gray-400 hover:text-gray-600"
            onClick={onClose}
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex">
            <button
              className={`px-4 py-2 text-sm font-medium ${
                activeTab === 'needs' ? 
                'border-b-2 border-blue-500 text-blue-600' : 
                'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab('needs')}
            >
              Team Needs
            </button>
            <button
              className={`px-4 py-2 text-sm font-medium ${
                activeTab === 'picks' ? 
                'border-b-2 border-blue-500 text-blue-600' : 
                'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab('picks')}
            >
              Draft Picks
            </button>
            <button
              className={`px-4 py-2 text-sm font-medium ${
                activeTab === 'details' ? 
                'border-b-2 border-blue-500 text-blue-600' : 
                'text-gray-500 hover:text-gray-700'
              }`}
              onClick={() => setActiveTab('details')}
            >
              Details
            </button>
          </nav>
        </div>
        
        {/* Tab content */}
        <div className="overflow-y-auto" style={{ maxHeight: 'calc(80vh - 8rem)' }}>
          {renderTabContent()}
        </div>
      </div>
    </div>
  );
};

export default TeamCard;