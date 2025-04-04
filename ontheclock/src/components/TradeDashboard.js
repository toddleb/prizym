import React, { useState, useContext, useEffect } from 'react';
import { DraftContext } from '../context/DraftContext';
import { calculateTradeValue } from '../utils/tradeCalculator';

const TradeDashboard = () => {
  const { teams, currentTeam, userTeam, draftHistory } = useContext(DraftContext);
  
  const [tradePartner, setTradePartner] = useState(null);
  const [userTeamPicks, setUserTeamPicks] = useState([]);
  const [partnerTeamPicks, setPartnerTeamPicks] = useState([]);
  const [userSelectedPicks, setUserSelectedPicks] = useState([]);
  const [partnerSelectedPicks, setPartnerSelectedPicks] = useState([]);
  const [tradeEvaluation, setTradeEvaluation] = useState(null);
  const [suggestedTrade, setSuggestedTrade] = useState(null);
  const [activeTab, setActiveTab] = useState('propose');
  
  // Initialize user team picks
  useEffect(() => {
    if (userTeam) {
      // Filter out picks already used in draft
      const picksUsed = draftHistory.map(pick => pick.pick);
      const availablePicks = userTeam.picks.filter(pick => !picksUsed.includes(pick));
      setUserTeamPicks(availablePicks);
    }
  }, [userTeam, draftHistory]);
  
  // Update partner team picks when trade partner is selected
  useEffect(() => {
    if (tradePartner) {
      // Filter out picks already used in draft
      const picksUsed = draftHistory.map(pick => pick.pick);
      const availablePicks = tradePartner.picks.filter(pick => !picksUsed.includes(pick));
      setPartnerTeamPicks(availablePicks);
      
      // Reset selections
      setPartnerSelectedPicks([]);
      setTradeEvaluation(null);
    }
  }, [tradePartner, draftHistory]);
  
  // Auto-generate a suggested trade whenever partner changes
  useEffect(() => {
    if (tradePartner && userTeam) {
      suggestBalancedTrade();
    }
  }, [tradePartner]);
  
  // Toggle selection of a user team pick
  const toggleUserPickSelection = (pick) => {
    if (userSelectedPicks.includes(pick)) {
      setUserSelectedPicks(userSelectedPicks.filter(p => p !== pick));
    } else {
      setUserSelectedPicks([...userSelectedPicks, pick]);
    }
  };
  
  // Toggle selection of a partner team pick
  const togglePartnerPickSelection = (pick) => {
    if (partnerSelectedPicks.includes(pick)) {
      setPartnerSelectedPicks(partnerSelectedPicks.filter(p => p !== pick));
    } else {
      setPartnerSelectedPicks([...partnerSelectedPicks, pick]);
    }
  };
  
  // Evaluate the current trade proposal
  const evaluateTrade = () => {
    if (userSelectedPicks.length === 0 || partnerSelectedPicks.length === 0) {
      return;
    }
    
    const userValue = userSelectedPicks.reduce((total, pick) => {
      // Calculate round and pick number
      const round = Math.floor(pick / 32) + 1;
      const pickNumber = pick % 32 || 32;
      return total + calculateTradeValue(pick);
    }, 0);
    
    const partnerValue = partnerSelectedPicks.reduce((total, pick) => {
      // Calculate round and pick number
      const round = Math.floor(pick / 32) + 1;
      const pickNumber = pick % 32 || 32;
      return total + calculateTradeValue(pick);
    }, 0);
    
    const difference = Math.abs(userValue - partnerValue);
    const percentDiff = difference / Math.max(userValue, partnerValue) * 100;
    
    setTradeEvaluation({
      userValue: userValue.toFixed(0),
      partnerValue: partnerValue.toFixed(0),
      difference: difference.toFixed(0),
      percentDifference: percentDiff.toFixed(1),
      favors: userValue < partnerValue ? "You" : partnerValue < userValue ? "Partner" : "Equal"
    });
  };
  
  // Auto-suggest a balanced trade
  const suggestBalancedTrade = () => {
    if (!tradePartner || !userTeam) return;
    
    // Start with partner's highest pick as the target
    const partnerPicks = [...partnerTeamPicks].sort((a, b) => a - b);
    if (partnerPicks.length === 0) return;
    
    const targetPick = partnerPicks[0]; // Highest pick (lowest number)
    const targetValue = calculateTradeValue(targetPick);
    
    // Sort user picks by value (ascending)
    const sortedUserPicks = [...userTeamPicks].sort((a, b) => a - b);
    
    let bestCombo = [];
    let bestDiff = Infinity;
    
    // Try 1-pick trades
    for (const pick of sortedUserPicks) {
      const pickValue = calculateTradeValue(pick);
      const diff = Math.abs(pickValue - targetValue);
      
      if (diff < bestDiff) {
        bestDiff = diff;
        bestCombo = [pick];
      }
    }
    
    // Try 2-pick trades if needed
    if (bestDiff > targetValue * 0.15) {
      for (let i = 0; i < sortedUserPicks.length; i++) {
        for (let j = i + 1; j < sortedUserPicks.length; j++) {
          const combinedValue = calculateTradeValue(sortedUserPicks[i]) + 
                                calculateTradeValue(sortedUserPicks[j]);
          const diff = Math.abs(combinedValue - targetValue);
          
          if (diff < bestDiff) {
            bestDiff = diff;
            bestCombo = [sortedUserPicks[i], sortedUserPicks[j]];
          }
        }
      }
    }
    
    // Format picks for display
    const formatPick = (pick) => {
      const round = Math.floor(pick / 32) + 1;
      const pickNumber = pick % 32 || 32;
      return `Round ${round}, Pick ${pickNumber}`;
    };
    
    const userValue = bestCombo.reduce((sum, pick) => sum + calculateTradeValue(pick), 0);
    
    setSuggestedTrade({
      targetPick: formatPick(targetPick),
      targetValue: targetValue.toFixed(0),
      suggestedPicks: bestCombo.map(formatPick),
      suggestedPicksRaw: bestCombo,
      userValue: userValue.toFixed(0),
      difference: Math.abs(userValue - targetValue).toFixed(0),
      percentDifference: (Math.abs(userValue - targetValue) / Math.max(userValue, targetValue) * 100).toFixed(1),
      favors: userValue < targetValue ? "You" : targetValue < userValue ? "Partner" : "Equal"
    });
  };
  
  // Apply the suggested trade
  const applySuggestedTrade = () => {
    if (!suggestedTrade) return;
    
    setUserSelectedPicks(suggestedTrade.suggestedPicksRaw);
    setPartnerSelectedPicks([partnerTeamPicks[0]]);
    
    evaluateTrade();
  };
  
  // Accept the trade (would normally send to context/backend)
  const acceptTrade = () => {
    // In a real implementation, this would call a method from DraftContext
    // to execute the trade, update team picks, etc.
    alert("Trade accepted! This would update the draft state in a full implementation.");
  };
  
  // Reset the trade interface
  const resetTrade = () => {
    setUserSelectedPicks([]);
    setPartnerSelectedPicks([]);
    setTradeEvaluation(null);
  };
  
  // Format a pick for display
  const formatPickDisplay = (pick) => {
    const round = Math.floor(pick / 32) + 1;
    const pickNumber = pick % 32 || 32;
    return `R${round}P${pickNumber} (${calculateTradeValue(pick)})`;
  };
  
  // Render pick list with selection functionality
  const renderPickList = (picks, selectedPicks, toggleFn, teamColors) => {
    return (
      <div className="grid grid-cols-2 gap-2 mt-2">
        {picks.map((pick) => (
          <div 
            key={pick}
            className={`p-2 text-sm rounded cursor-pointer ${
              selectedPicks.includes(pick) 
                ? `bg-${teamColors.primary} text-white` 
                : 'bg-gray-100 hover:bg-gray-200'
            }`}
            onClick={() => toggleFn(pick)}
          >
            {formatPickDisplay(pick)}
          </div>
        ))}
      </div>
    );
  };
  
  // Render trade evaluation results
  const renderTradeEvaluation = () => {
    if (!tradeEvaluation) return null;
    
    const fairnessColor = 
      parseFloat(tradeEvaluation.percentDifference) < 10 ? 'text-green-600' :
      parseFloat(tradeEvaluation.percentDifference) < 20 ? 'text-yellow-600' :
      'text-red-600';
    
    return (
      <div className="mt-4 p-3 bg-gray-50 rounded border">
        <h3 className="font-bold text-lg mb-2">Trade Evaluation</h3>
        
        <div className="grid grid-cols-2 gap-4 mb-2">
          <div>
            <div className="text-sm text-gray-500">Your Value</div>
            <div className="text-xl font-bold">{tradeEvaluation.userValue}</div>
          </div>
          <div>
            <div className="text-sm text-gray-500">Partner Value</div>
            <div className="text-xl font-bold">{tradeEvaluation.partnerValue}</div>
          </div>
        </div>
        
        <div className="border-t pt-2 mt-2">
          <div className="flex justify-between items-center">
            <div>
              <span className="text-sm text-gray-500">Difference: </span>
              <span className={fairnessColor}>{tradeEvaluation.difference} points ({tradeEvaluation.percentDifference}%)</span>
            </div>
            <div>
              <span className="text-sm text-gray-500">Trade favors: </span>
              <span className="font-medium">{tradeEvaluation.favors}</span>
            </div>
          </div>
          
          <div className="mt-4 flex space-x-2">
            <button
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 flex-1"
              onClick={acceptTrade}
            >
              Accept Trade
            </button>
            <button
              className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100"
              onClick={resetTrade}
            >
              Reset
            </button>
          </div>
        </div>
      </div>
    );
  };
  
  // Render suggested trade results
  const renderSuggestedTrade = () => {
    if (!suggestedTrade) return null;
    
    const fairnessColor = 
      parseFloat(suggestedTrade.percentDifference) < 10 ? 'text-green-600' :
      parseFloat(suggestedTrade.percentDifference) < 20 ? 'text-yellow-600' :
      'text-red-600';
    
    return (
      <div className="mt-4 p-3 bg-gray-50 rounded border">
        <h3 className="font-bold text-lg mb-2">Suggested Trade</h3>
        
        <div className="mb-3">
          <div className="text-sm text-gray-500">Partner gives:</div>
          <div className="font-medium">{suggestedTrade.targetPick} (Value: {suggestedTrade.targetValue})</div>
        </div>
        
        <div className="mb-3">
          <div className="text-sm text-gray-500">You give:</div>
          {suggestedTrade.suggestedPicks.map((pick, idx) => (
            <div key={idx} className="font-medium">{pick}</div>
          ))}
          <div className="text-sm mt-1">Total Value: {suggestedTrade.userValue}</div>
        </div>
        
        <div className="border-t pt-2 mt-2">
          <div className="flex justify-between items-center">
            <div>
              <span className="text-sm text-gray-500">Difference: </span>
              <span className={fairnessColor}>{suggestedTrade.difference} points ({suggestedTrade.percentDifference}%)</span>
            </div>
            <div>
              <span className="text-sm text-gray-500">Trade favors: </span>
              <span className="font-medium">{suggestedTrade.favors}</span>
            </div>
          </div>
          
          <button
            className="mt-4 w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            onClick={applySuggestedTrade}
          >
            Apply This Trade
          </button>
        </div>
      </div>
    );
  };
  
  if (!userTeam) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6 text-center">
        <h2 className="text-xl font-bold mb-4">Trade Dashboard</h2>
        <p className="text-gray-500">Please select your team to use the trade dashboard.</p>
      </div>
    );
  }
  
  return (
    <div className="bg-white rounded-lg shadow-md h-full flex flex-col">
      <div className="p-4 border-b">
        <h2 className="text-xl font-bold">Trade Dashboard</h2>
        <p className="text-sm text-gray-600">Propose and evaluate draft pick trades</p>
      </div>
      
      {/* Navigation tabs */}
      <div className="border-b">
        <nav className="flex">
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'propose' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('propose')}
          >
            Propose Trade
          </button>
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'suggest' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('suggest')}
          >
            Suggested Trades
          </button>
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'value' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('value')}
          >
            Value Chart
          </button>
        </nav>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4">
        {activeTab === 'propose' && (
          <>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Trade Partner</label>
              <select
                className="w-full p-2 border rounded"
                value={tradePartner ? tradePartner.id : ''}
                onChange={(e) => {
                  const selectedTeam = teams.find(t => t.id.toString() === e.target.value);
                  setTradePartner(selectedTeam);
                }}
              >
                <option value="">Select a team...</option>
                {teams
                  .filter(team => team.id !== userTeam.id)
                  .map(team => (
                    <option key={team.id} value={team.id}>
                      {team.name}
                    </option>
                  ))
                }
              </select>
            </div>
            
            {tradePartner && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <div className="flex items-center">
                    <div 
                      className="w-6 h-6 rounded-full mr-2 flex items-center justify-center"
                      style={{ 
                        backgroundColor: userTeam.colors.secondary,
                        borderColor: userTeam.colors.primary,
                        borderWidth: '2px'
                      }}
                    >
                      <span className="text-xs font-bold">{userTeam.abbreviation}</span>
                    </div>
                    <h3 className="text-lg font-medium">Your Picks</h3>
                  </div>
                  {userTeamPicks.length > 0 ? (
                    renderPickList(
                      userTeamPicks, 
                      userSelectedPicks, 
                      toggleUserPickSelection,
                      { primary: 'blue-600', secondary: 'blue-100' }
                    )
                  ) : (
                    <p className="text-sm text-gray-500 mt-2">No available picks</p>
                  )}
                </div>
                
                <div>
                  <div className="flex items-center">
                    <div 
                      className="w-6 h-6 rounded-full mr-2 flex items-center justify-center"
                      style={{ 
                        backgroundColor: tradePartner.colors.secondary,
                        borderColor: tradePartner.colors.primary,
                        borderWidth: '2px'
                      }}
                    >
                      <span className="text-xs font-bold">{tradePartner.abbreviation}</span>
                    </div>
                    <h3 className="text-lg font-medium">{tradePartner.name} Picks</h3>
                  </div>
                  {partnerTeamPicks.length > 0 ? (
                    renderPickList(
                      partnerTeamPicks, 
                      partnerSelectedPicks, 
                      togglePartnerPickSelection,
                      { primary: 'green-600', secondary: 'green-100' }
                    )
                  ) : (
                    <p className="text-sm text-gray-500 mt-2">No available picks</p>
                  )}
                </div>
              </div>
            )}
            
            {tradePartner && (
              <div className="mt-4">
                <button
                  className="w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
                  onClick={evaluateTrade}
                  disabled={userSelectedPicks.length === 0 || partnerSelectedPicks.length === 0}
                >
                  Evaluate Trade
                </button>
              </div>
            )}
            
            {tradeEvaluation && renderTradeEvaluation()}
          </>
        )}
        
        {activeTab === 'suggest' && (
          <>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Trade Partner</label>
              <select
                className="w-full p-2 border rounded"
                value={tradePartner ? tradePartner.id : ''}
                onChange={(e) => {
                  const selectedTeam = teams.find(t => t.id.toString() === e.target.value);
                  setTradePartner(selectedTeam);
                }}
              >
                <option value="">Select a team...</option>
                {teams
                  .filter(team => team.id !== userTeam.id)
                  .map(team => (
                    <option key={team.id} value={team.id}>
                      {team.name}
                    </option>
                  ))
                }
              </select>
            </div>
            
            {tradePartner && (
              <>
                <div className="mb-4">
                  <p className="text-sm">
                    Our algorithm analyzes draft pick values to suggest balanced trades 
                    with your selected partner.
                  </p>
                </div>
                
                {renderSuggestedTrade()}
              </>
            )}
          </>
        )}
        
        {activeTab === 'value' && (
          <div className="p-2">
            <h3 className="font-bold text-lg mb-3">Draft Pick Value Chart</h3>
            <p className="text-sm mb-4">
              Based on historical draft pick trade data. Values are approximate and may
              vary based on draft class strength and team needs.
            </p>
            
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="bg-gray-100">
                  <tr>
                    <th className="p-2">Pick</th>
                    <th className="p-2">Value</th>
                    <th className="p-2">Pick</th>
                    <th className="p-2">Value</th>
                    <th className="p-2">Pick</th>
                    <th className="p-2">Value</th>
                  </tr>
                </thead>
                <tbody>
                  {[...Array(32)].map((_, i) => (
                    <tr key={i} className="border-b">
                      <td className="p-2">{i+1}</td>
                      <td className="p-2 font-medium">{calculateTradeValue(i+1)}</td>
                      <td className="p-2">{i+33}</td>
                      <td className="p-2 font-medium">{calculateTradeValue(i+33)}</td>
                      <td className="p-2">{i+65}</td>
                      <td className="p-2 font-medium">{calculateTradeValue(i+65)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            <div className="mt-4 p-3 bg-gray-50 rounded border">
              <h4 className="font-medium mb-2">Notable Trade Examples</h4>
              <ul className="text-sm space-y-2">
                <li>Trading up from pick #15 to #5 typically costs an additional 1st round pick</li>
                <li>A high 2nd round pick is roughly equivalent to a late 1st rounder</li>
                <li>Trading back from early 1st to mid-1st can net an additional 2nd or 3rd round pick</li>
                <li>Top 5 picks hold significantly higher value than the rest of the 1st round</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TradeDashboard;