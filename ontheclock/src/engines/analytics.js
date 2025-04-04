import React, { useState, useContext, useEffect } from 'react';
import { DraftContext } from '../context/DraftContext';

const DraftAnalytics = () => {
  const { teams, prospects, draftHistory } = useContext(DraftContext);
  
  const [activeTab, setActiveTab] = useState('position');
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [positionData, setPositionData] = useState(null);
  const [teamData, setTeamData] = useState(null);
  const [roundSuccess, setRoundSuccess] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // Calculate analytics when data changes
  useEffect(() => {
    if (teams && prospects && draftHistory) {
      generateAnalytics();
      setLoading(false);
    }
  }, [teams, prospects, draftHistory]);
  
  // Update team data when selected team changes
  useEffect(() => {
    if (selectedTeam) {
      generateTeamAnalytics(selectedTeam);
    }
  }, [selectedTeam, draftHistory]);
  
  // Generate all analytics data
  const generateAnalytics = () => {
    calculatePositionDistribution();
    calculateRoundSuccess();
    
    // Set a default team if none selected
    if (teams && teams.length > 0 && !selectedTeam) {
      setSelectedTeam(teams[0]);
    }
  };
  
  // Calculate position distribution from draft history
  const calculatePositionDistribution = () => {
    if (!draftHistory || draftHistory.length === 0) {
      // If no draft history yet, use mock data
      setPositionData(getMockPositionData());
      return;
    }
    
    // Count by position
    const positionCounts = {};
    const roundCounts = {};
    
    draftHistory.forEach(pick => {
      const position = pick.prospect.position;
      const round = pick.round;
      
      // Position totals
      positionCounts[position] = (positionCounts[position] || 0) + 1;
      
      // Position by round
      if (!roundCounts[round]) {
        roundCounts[round] = {};
      }
      
      roundCounts[round][position] = (roundCounts[round][position] || 0) + 1;
    });
    
    // Convert to arrays for charting
    const positionArray = Object.entries(positionCounts)
      .map(([position, count]) => ({ position, count }))
      .sort((a, b) => b.count - a.count);
    
    // Calculate position tiers by pick value
    const positionTiers = calculatePositionTiers();
    
    setPositionData({
      counts: positionArray,
      byRound: roundCounts,
      tiers: positionTiers
    });
  };
  
  // Calculate position tiers by value
  const calculatePositionTiers = () => {
    if (!draftHistory || draftHistory.length === 0) {
      return getMockPositionTiers();
    }
    
    const positionValues = {};
    
    draftHistory.forEach(pick => {
      const position = pick.prospect.position;
      const pickValue = getPickValue(pick.round, pick.pick);
      
      if (!positionValues[position]) {
        positionValues[position] = [];
      }
      
      positionValues[position].push(pickValue);
    });
    
    // Calculate average value by position
    const positionTiers = Object.entries(positionValues).map(([position, values]) => {
      const totalValue = values.reduce((sum, val) => sum + val, 0);
      const avgValue = totalValue / values.length;
      const pickCount = values.length;
      
      return { position, avgValue, pickCount };
    });
    
    return positionTiers.sort((a, b) => b.avgValue - a.avgValue);
  };
  
  // Calculate round success rates
  const calculateRoundSuccess = () => {
    // In a real implementation, this would calculate actual success metrics
    // For now, we'll use mocked success metrics
    setRoundSuccess([
      { round: 1, successRate: 0.67, allProRate: 0.21, starterRate: 0.78 },
      { round: 2, successRate: 0.58, allProRate: 0.12, starterRate: 0.65 },
      { round: 3, successRate: 0.42, allProRate: 0.07, starterRate: 0.52 },
      { round: 4, successRate: 0.33, allProRate: 0.05, starterRate: 0.39 },
      { round: 5, successRate: 0.25, allProRate: 0.03, starterRate: 0.29 },
      { round: 6, successRate: 0.17, allProRate: 0.02, starterRate: 0.20 },
      { round: 7, successRate: 0.08, allProRate: 0.01, starterRate: 0.12 }
    ]);
  };
  
  // Generate team-specific analytics
  const generateTeamAnalytics = (team) => {
    if (!team || !draftHistory) return;
    
    // Filter draft history for the selected team
    const teamPicks = draftHistory.filter(pick => pick.team === team.name);
    
    // Count positions drafted by this team
    const positionCounts = {};
    teamPicks.forEach(pick => {
      const position = pick.prospect.position;
      positionCounts[position] = (positionCounts[position] || 0) + 1;
    });
    
    // Position preferences (compared to league average)
    const leaguePositionCounts = {};
    draftHistory.forEach(pick => {
      const position = pick.prospect.position;
      leaguePositionCounts[position] = (leaguePositionCounts[position] || 0) + 1;
    });
    
    const positionPreferences = Object.entries(positionCounts).map(([position, count]) => {
      const teamPct = count / teamPicks.length;
      const leaguePct = (leaguePositionCounts[position] || 0) / draftHistory.length;
      const differential = teamPct - leaguePct;
      
      return {
        position,
        count,
        teamPct: teamPct.toFixed(2),
        leaguePct: leaguePct.toFixed(2),
        differential: differential.toFixed(2)
      };
    }).sort((a, b) => parseFloat(b.differential) - parseFloat(a.differential));
    
    // Draft approach - trade up/down tendencies
    // This would be calculated from actual trade data, but we'll mock it
    const tradeApproach = {
      tradesUp: Math.floor(Math.random() * 5) + 1,
      tradesDown: Math.floor(Math.random() * 5) + 2,
      netPicksGained: Math.floor(Math.random() * 6) - 2
    };
    
    // Historical pick success rates (mocked)
    const pickSuccess = {
      totalPicks: teamPicks.length,
      starters: Math.floor(teamPicks.length * 0.4),
      probowlers: Math.floor(teamPicks.length * 0.12),
      busts: Math.floor(teamPicks.length * 0.25)
    };
    
    setTeamData({
      picks: teamPicks,
      positionCounts,
      positionPreferences,
      tradeApproach,
      pickSuccess
    });
  };
  
  // Get draft pick value based on Jimmy Johnson chart (approximate)
  const getPickValue = (round, pick) => {
    const overallPick = (round - 1) * 32 + pick;
    
    if (overallPick <= 10) return 1000 + (11 - overallPick) * 200;
    if (overallPick <= 32) return 600 + (33 - overallPick) * 15;
    if (overallPick <= 64) return 300 + (65 - overallPick) * 5;
    if (overallPick <= 96) return 150 + (97 - overallPick) * 3;
    if (overallPick <= 128) return 50 + (129 - overallPick);
    return 50;
  };
  
  // Mock data when no real draft history exists
  const getMockPositionData = () => {
    return {
      counts: [
        { position: 'WR', count: 32 },
        { position: 'CB', count: 27 },
        { position: 'EDGE', count: 25 },
        { position: 'OT', count: 23 },
        { position: 'QB', count: 18 },
        { position: 'DT', count: 17 },
        { position: 'RB', count: 16 },
        { position: 'LB', count: 15 },
        { position: 'S', count: 14 },
        { position: 'TE', count: 12 },
        { position: 'OG', count: 11 },
        { position: 'C', count: 6 }
      ],
      byRound: {
        1: { 'QB': 5, 'OT': 5, 'WR': 4, 'EDGE': 4, 'CB': 4, 'DT': 3, 'TE': 2, 'LB': 2, 'S': 1, 'OG': 1, 'RB': 1 },
        2: { 'CB': 5, 'WR': 5, 'EDGE': 4, 'OT': 3, 'S': 3, 'RB': 3, 'DT': 2, 'TE': 2, 'LB': 2, 'OG': 2, 'QB': 1 },
        3: { 'WR': 6, 'CB': 5, 'RB': 3, 'OG': 3, 'EDGE': 3, 'LB': 3, 'S': 2, 'TE': 2, 'DT': 2, 'OT': 2, 'QB': 1 }
      }
    };
  };
  
  // Mock position tier data
  const getMockPositionTiers = () => {
    return [
      { position: 'QB', avgValue: 850, pickCount: 18 },
      { position: 'OT', avgValue: 720, pickCount: 23 },
      { position: 'EDGE', avgValue: 680, pickCount: 25 },
      { position: 'CB', avgValue: 620, pickCount: 27 },
      { position: 'WR', avgValue: 580, pickCount: 32 },
      { position: 'DT', avgValue: 550, pickCount: 17 },
      { position: 'TE', avgValue: 480, pickCount: 12 },
      { position: 'S', avgValue: 460, pickCount: 14 },
      { position: 'LB', avgValue: 440, pickCount: 15 },
      { position: 'RB', avgValue: 420, pickCount: 16 },
      { position: 'OG', avgValue: 400, pickCount: 11 },
      { position: 'C', avgValue: 380, pickCount: 6 }
    ];
  };
  
  // Render position distribution chart
  const renderPositionChart = () => {
    if (!positionData) return null;
    
    const maxCount = Math.max(...positionData.counts.map(item => item.count));
    
    return (
      <div className="mb-8">
        <h3 className="font-bold text-lg mb-4">Position Distribution</h3>
        <div className="relative h-64">
          {positionData.counts.map((item, index) => {
            const barHeight = (item.count / maxCount) * 100;
            return (
              <div key={item.position} className="absolute flex flex-col items-center" style={{
                left: `${index * (100 / positionData.counts.length)}%`,
                width: `${100 / positionData.counts.length}%`
              }}>
                <div className="w-full px-1">
                  <div 
                    className="bg-blue-500 hover:bg-blue-600 transition-all rounded-t"
                    style={{ height: `${barHeight}%` }}
                  ></div>
                </div>
                <div className="text-xs font-medium mt-1">{item.position}</div>
                <div className="text-xs text-gray-500">{item.count}</div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };
  
  // Render position value tiers
  const renderPositionTiers = () => {
    if (!positionData || !positionData.tiers) return null;
    
    return (
      <div className="mb-8">
        <h3 className="font-bold text-lg mb-4">Position Value Tiers</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">Position</th>
                <th className="px-4 py-2 text-center">Avg Draft Value</th>
                <th className="px-4 py-2 text-center">Picks</th>
                <th className="px-4 py-2 text-left">Value Tier</th>
              </tr>
            </thead>
            <tbody>
              {positionData.tiers.map((tier, idx) => (
                <tr key={tier.position} className="border-b">
                  <td className="px-4 py-2 font-medium">{tier.position}</td>
                  <td className="px-4 py-2 text-center">{Math.round(tier.avgValue)}</td>
                  <td className="px-4 py-2 text-center">{tier.pickCount}</td>
                  <td className="px-4 py-2">
                    <div className="flex items-center">
                      <div className={`w-3 h-3 rounded-full mr-2 ${
                        idx < 4 ? 'bg-green-500' : 
                        idx < 8 ? 'bg-blue-500' : 'bg-gray-500'
                      }`}></div>
                      <span>
                        {idx < 4 ? 'Premium' : idx < 8 ? 'Mid-Tier' : 'Value'}
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };
  
  // Render round success rates
  const renderRoundSuccess = () => {
    if (!roundSuccess) return null;
    
    return (
      <div className="mb-8">
        <h3 className="font-bold text-lg mb-4">Draft Success by Round</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-4 py-2 text-left">Round</th>
                <th className="px-4 py-2 text-center">Success Rate</th>
                <th className="px-4 py-2 text-center">Starter %</th>
                <th className="px-4 py-2 text-center">All-Pro %</th>
                <th className="px-4 py-2 text-left">Expectation</th>
              </tr>
            </thead>
            <tbody>
              {roundSuccess.map(round => (
                <tr key={round.round} className="border-b">
                  <td className="px-4 py-2 font-medium">Round {round.round}</td>
                  <td className="px-4 py-2 text-center">
                    <div className="flex items-center">
                      <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2">
                        <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${round.successRate * 100}%` }}></div>
                      </div>
                      <span>{(round.successRate * 100).toFixed(0)}%</span>
                    </div>
                  </td>
                  <td className="px-4 py-2 text-center">{(round.starterRate * 100).toFixed(0)}%</td>
                  <td className="px-4 py-2 text-center">{(round.allProRate * 100).toFixed(0)}%</td>
                  <td className="px-4 py-2">
                    {round.round <= 2 ? 'Immediate Impact' : 
                     round.round <= 4 ? 'Developmental Starter' : 'Depth/Special Teams'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };
  
  // Render team analytics
  const renderTeamAnalytics = () => {
    if (!teamData) return null;
    
    return (
      <div>
        <h3 className="font-bold text-lg mb-4">Team Draft Analysis: {selectedTeam?.name}</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="bg-white p-4 rounded shadow">
            <h4 className="text-sm font-medium text-gray-500 mb-1">Total Picks</h4>
            <div className="text-2xl font-bold">{teamData.pickSuccess.totalPicks}</div>
            <div className="mt-2 text-xs text-gray-600">
              <div className="flex justify-between mb-1">
                <span>Starter-quality players:</span>
                <span className="font-medium">{teamData.pickSuccess.starters} ({(teamData.pickSuccess.starters / teamData.pickSuccess.totalPicks * 100).toFixed(0)}%)</span>
              </div>
              <div className="flex justify-between mb-1">
                <span>Pro Bowl players:</span>
                <span className="font-medium">{teamData.pickSuccess.probowlers} ({(teamData.pickSuccess.probowlers / teamData.pickSuccess.totalPicks * 100).toFixed(0)}%)</span>
              </div>
              <div className="flex justify-between">
                <span>Draft busts:</span>
                <span className="font-medium">{teamData.pickSuccess.busts} ({(teamData.pickSuccess.busts / teamData.pickSuccess.totalPicks * 100).toFixed(0)}%)</span>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 rounded shadow">
            <h4 className="text-sm font-medium text-gray-500 mb-1">Draft Trading</h4>
            <div className="text-2xl font-bold">{teamData.tradeApproach.netPicksGained > 0 ? 'Trade Down' : 'Trade Up'}</div>
            <div className="mt-2 text-xs text-gray-600">
              <div className="flex justify-between mb-1">
                <span>Trades up:</span>
                <span className="font-medium">{teamData.tradeApproach.tradesUp}</span>
              </div>
              <div className="flex justify-between mb-1">
                <span>Trades down:</span>
                <span className="font-medium">{teamData.tradeApproach.tradesDown}</span>
              </div>
              <div className="flex justify-between">
                <span>Net picks gained:</span>
                <span className={`font-medium ${teamData.tradeApproach.netPicksGained > 0 ? 'text-green-600' : teamData.tradeApproach.netPicksGained < 0 ? 'text-red-600' : ''}`}>
                  {teamData.tradeApproach.netPicksGained > 0 ? '+' : ''}{teamData.tradeApproach.netPicksGained}
                </span>
              </div>
            </div>
          </div>
          
          <div className="bg-white p-4 rounded shadow">
            <h4 className="text-sm font-medium text-gray-500 mb-1">Position Strategy</h4>
            <div className="text-xl font-bold truncate">
              {teamData.positionPreferences[0]?.position}, {teamData.positionPreferences[1]?.position}
            </div>
            <div className="mt-2 text-xs text-gray-600">
              <div className="mb-1">Top position preferences vs. league avg:</div>
              {teamData.positionPreferences.slice(0, 3).map(pos => (
                <div key={pos.position} className="flex justify-between mb-1">
                  <span>{pos.position}:</span>
                  <span className={`font-medium ${parseFloat(pos.differential) > 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {parseFloat(pos.differential) > 0 ? '+' : ''}{pos.differential}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <h4 className="font-medium mb-2">Position Focus</h4>
        <div className="mb-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {Object.entries(teamData.positionCounts)
              .sort((a, b) => b[1] - a[1])
              .map(([position, count]) => (
                <div key={position} className="bg-gray-50 p-2 rounded border flex justify-between items-center">
                  <span className="font-medium">{position}</span>
                  <span className="text-sm bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">{count}</span>
                </div>
              ))
            }
          </div>
        </div>
        
        <h4 className="font-medium mb-2">Recent Draft Picks</h4>
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-2 py-2 text-left">Round</th>
                <th className="px-2 py-2 text-left">Player</th>
                <th className="px-2 py-2 text-center">Position</th>
                <th className="px-2 py-2 text-left">College</th>
              </tr>
            </thead>
            <tbody>
              {teamData.picks.slice(0, 8).map((pick, idx) => (
                <tr key={idx} className="border-b">
                  <td className="px-2 py-2">{pick.round}.{pick.pick}</td>
                  <td className="px-2 py-2 font-medium">{pick.prospect.name}</td>
                  <td className="px-2 py-2 text-center">
                    <span className="inline-block bg-gray-100 px-2 py-0.5 rounded-full text-xs">
                      {pick.prospect.position}
                    </span>
                  </td>
                  <td className="px-2 py-2 text-sm text-gray-600">{pick.prospect.college}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    );
  };
  
  // Render value distribution
  const renderValueDistribution = () => {
    return (
      <div className="mb-8">
        <h3 className="font-bold text-lg mb-4">Draft Pick Value Distribution</h3>
        <p className="text-sm text-gray-600 mb-4">
          Based on the Jimmy Johnson trade value chart used by NFL teams.
        </p>
        
        <div className="relative h-64 mb-6">
          {[...Array(32)].map((_, i) => {
            const pick = i + 1;
            const value = getPickValue(1, pick);
            const maxValue = getPickValue(1, 1);
            const height = (value / maxValue) * 100;
            
            return (
              <div key={i} className="absolute flex flex-col items-center" style={{
                left: `${i * (100 / 32)}%`,
                width: `${100 / 32}%`
              }}>
                <div className="w-full px-0.5">
                  <div 
                    className="bg-green-500 hover:bg-green-600 rounded-t"
                    style={{ height: `${height}%` }}
                  ></div>
                </div>
                {i % 4 === 0 && (
                  <div className="text-xs font-medium mt-1">{pick}</div>
                )}
              </div>
            );
          })}
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
          <div className="bg-white p-3 rounded shadow">
            <div className="text-sm text-gray-500">Pick #1</div>
            <div className="text-xl font-bold">3,000 pts</div>
          </div>
          <div className="bg-white p-3 rounded shadow">
            <div className="text-sm text-gray-500">Pick #10</div>
            <div className="text-xl font-bold">1,300 pts</div>
          </div>
          <div className="bg-white p-3 rounded shadow">
            <div className="text-sm text-gray-500">Pick #32</div>
            <div className="text-xl font-bold">590 pts</div>
          </div>
          <div className="bg-white p-3 rounded shadow">
            <div className="text-sm text-gray-500">Pick #64</div>
            <div className="text-xl font-bold">270 pts</div>
          </div>
        </div>
        
        <div className="bg-blue-50 p-4 rounded border border-blue-200">
          <h4 className="font-medium mb-2">Value Insights</h4>
          <ul className="text-sm space-y-1">
            <li>• The value difference between Pick #1 and #10 (1,700 pts) is greater than the entire 2nd round</li>
            <li>• Moving up 5 spots in the top 10 typically costs a 2nd round pick</li>
            <li>• A mid-1st round pick (#15-#20) is roughly worth two early 2nd round picks</li>
            <li>• Three 3rd round picks roughly equal one late 1st round pick</li>
          </ul>
        </div>
      </div>
    );
  };
  
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6 h-full flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <p className="mt-2">Loading analytics...</p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="bg-white rounded-lg shadow-md h-full flex flex-col">
      <div className="p-4 border-b">
        <h2 className="text-xl font-bold">Draft Analytics</h2>
        <p className="text-sm text-gray-600">Data-driven insights from the 2025 NFL Draft</p>
      </div>
      
      {/* Navigation tabs */}
      <div className="border-b">
        <nav className="flex">
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'position' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('position')}
          >
            Position Analysis
          </button>
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'value' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('value')}
          >
            Draft Value
          </button>
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'success' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('success')}
          >
            Success Rates
          </button>
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeTab === 'team' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('team')}
          >
            Team Analysis
          </button>
        </nav>
      </div>
      
      {/* Content area */}
      <div className="flex-1 overflow-y-auto p-4">
        {activeTab === 'position' && (
          <>
            {renderPositionChart()}
            {renderPositionTiers()}
            
            <div className="bg-gray-50 p-4 rounded border">
              <h4 className="font-medium mb-2">Position Insights</h4>
              <ul className="text-sm space-y-2">
                <li>• Wide receiver is the most frequently drafted position, accounting for ~13% of all picks</li>
                <li>• Quarterbacks have the highest average draft position value, typically selected in premium slots</li>
                <li>• Defensive backs (CB + S) make up nearly 20% of all draft selections</li>
                <li>• Running backs are being selected later in drafts compared to historical trends</li>
                <li>• Offensive tackles are the second most valuable position by draft capital spent</li>
              </ul>
            </div>
          </>
        )}
        
        {activeTab === 'value' && (
          <>
            {renderValueDistribution()}
          </>
        )}
        
        {activeTab === 'success' && (
          <>
            {renderRoundSuccess()}
            
            <div className="bg-gray-50 p-4 rounded border">
              <h4 className="font-medium mb-2">Success Rate Insights</h4>
              <ul className="text-sm space-y-2">
                <li>• 1st round picks have a 67% chance of becoming successful NFL players</li>
                <li>• All-Pro selections drop dramatically after the 2nd round</li>
                <li>• Late-round steals (Rounds 6-7) occur in only about 1 in 12 picks</li>
                <li>• Teams should expect starters from the first three rounds</li>
                <li>• Special teams contributions are the most likely positive outcome for Day 3 picks</li>
              </ul>
            </div>
          </>
        )}
        
        {activeTab === 'team' && (
          <>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Select Team</label>
              <select
                className="w-full p-2 border rounded"
                value={selectedTeam ? selectedTeam.id : ''}
                onChange={(e) => {
                  const team = teams.find(t => t.id.toString() === e.target.value);
                  setSelectedTeam(team);
                }}
              >
                {teams.map(team => (
                  <option key={team.id} value={team.id}>
                    {team.name}
                  </option>
                ))}
              </select>
            </div>
            
            {renderTeamAnalytics()}
          </>
        )}
      </div>
      
      <div className="p-3 border-t bg-gray-50 text-xs text-gray-500">
        Note: Analysis is based on current draft data and historical NFL trends.
      </div>
    </div>
  );
};

export default DraftAnalytics;