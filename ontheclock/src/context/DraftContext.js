import React, { createContext, useState, useEffect } from 'react';
import { teams as initialTeams } from '../data/teams';
import { prospects as initialProspects } from '../data/prospects';

export const DraftContext = createContext();

export const DraftProvider = ({ children }) => {
  // State for teams, prospects, and draft status
  const [teams, setTeams] = useState(initialTeams);
  const [prospects, setProspects] = useState(initialProspects);
  const [draftHistory, setDraftHistory] = useState([]);
  const [currentRound, setCurrentRound] = useState(1);
  const [currentPick, setCurrentPick] = useState(1);
  const [activeTeamIndex, setActiveTeamIndex] = useState(0);
  const [selectedProspect, setSelectedProspect] = useState(null);
  const [userTeam, setUserTeam] = useState(null);
  const [draftMode, setDraftMode] = useState('solo'); // 'solo', 'spectator', or 'multiplayer'
  const [isSimulating, setIsSimulating] = useState(false);
  
  // Computed current team
  const currentTeam = teams[activeTeamIndex];
  
  // Check if it's the user's turn
  const isUsersTurn = draftMode === 'solo' && userTeam && userTeam.id === currentTeam?.id;
  
  // Set initial draft order based on first pick of each team
  useEffect(() => {
    // Could sort teams by their first pick here if needed
    // For now, we'll use the order they're defined in teams.js
  }, []);
  
  // Select a team (user action)
  const selectTeam = (teamId) => {
    const team = teams.find(t => t.id === teamId);
    if (team) {
      setUserTeam(team);
    }
  };
  
  // Draft a player (user action)
  const draftPlayer = (playerId) => {
    // Find the player
    const player = prospects.find(p => p.id === playerId);
    
    // Only allow drafting if there's a selected player
    if (!player) return;
    
    // Add to draft history
    const draftPick = {
      round: currentRound,
      pick: currentPick,
      team: currentTeam.name,
      teamId: currentTeam.id,
      prospect: player,
      playerId: player.id,
    };
    
    setDraftHistory([...draftHistory, draftPick]);
    
    // Remove player from available prospects
    setProspects(prospects.filter(p => p.id !== playerId));
    
    // Reset selected prospect
    setSelectedProspect(null);
    
    // Advance to next team
    advancePick();
  };
  
  // AI makes a draft selection
  const aiDraftPlayer = () => {
    if (isUsersTurn || prospects.length === 0) return;
    
    // Get team needs
    const needs = currentTeam.needs || [];
    
    // Group prospects by position
    const prospectsByPosition = {};
    prospects.forEach(prospect => {
      if (!prospectsByPosition[prospect.position]) {
        prospectsByPosition[prospect.position] = [];
      }
      prospectsByPosition[prospect.position].push(prospect);
    });
    
    // Sort each position group by grade
    Object.keys(prospectsByPosition).forEach(position => {
      prospectsByPosition[position].sort((a, b) => b.grade - a.grade);
    });
    
    // First check if a top-graded player at a position of need is available
    let aiPick = null;
    for (const need of needs) {
      const positionProspects = prospectsByPosition[need] || [];
      if (positionProspects.length > 0) {
        aiPick = positionProspects[0];
        break;
      }
    }
    
    // If no position of need, take best player available
    if (!aiPick) {
      const sortedProspects = [...prospects].sort((a, b) => b.grade - a.grade);
      aiPick = sortedProspects[0];
    }
    
    // Add to draft history
    const draftPick = {
      round: currentRound,
      pick: currentPick,
      team: currentTeam.name,
      teamId: currentTeam.id,
      prospect: aiPick,
      playerId: aiPick.id,
    };
    
    setDraftHistory([...draftHistory, draftPick]);
    
    // Remove player from available prospects
    setProspects(prospects.filter(p => p.id !== aiPick.id));
    
    // Advance to next pick
    advancePick();
  };
  
  // Advance to the next pick
  const advancePick = () => {
    const nextTeamIndex = (activeTeamIndex + 1) % teams.length;
    
    // If we've gone through all teams, advance to next round
    if (nextTeamIndex === 0) {
      setCurrentRound(currentRound + 1);
    }
    
    setActiveTeamIndex(nextTeamIndex);
    setCurrentPick(currentPick + 1);
  };
  
  // Start simulating the draft automatically
  const startSimulation = () => {
    setIsSimulating(true);
  };
  
  // Stop simulating the draft
  const stopSimulation = () => {
    setIsSimulating(false);
  };
  
  // Effect to handle AI picks when simulating
  useEffect(() => {
    let timeoutId;
    
    if (isSimulating && !isUsersTurn) {
      timeoutId = setTimeout(() => {
        aiDraftPlayer();
      }, 2000); // 2 second delay between picks
    }
    
    return () => clearTimeout(timeoutId);
  }, [isSimulating, isUsersTurn, currentPick, currentRound]);
  
  // Reset the draft
  const resetDraft = () => {
    setProspects(initialProspects);
    setDraftHistory([]);
    setCurrentRound(1);
    setCurrentPick(1);
    setActiveTeamIndex(0);
    setSelectedProspect(null);
    setIsSimulating(false);
  };
  
  // Provide all the draft state and functions
  const contextValue = {
    teams,
    prospects,
    draftHistory,
    currentRound,
    currentPick,
    currentTeam,
    activeTeamIndex,
    selectedProspect,
    userTeam,
    isUsersTurn,
    isSimulating,
    draftMode,
    selectTeam,
    setSelectedProspect,
    draftPlayer,
    aiDraftPlayer,
    startSimulation,
    stopSimulation,
    setDraftMode,
    resetDraft
  };
  
  return (
    <DraftContext.Provider value={contextValue}>
      {children}
    </DraftContext.Provider>
  );
};

export default DraftProvider;