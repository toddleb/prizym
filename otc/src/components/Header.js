import React, { useContext } from 'react';
import { DraftContext } from '../context/DraftContext';

const Header = ({ setActiveTab, activeTab }) => {
  const { 
    currentRound, 
    currentPick, 
    currentTeam, 
    userTeam,
    draftMode,
    setDraftMode,
    isSimulating,
    startSimulation,
    stopSimulation,
    resetDraft
  } = useContext(DraftContext);
  
  return (
    <header className="bg-gray-800 text-white">
      <div className="container mx-auto px-4 py-4">
        <div className="flex flex-col md:flex-row md:justify-between md:items-center">
          <div className="flex items-center mb-4 md:mb-0">
            <h1 className="text-2xl font-bold mr-2">On The Clock</h1>
            <span className="bg-yellow-500 text-black px-2 py-1 rounded text-xs font-bold">
              2025 NFL Draft
            </span>
          </div>
          
          <div className="flex space-x-2 mb-4 md:mb-0">
            <select 
              className="bg-gray-700 text-white rounded px-2 py-1 text-sm"
              value={draftMode}
              onChange={(e) => setDraftMode(e.target.value)}
            >
              <option value="solo">Solo Mode</option>
              <option value="spectator">Spectator Mode</option>
              <option value="multiplayer">Multiplayer (Coming Soon)</option>
            </select>
            
            <button 
              className={`px-3 py-1 rounded text-sm ${
                isSimulating 
                  ? 'bg-red-600 hover:bg-red-700' 
                  : 'bg-green-600 hover:bg-green-700'
              }`}
              onClick={isSimulating ? stopSimulation : startSimulation}
            >
              {isSimulating ? 'Stop Sim' : 'Start Sim'}
            </button>
            
            <button 
              className="bg-gray-600 hover:bg-gray-700 px-3 py-1 rounded text-sm"
              onClick={resetDraft}
            >
              Reset
            </button>
          </div>
          
          {userTeam && (
            <div className="flex items-center mb-4 md:mb-0">
              <span className="mr-2">Your Team:</span>
              <div 
                className="w-8 h-8 rounded-full bg-cover bg-center mr-2 flex items-center justify-center"
                style={{ 
                  backgroundColor: userTeam.colors.secondary,
                  borderColor: userTeam.colors.primary,
                  borderWidth: '2px'
                }}
              >
                <img 
                  src={`/assets/logos/${userTeam.abbreviation.toLowerCase()}.png`}
                  alt={`${userTeam.name} logo`}
                  className="w-6 h-6"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = '/api/placeholder/32/32';
                  }}
                />
              </div>
              <span className="font-bold">{userTeam.name}</span>
            </div>
          )}
          
          <div className="draft-status flex items-center mb-4 md:mb-0">
            <div className="mr-4">
              <span className="text-gray-400 text-sm">Round</span>
              <span className="ml-2 font-bold">{currentRound}</span>
            </div>
            <div className="mr-4">
              <span className="text-gray-400 text-sm">Pick</span>
              <span className="ml-2 font-bold">{currentPick}</span>
            </div>
            {currentTeam && (
              <div>
                <span className="text-gray-400 text-sm">On The Clock</span>
                <span className="ml-2 font-bold">{currentTeam.abbreviation}</span>
              </div>
            )}
          </div>
        </div>
        
        <nav className="mt-4">
          <ul className="flex border-b border-gray-700">
            <li className="-mb-px mr-1">
              <button
                className={`inline-block py-2 px-4 ${
                  activeTab === 'draft'
                    ? 'text-yellow-500 border-b-2 border-yellow-500 font-bold'
                    : 'text-gray-300 hover:text-white'
                }`}
                onClick={() => setActiveTab('draft')}
              >
                Draft Board
              </button>
            </li>
            <li className="mr-1">
              <button
                className={`inline-block py-2 px-4 ${
                  activeTab === 'teams'
                    ? 'text-yellow-500 border-b-2 border-yellow-500 font-bold'
                    : 'text-gray-300 hover:text-white'
                }`}
                onClick={() => setActiveTab('teams')}
              >
                Teams
              </button>
            </li>
            <li className="mr-1">
              <button
                className={`inline-block py-2 px-4 ${
                  activeTab === 'history'
                    ? 'text-yellow-500 border-b-2 border-yellow-500 font-bold'
                    : 'text-gray-300 hover:text-white'
                }`}
                onClick={() => setActiveTab('history')}
              >
                Draft History
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;