import React, { useContext, useState } from 'react';
import { DraftContext } from '../context/DraftContext';

const DraftHistory = () => {
  const { draftHistory, teams } = useContext(DraftContext);
  const [filterRound, setFilterRound] = useState('all');
  const [filterTeam, setFilterTeam] = useState('all');
  const [filterPosition, setFilterPosition] = useState('all');
  
  if (!draftHistory || draftHistory.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6 text-center">
        <h2 className="text-xl font-bold mb-4">Draft History</h2>
        <p className="text-gray-500">No picks have been made yet.</p>
      </div>
    );
  }
  
  // Get unique rounds, teams, and positions for filters
  const rounds = [...new Set(draftHistory.map(pick => pick.round))].sort((a, b) => a - b);
  const teamsList = [...new Set(draftHistory.map(pick => pick.team))].sort();
  const positions = [...new Set(draftHistory.map(pick => pick.prospect.position))].sort();
  
  // Apply filters
  const filteredHistory = draftHistory.filter(pick => {
    const matchesRound = filterRound === 'all' || pick.round === parseInt(filterRound);
    const matchesTeam = filterTeam === 'all' || pick.team === filterTeam;
    const matchesPosition = filterPosition === 'all' || pick.prospect.position === filterPosition;
    
    return matchesRound && matchesTeam && matchesPosition;
  });
  
  // Get team colors for styling
  const getTeamColors = (teamName) => {
    const team = teams.find(t => t.name === teamName);
    return team ? team.colors : { primary: '#000000', secondary: '#FFFFFF' };
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold mb-4">Draft History</h2>
      
      {/* Filters */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Round</label>
          <select
            className="w-full p-2 border rounded"
            value={filterRound}
            onChange={(e) => setFilterRound(e.target.value)}
          >
            <option value="all">All Rounds</option>
            {rounds.map(round => (
              <option key={round} value={round}>Round {round}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Team</label>
          <select
            className="w-full p-2 border rounded"
            value={filterTeam}
            onChange={(e) => setFilterTeam(e.target.value)}
          >
            <option value="all">All Teams</option>
            {teamsList.map(team => (
              <option key={team} value={team}>{team}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Position</label>
          <select
            className="w-full p-2 border rounded"
            value={filterPosition}
            onChange={(e) => setFilterPosition(e.target.value)}
          >
            <option value="all">All Positions</option>
            {positions.map(position => (
              <option key={position} value={position}>{position}</option>
            ))}
          </select>
        </div>
      </div>
      
      {/* History table */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Pick
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Team
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Player
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Position
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                College
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Grade
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredHistory.map((pick, index) => {
              const teamColors = getTeamColors(pick.team);
              
              return (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {pick.round}.{pick.pick}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div 
                        className="w-8 h-8 rounded-full mr-2 flex items-center justify-center"
                        style={{ 
                          backgroundColor: teamColors.secondary,
                          borderColor: teamColors.primary,
                          borderWidth: '2px'
                        }}
                      >
                        {/* Find team abbreviation based on team name */}
                        {(() => {
                          const team = teams.find(t => t.name === pick.team);
                          if (team) {
                            return (
                              <img 
                                src={`/assets/logos/${team.abbreviation.toLowerCase()}.png`}
                                alt={`${team.name} logo`}
                                className="w-6 h-6"
                                onError={(e) => {
                                  e.target.onerror = null;
                                  e.target.src = '/api/placeholder/32/32';
                                }}
                              />
                            );
                          } else {
                            return <span>{pick.team.substring(0, 3).toUpperCase()}</span>;
                          }
                        })()}
                      </div>
                      <div className="text-sm font-medium text-gray-900">
                        {pick.team}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">
                      {pick.prospect.name}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                      {pick.prospect.position}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-500">
                      {pick.prospect.college}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className={`text-sm font-medium ${
                      pick.prospect.grade >= 7.5 ? 'text-green-600' :
                      pick.prospect.grade >= 7.0 ? 'text-blue-600' :
                      pick.prospect.grade >= 6.5 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {pick.prospect.grade.toFixed(1)}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      
      {/* No results message */}
      {filteredHistory.length === 0 && (
        <div className="text-center py-4 text-gray-500">
          No draft picks match your filters.
        </div>
      )}
      
      {/* Summary */}
      <div className="mt-6 p-4 bg-gray-50 rounded">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Draft Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-3 rounded shadow">
            <div className="text-sm text-gray-500">Total Picks</div>
            <div className="text-xl font-bold">{draftHistory.length}</div>
          </div>
          <div className="bg-white p-3 rounded shadow">
            <div className="text-sm text-gray-500">Rounds Completed</div>
            <div className="text-xl font-bold">{Math.max(...draftHistory.map(p => p.round))}</div>
          </div>
          <div className="bg-white p-3 rounded shadow">
            <div className="text-sm text-gray-500">Teams Drafting</div>
            <div className="text-xl font-bold">{new Set(draftHistory.map(p => p.team)).size}</div>
          </div>
          <div className="bg-white p-3 rounded shadow">
            <div className="text-sm text-gray-500">Top Position</div>
            <div className="text-xl font-bold">
              {(() => {
                const posCount = {};
                draftHistory.forEach(p => {
                  posCount[p.prospect.position] = (posCount[p.prospect.position] || 0) + 1;
                });
                return Object.entries(posCount).sort((a, b) => b[1] - a[1])[0][0];
              })()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DraftHistory;