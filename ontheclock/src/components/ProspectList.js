import React, { useContext, useState } from 'react';
import { DraftContext } from '../context/DraftContext';

const ProspectList = () => {
  const { 
    prospects, 
    setSelectedProspect, 
    draftPlayer, 
    isUsersTurn, 
    currentTeam 
  } = useContext(DraftContext);
  
  const [search, setSearch] = useState('');
  const [positionFilter, setPositionFilter] = useState('All');
  const [sortBy, setSortBy] = useState('grade'); // Default sort by grade
  const [sortDirection, setSortDirection] = useState('desc'); // Default descending
  
  const positions = ['All', 'QB', 'RB', 'WR', 'TE', 'OT', 'OG', 'OL', 'EDGE', 'DT', 'DL', 'LB', 'CB', 'S'];
  
  // Filter prospects
  const filteredProspects = Array.isArray(prospects) ? prospects.filter(prospect => {
    const matchesSearch = prospect.name.toLowerCase().includes(search.toLowerCase()) || 
                         prospect.college.toLowerCase().includes(search.toLowerCase());
    
    const matchesPosition = positionFilter === 'All' || 
                         prospect.position === positionFilter ||
                         (positionFilter === 'OL' && ['OT', 'OG', 'C'].includes(prospect.position)) ||
                         (positionFilter === 'DL' && ['DT', 'DE'].includes(prospect.position));
    
    return matchesSearch && matchesPosition;
  }) : [];
  
  // Sort prospects
  const sortedProspects = [...filteredProspects].sort((a, b) => {
    if (sortBy === 'grade') {
      return sortDirection === 'desc' ? b.grade - a.grade : a.grade - b.grade;
    } else if (sortBy === 'name') {
      return sortDirection === 'desc' ? b.name.localeCompare(a.name) : a.name.localeCompare(b.name);
    } else if (sortBy === 'position') {
      return sortDirection === 'desc' ? b.position.localeCompare(a.position) : a.position.localeCompare(b.position);
    } else if (sortBy === 'college') {
      return sortDirection === 'desc' ? b.college.localeCompare(a.college) : a.college.localeCompare(b.college);
    }
    return 0;
  });
  
  // Handle sorting
  const handleSort = (column) => {
    if (sortBy === column) {
      // Toggle direction if clicking the same column
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // Set new column and default to descending (except for name)
      setSortBy(column);
      setSortDirection(column === 'name' ? 'asc' : 'desc');
    }
  };
  
  // Get sort icon
  const getSortIcon = (column) => {
    if (sortBy !== column) return '↕️';
    return sortDirection === 'asc' ? '↑' : '↓';
  };
  
  // Handle selecting a prospect
  const handleSelectProspect = (prospect) => {
    setSelectedProspect(prospect);
  };
  
  // Handle drafting a prospect
  const handleDraftPlayer = (prospect) => {
    if (isUsersTurn) {
      draftPlayer(prospect.id);
    }
  };
  
  // Calculate prospect need match for current team
  const getProspectNeedLevel = (prospect) => {
    if (!currentTeam || !currentTeam.needs) return 'low';
    
    const position = prospect.position;
    const positionGroup = {
      'QB': 'QB',
      'RB': 'RB',
      'WR': 'WR',
      'TE': 'TE',
      'OT': 'OL',
      'OG': 'OL',
      'C': 'OL',
      'OL': 'OL',
      'EDGE': 'EDGE',
      'DT': 'DL',
      'DE': 'EDGE',
      'DL': 'DL',
      'LB': 'LB',
      'CB': 'CB',
      'S': 'S'
    };
    
    const groupPosition = positionGroup[position] || position;
    
    if (currentTeam.needs[0] === groupPosition) return 'high';
    if (currentTeam.needs[1] === groupPosition) return 'medium';
    if (currentTeam.needs[2] === groupPosition) return 'medium';
    if (currentTeam.needs.includes(groupPosition)) return 'low';
    
    return 'low';
  };
  
  // Get grade color
  const getGradeColor = (grade) => {
    if (grade >= 9.0) return 'text-green-600 font-bold';
    if (grade >= 8.5) return 'text-green-500';
    if (grade >= 8.0) return 'text-blue-500';
    if (grade >= 7.5) return 'text-blue-400';
    return 'text-gray-600';
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md h-full p-4 overflow-hidden flex flex-col">
      <h2 className="text-xl font-bold mb-4">Draft Prospects</h2>
      
      <div className="mb-4 flex space-x-2">
        <input
          type="text"
          placeholder="Search prospects..."
          className="flex-1 px-4 py-2 border rounded"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        
        <select 
          className="px-4 py-2 border rounded bg-white"
          value={positionFilter}
          onChange={(e) => setPositionFilter(e.target.value)}
        >
          {positions.map(pos => (
            <option key={pos} value={pos}>{pos}</option>
          ))}
        </select>
      </div>
      
      <div className="overflow-y-auto flex-grow">
        <table className="min-w-full">
          <thead className="bg-gray-100 sticky top-0">
            <tr>
              <th 
                className="px-4 py-2 text-left cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('name')}
              >
                Name {getSortIcon('name')}
              </th>
              <th 
                className="px-4 py-2 text-center cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('position')}
              >
                Pos {getSortIcon('position')}
              </th>
              <th 
                className="px-4 py-2 text-left cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('college')}
              >
                College {getSortIcon('college')}
              </th>
              <th 
                className="px-4 py-2 text-center cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('grade')}
              >
                Grade {getSortIcon('grade')}
              </th>
            </tr>
          </thead>
          <tbody>
            {sortedProspects.map(prospect => {
              const needLevel = getProspectNeedLevel(prospect);
              const needClass = needLevel === 'high' ? 'bg-red-50' : 
                              needLevel === 'medium' ? 'bg-yellow-50' : '';
              
              return (
                <tr 
                  key={prospect.id} 
                  className={`border-b hover:bg-gray-50 cursor-pointer ${needClass}`}
                  onClick={() => handleSelectProspect(prospect)}
                >
                  <td className="px-4 py-2 font-medium">{prospect.name}</td>
                  <td className="px-4 py-2 text-center">
                    <span className="px-2 py-1 rounded-full text-xs bg-gray-100">
                      {prospect.position}
                    </span>
                  </td>
                  <td className="px-4 py-2">{prospect.college}</td>
                  <td className={`px-4 py-2 text-center ${getGradeColor(prospect.grade)}`}>
                    {prospect.grade.toFixed(1)}
                  </td>
                </tr>
              );
            })}
            
            {sortedProspects.length === 0 && (
              <tr>
                <td colSpan="4" className="px-4 py-2 text-center text-gray-500">
                  No prospects match your filters
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      
      {isUsersTurn && (
        <div className="mt-4 p-3 bg-gray-50 rounded-lg border">
          <div className="text-sm text-gray-700 mb-2">
            <span className="font-medium">{currentTeam?.name} Team Needs: </span>
            {currentTeam?.needs.map((need, index) => (
              <span key={index} className={`ml-1 px-2 py-1 rounded-full text-xs ${
                index === 0 ? 'bg-red-100 text-red-800' : 
                index <= 2 ? 'bg-yellow-100 text-yellow-800' : 
                'bg-gray-100 text-gray-800'
              }`}>
                {need}
              </span>
            ))}
          </div>
          
          <button
            className="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:bg-gray-400"
            disabled={!isUsersTurn}
            onClick={() => handleDraftPlayer(sortedProspects[0])}
          >
            {isUsersTurn ? 'Select Top Available Prospect' : 'Waiting for your turn...'}
          </button>
        </div>
      )}
    </div>
  );
};

export default ProspectList;