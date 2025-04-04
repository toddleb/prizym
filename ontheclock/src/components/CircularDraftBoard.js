import React, { useContext, useEffect, useState } from 'react';
import { DraftContext } from '../context/DraftContext';

const CircularDraftBoard = () => {
  const { 
    teams, 
    prospects,
    currentPick, 
    currentRound,
    currentTeam,
    selectedProspect,
    setSelectedProspect,
    isUsersTurn,
    draftPlayer,
    aiDraftPlayer
  } = useContext(DraftContext);
  
  const [boardSize, setBoardSize] = useState({ width: 600, height: 600 });
  const [hoveredTeam, setHoveredTeam] = useState(null);
  const [timeLeft, setTimeLeft] = useState(300); // 5-minute draft clock (in seconds)
  
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
  
  // Update the timer every second
  useEffect(() => {
    if (!isUsersTurn) return; // Only run timer on user's turn
    
    const timer = setInterval(() => {
      setTimeLeft((prevTime) => {
        // If timer reaches 0, auto-draft and reset
        if (prevTime <= 1) {
          aiDraftPlayer(); // Auto-pick when time expires
          return 300; // Reset to 5 minutes
        }
        return prevTime - 1;
      });
    }, 1000);
    
    return () => clearInterval(timer);
  }, [isUsersTurn, aiDraftPlayer]);
  
  // Reset timer when it's a new pick
  useEffect(() => {
    setTimeLeft(300);
  }, [currentPick, currentRound]);
  
  if (!teams || teams.length === 0) {
    return <div className="text-center p-4">Loading teams...</div>;
  }
  
  const numTeams = teams.length;
  const centerX = boardSize.width / 2;
  const centerY = boardSize.height / 2;
  const radius = Math.min(centerX, centerY) - 110; // Leaving more space for team helmets
  
  // Get current team index
  const currentTeamIndex = teams.findIndex(team => 
    currentTeam && team.id === currentTeam.id
  );
  
  // Calculate position for each team
  const getTeamPosition = (index) => {
    const angle = ((index - currentTeamIndex) / numTeams) * 2 * Math.PI - Math.PI / 2; // Rotate based on current team
    const x = centerX + radius * Math.cos(angle);
    const y = centerY + radius * Math.sin(angle);
    return { x, y, angle };
  };
  
  // Show team tooltip
  const handleTeamHover = (team) => {
    setHoveredTeam(team);
  };
  
  // Handle prospect selection
  const handleSelectProspect = (prospect) => {
    setSelectedProspect(prospect);
  };
  
  // Handle draft button click
  const handleDraft = () => {
    if (selectedProspect && isUsersTurn) {
      draftPlayer(selectedProspect.id);
    }
  };
  
  // Calculate team needs (for demo purposes - in real app this would come from data)
  const getTeamNeeds = (team) => {
    return team.needs || [];
  };
  
  // Get top prospects by team need
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
    const teamNeeds = getTeamNeeds(currentTeam);
    return teamNeeds
      .map(position => {
        const positionProspects = prospectsByPosition[position] || [];
        return positionProspects[0];
      })
      .filter(Boolean)
      .slice(0, 3); // Limit to top 3
  };
  
  const teamNeeds = currentTeam ? getTeamNeeds(currentTeam) : [];
  const topProspects = getTopProspectsByNeed();
  
  // Calculate the timer percentage for the progress ring
  const timerPercentage = (timeLeft / 300) * 100; // Based on 5 minute clock
  const circumference = 2 * Math.PI * 30; // 30 is the radius of the timer ring
  
  // Format time as MM:SS
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };
  
  return (
    <div className="circular-draft-board-container relative w-full h-[80vh] overflow-hidden rounded-xl border-4 border-gray-800 shadow-2xl">
      {/* Football field background */}
      <div className="absolute inset-0 bg-green-600">
        {/* Field markings */}
        <div className="absolute inset-0 flex flex-col">
          {/* Field lines */}
          {[...Array(11)].map((_, i) => (
            <div 
              key={i} 
              className="w-full h-px bg-white opacity-30 absolute" 
              style={{ top: `${i * 10}%` }}
            ></div>
          ))}
          
          {/* Middle field line */}
          <div className="absolute top-1/2 left-0 right-0 h-1 bg-white opacity-60 -translate-y-1/2"></div>
          
          {/* End zones */}
          <div className="absolute top-0 left-0 right-0 h-1/6 bg-red-800 opacity-20"></div>
          <div className="absolute bottom-0 left-0 right-0 h-1/6 bg-blue-800 opacity-20"></div>
          
          {/* Hash marks */}
          <div className="absolute top-1/4 left-1/3 w-1/3 h-px bg-white opacity-50"></div>
          <div className="absolute top-3/4 left-1/3 w-1/3 h-px bg-white opacity-50"></div>
        </div>
      </div>
      
      <div className="text-center z-10 mb-4 relative pt-4">
        <h2 className="text-2xl font-bold text-white drop-shadow-md">2025 NFL Draft - Round {currentRound}</h2>
      </div>
      
      <div className="relative w-full h-4/5">
        {/* Center team info area */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-white rounded-full shadow-lg flex flex-col items-center justify-center p-4 z-20 border-4 border-blue-500">
          {/* Timer ring */}
          <svg className="absolute top-0 left-0 w-full h-full -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="30"
              fill="none"
              stroke="#e5e7eb"
              strokeWidth="4"
            />
            <circle
              cx="50"
              cy="50"
              r="30"
              fill="none"
              stroke={timeLeft < 60 ? "#ef4444" : "#3b82f6"}
              strokeWidth="4"
              strokeDasharray={circumference}
              strokeDashoffset={circumference - (timerPercentage / 100) * circumference}
              strokeLinecap="round"
              className="transition-all duration-1000 ease-linear"
            />
          </svg>
          
          {currentTeam && (
            <>
              <div className="text-center mb-2 z-10">
                <h3 className="text-xl font-bold text-blue-800">On The Clock</h3>
                <div className="flex items-center justify-center my-1">
                  <div 
                    className="w-10 h-10 rounded-full bg-cover bg-center mr-2 flex items-center justify-center"
                    style={{ 
                      backgroundColor: currentTeam.colors?.secondary || '#CCCCCC',
                      borderColor: currentTeam.colors?.primary || '#333333',
                      borderWidth: '2px'
                    }}
                  >
                    <img 
                      src={`/assets/logos/${currentTeam.abbreviation?.toLowerCase()}.png`}
                      alt={`${currentTeam.name} logo`}
                      className="w-7 h-7"
                      onError={(e) => {
                        e.target.onerror = null;
                        e.target.src = '/api/placeholder/32/32';
                      }}
                    />
                  </div>
                  <span className="text-lg font-bold">{currentTeam.name}</span>
                </div>
                <p className="text-sm text-gray-600">Pick #{currentPick}</p>
                <p className={`font-bold text-lg ${timeLeft < 60 ? 'text-red-600' : 'text-blue-600'}`}>
                  {formatTime(timeLeft)}
                </p>
              </div>
              
              {isUsersTurn && (
                <div className="w-full z-10">
                  <h4 className="text-sm font-bold border-b border-gray-200 mb-1">Team Needs</h4>
                  <div className="flex flex-wrap justify-center gap-1 mb-2">
                    {teamNeeds.map((position, i) => (
                      <span key={i} className={`px-2 py-1 ${
                        i === 0 ? 'bg-red-100 text-red-800' :
                        i <= 2 ? 'bg-orange-100 text-orange-800' :
                        'bg-yellow-100 text-yellow-800'
                      } text-xs rounded-full`}>
                        {position}
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
                        onClick={() => handleSelectProspect(prospect)}
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
              )}
              
              {!isUsersTurn && (
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
        {teams.map((team, index) => {
          const position = getTeamPosition(index);
          const isActive = currentTeam && team.id === currentTeam.id;
          
          return (
            <div 
              key={team.id}
              className={`absolute cursor-pointer transition-all duration-500 ${
                isActive ? 'z-20 scale-110' : 'z-10 hover:scale-105'
              }`}
              style={{ 
                left: position.x,
                top: position.y,
                transform: 'translate(-50%, -50%)'
              }}
              onMouseEnter={() => handleTeamHover(team)}
              onMouseLeave={() => handleTeamHover(null)}
            >
              {/* Football Helmet Design */}
              <div className="relative w-20 h-16">
                {/* Helmet Shape */}
                <div 
                  className="absolute inset-0 rounded-t-full rounded-b-lg transform skew-x-6 shadow-md"
                  style={{backgroundColor: team.colors?.primary || '#333333'}}
                ></div>
                
                {/* Helmet Stripe */}
                <div 
                  className="absolute top-0 bottom-0 left-1/2 w-2 transform -translate-x-1/2"
                  style={{backgroundColor: team.colors?.secondary || '#FFFFFF'}}
                ></div>
                
                {/* Facemask */}
                <div 
                  className="absolute bottom-0 left-0 right-0 h-6 w-10 ml-5 rounded-r-md rounded-l-sm"
                  style={{backgroundColor: team.colors?.secondary || '#FFFFFF'}}
                ></div>
                
                {/* Team Logo on Helmet */}
                <div className={`absolute top-1 left-5 w-10 h-10 bg-white rounded-full flex items-center justify-center ${
                  isActive ? 'border-2 border-yellow-500' : 'border border-gray-300'
                }`}>
                  <img 
                    src={`/assets/logos/${team.abbreviation?.toLowerCase()}.png`} 
                    alt={`${team.name} logo`} 
                    className="w-7 h-7"
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.src = '/api/placeholder/32/32';
                    }}
                  />
                </div>
                
                {/* Team name below helmet */}
                <div className="absolute -bottom-5 left-0 right-0 text-center">
                  <span className="text-xs font-bold text-white leading-none drop-shadow-md">{team.abbreviation}</span>
                  <div className="text-xs text-white leading-none drop-shadow-md">
                    #{team.picks ? team.picks[0] : index + 1}
                  </div>
                </div>
                
                {/* Highlight for active team */}
                {isActive && (
                  <div className="absolute -inset-1 bg-yellow-200 rounded-full opacity-50 animate-pulse -z-10"></div>
                )}
              </div>
            </div>
          );
        })}
        
        {/* Active team indicator - line pointing to center */}
        {currentTeamIndex >= 0 && (
          <div 
            className="absolute top-1/2 left-1/2 h-1 bg-yellow-500 origin-left z-0"
            style={{
              width: radius,
              transform: `rotate(${getTeamPosition(currentTeamIndex).angle}rad)`
            }}
          ></div>
        )}
      </div>
      
      {/* Team hover tooltip */}
      {hoveredTeam && (
        <div 
          className="absolute z-30 bg-white p-3 rounded-lg shadow-lg border border-gray-300"
          style={{ 
            top: '10%',
            right: '10%',
            maxWidth: '200px'
          }}
        >
          <h4 className="font-bold text-lg" style={{ color: hoveredTeam.colors?.primary || '#333333' }}>
            {hoveredTeam.name}
          </h4>
          <p className="text-sm mt-1">
            Picks: {hoveredTeam.picks ? hoveredTeam.picks.slice(0, 3).join(', ') : 'None'}
            {hoveredTeam.picks && hoveredTeam.picks.length > 3 ? '...' : ''}
          </p>
          <p className="text-sm mt-1">
            Needs: {hoveredTeam.needs ? hoveredTeam.needs.join(', ') : 'Unknown'}
          </p>
        </div>
      )}
    </div>
  );
};

export default CircularDraftBoard;