import React, { useContext, useEffect, useState } from 'react';
import { DraftContext } from '../context/DraftContext';

const CircularDraftBoard = ({ selectedProspect, setSelectedProspect }) => {
  const { 
    teams, 
    prospects,
    currentPick, 
    currentRound,
    currentTeam,
    isUsersTurn,
    draftPlayer
  } = useContext(DraftContext);
  
  const [boardSize, setBoardSize] = useState({ width: 600, height: 600 });
  const [timeLeft, setTimeLeft] = useState(300); // 5-minute draft clock
  
  // Calculate responsive dimensions
  useEffect(() => {
    const handleResize = () => {
      const size = Math.min(window.innerWidth * 0.8, window.innerHeight * 0.8, 800);
      setBoardSize({ width: size, height: size });
    };
    
    window.addEventListener('resize', handleResize);
    handleResize();
    
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  if (!teams || teams.length === 0) {
    return <div className="text-center p-4">Loading teams...</div>;
  }
  
  // Calculate position for each team in a circle
  const getTeamPosition = (index, activeIndex) => {
    const totalTeams = teams.length;
    const angleIncrement = 360 / Math.min(totalTeams, 32); // Cap at 32 teams for visual clarity
    const angle = (index * angleIncrement) - (activeIndex * angleIncrement);
    const radius = 35; // in vh units
    
    // Convert polar coordinates to Cartesian
    const x = radius * Math.sin(angle * Math.PI / 180);
    const y = -radius * Math.cos(angle * Math.PI / 180);
    
    return {
      transform: `translate(${x}vh, ${y}vh)`,
      transition: 'transform 1s ease-in-out'
    };
  };
  
  // Get filtered top prospects by team need
  const getTopProspectsByNeed = () => {
    if (!currentTeam || !prospects || prospects.length === 0) return [];
    
    // Group prospects by position
    const prospectsByPosition = {};
    prospects.forEach(prospect => {
      if (!prospectsByPosition[prospect.position]) {
        prospectsByPosition[prospect.position] = [];
      }
      prospectsByPosition[prospect.position].push(prospect);
    });
    
    // Sort by grade within each position
    Object.keys(prospectsByPosition).forEach(position => {
      prospectsByPosition[position].sort((a, b) => b.grade - a.grade);
    });
    
    // Get top prospect for each need position
    return currentTeam.needs
      .map(position => {
        const positionProspects = prospectsByPosition[position] || [];
        return positionProspects[0];
      })
      .filter(Boolean)
      .slice(0, 3); // Limit to top 3
  };
  
  const teamNeeds = currentTeam ? currentTeam.needs.map(pos => ({
    position: pos,
    priority: pos === currentTeam.needs[0] ? 'High' : 
             pos === currentTeam.needs[1] ? 'Medium' : 'Low'
  })) : [];
  
  const topProspects = getTopProspectsByNeed();
  
  // Format time as MM:SS
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };
  
  // Handle draft button click
  const handleDraft = () => {
    if (selectedProspect && isUsersTurn) {
      draftPlayer(selectedProspect.id);
      setSelectedProspect(null);
    }
  };
  
  // Get current team index
  const currentTeamIndex = teams.findIndex(team => 
    currentTeam && team.id === currentTeam.id
  );
  
  return (
    <div className="w-full h-full bg-green-600 flex flex-col items-center justify-center relative overflow-hidden">
      <div className="text-center z-10 mb-4">
        <h2 className="text-2xl font-bold text-white">2025 NFL Draft - Round {currentRound}</h2>
      </div>
      
      <div className="relative w-full h-4/5">
        {/* Center team info area */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-white rounded-full shadow-lg flex flex-col items-center justify-center p-4 z-20 border-4 border-blue-500">
          {currentTeam && (
            <>
              <div className="text-center mb-2">
                <h3 className="text-xl font-bold text-blue-800">On The Clock</h3>
                <div className="flex items-center justify-center my-1">
                  <div 
                    className="w-10 h-10 rounded-full flex items-center justify-center"
                    style={{ 
                      backgroundColor: currentTeam.colors.secondary,
                      borderColor: currentTeam.colors.primary,
                      borderWidth: '2px'
                    }}
                  >
                    <img 
                      src={`/api/placeholder/32/32`}
                      alt={`${currentTeam.name} logo`}
                      className="w-7 h-7"
                    />
                  </div>
                  <span className="text-lg font-bold ml-2">{currentTeam.name}</span>
                </div>
                <p className="text-sm text-gray-600">Pick #{currentPick}</p>
                <p className="font-bold text-lg text-blue-600">
                  {formatTime(timeLeft)}
                </p>
              </div>
              
              {isUsersTurn ? (
                <div className="w-full">
                  <h4 className="text-sm font-bold border-b border-gray-200 mb-1">Team Needs</h4>
                  <div className="flex flex-wrap justify-center gap-1 mb-2">
                    {teamNeeds.map((need, i) => (
                      <span key={i} className={`px-2 py-1 ${
                        need.priority === 'High' ? 'bg-red-100 text-red-800' :
                        need.priority === 'Medium' ? 'bg-orange-100 text-orange-800' :
                        'bg-yellow-100 text-yellow-800'
                      } text-xs rounded-full`}>
                        {need.position}
                      </span>
                    ))}
                  </div>
                  
                  <h4 className="text-sm font-bold border-b border-gray-200 mb-1">Top Available</h4>
                  <div className="overflow-y-auto max-h-16">
                    {topProspects.map(prospect => (
                      <div 
                        key={prospect.id} 
                        className={`text-xs p-1 hover:bg-gray-100 flex justify-between cursor-pointer ${
                          selectedProspect && selectedProspect.id === prospect.id ? 'bg-blue-100' : ''
                        }`}
                        onClick={() => setSelectedProspect(prospect)}
                      >
                        <span className="font-medium">{prospect.name} ({prospect.position})</span>
                        <span className="text-blue-600">{prospect.grade.toFixed(1)}</span>
                      </div>
                    ))}
                  </div>
                  
                  <button 
                    className={`w-full mt-2 py-1 text-sm rounded ${
                      selectedProspect 
                        ? 'bg-green-500 hover:bg-green-600 text-white' 
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                    }`}
                    onClick={handleDraft}
                    disabled={!selectedProspect}
                  >
                    {selectedProspect ? `Draft ${selectedProspect.name}` : 'Select a Player'}
                  </button>
                </div>
              ) : (
                <div className="text-center mt-2">
                  <p className="text-sm text-gray-600">AI is making a selection...</p>
                  <div className="flex justify-center mt-2">
                    <div className="animate-pulse w-6 h-6 rounded-full bg-blue-500 mx-1"></div>
                    <div className="animate-pulse w-6 h-6 rounded-full bg-blue-500 mx-1" style={{ animationDelay: '0.2s' }}></div>
                    <div className="animate-pulse w-6 h-6 rounded-full bg-blue-500 mx-1" style={{ animationDelay: '0.4s' }}></div>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
        
        {/* Teams positioned in a circle */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          {teams.slice(0, 16).map((team, index) => (
            <div 
              key={team.id} 
              className="absolute transform -translate-x-1/2 -translate-y-1/2 transition-all duration-500"
              style={getTeamPosition(index, currentTeamIndex)}
            >
              {/* Football Helmet Design */}
              <div className={`relative w-20 h-16 ${
                index === currentTeamIndex ? 'z-20' : 'z-10'
              }`}>
                {/* Helmet Shape */}
                <div 
                  className="absolute inset-0 rounded-t-full rounded-b-lg transform skew-x-6 shadow-md"
                  style={{backgroundColor: team.colors.primary}}
                ></div>
                
                {/* Facemask */}
                <div 
                  className="absolute bottom-0 left-0 right-0 h-6 w-10 ml-5 rounded-r-md rounded-l-sm"
                  style={{backgroundColor: team.colors.secondary}}
                ></div>
                
                {/* Team Logo on Helmet */}
                <div className={`absolute top-1 left-5 w-10 h-10 bg-white rounded-full flex items-center justify-center ${
                  index === currentTeamIndex ? 'border-2 border-yellow-500' : 'border border-gray-300'
                }`}>
                  <img 
                    src="/api/placeholder/32/32" 
                    alt={`${team.name} logo`} 
                    className="w-7 h-7" 
                  />
                </div>
                
                {/* Team name below helmet */}
                <div className="absolute -bottom-5 left-0 right-0 text-center">
                  <span className="text-xs font-bold text-white">{team.abbreviation}</span>
                  <div className="text-xs text-white">#{team.picks[0]}</div>
                </div>
                
                {/* Highlight for active team */}
                {index === currentTeamIndex && (
                  <div className="absolute -inset-1 bg-yellow-200 rounded-full opacity-50 animate-pulse -z-10"></div>
                )}
              </div>
            </div>
          ))}
        </div>
        
        {/* Active team indicator - line pointing to center */}
        <div 
          className="absolute top-1/2 left-1/2 h-1 bg-yellow-500 origin-left z-0"
          style={{
            width: '35vh',
            transform: `rotate(0deg)`
          }}
        ></div>
      </div>
    </div>
  );
};

export default CircularDraftBoard;