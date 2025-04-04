// src/App.tsx
import { useState, useEffect } from 'react';
import StarSynCard from './components/StarsynCard';
import useUserProfile from './hooks/useUserProfile';
import { getAllUsers, getUsersWithAssessments, UserBasicInfo } from './prisma/userService';

function App() {
  const [users, setUsers] = useState<UserBasicInfo[]>([]);
  const [userId, setUserId] = useState<string>('');
  const [usersLoading, setUsersLoading] = useState(true);
  const [userTypeFilter, setUserTypeFilter] = useState<string>('STUDENT');
  const [searchQuery, setSearchQuery] = useState<string>('');
  
  const { 
    loading: profileLoading, 
    error: profileError, 
    profileData, 
    isBlindMode,
    toggleBlindMode 
  } = useUserProfile(userId, true);

  // Load the list of users on component mount or when filters change
  useEffect(() => {
    async function loadUsers() {
      try {
        setUsersLoading(true);
        // Get users with assessments and the specified user type
        const usersWithAssessments = await getUsersWithAssessments(userTypeFilter);
        setUsers(usersWithAssessments);
        
        // Set the first user as default if we have any
        if (usersWithAssessments.length > 0 && !userId) {
          setUserId(usersWithAssessments[0].id);
        } else if (usersWithAssessments.length > 0) {
          // Check if current userId is still in the list
          if (!usersWithAssessments.some(user => user.id === userId)) {
            setUserId(usersWithAssessments[0].id);
          }
        } else if (userId) {
          // Clear userId if no users are available
          setUserId('');
        }
      } catch (error) {
        console.error('Error loading users:', error);
      } finally {
        setUsersLoading(false);
      }
    }
    
    loadUsers();
  }, [userTypeFilter]);

  // Handle user selection change
  const handleUserChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setUserId(e.target.value);
  };
  
  // Handle user type filter change
  const handleUserTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setUserTypeFilter(e.target.value);
  };

  const isLoading = usersLoading || (userId && profileLoading);

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6 bg-white p-4 rounded shadow-sm">
          <h1 className="text-2xl font-bold mb-4">Starsyn Profile Viewer</h1>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label htmlFor="userTypeSelect" className="block text-sm font-medium text-gray-700 mb-1">
                User Type:
              </label>
              <select
                id="userTypeSelect"
                value={userTypeFilter}
                onChange={handleUserTypeChange}
                className="border border-gray-300 rounded-md px-3 py-2 w-full"
                disabled={usersLoading}
              >
                <option value="STUDENT">Students</option>
                <option value="AGENCY">Agencies</option>
                <option value="PROGRAM">Programs</option>
                <option value="MILITARY">Military</option>
                <option value="">All Types</option>
              </select>
            </div>
            
            <div>
              <label htmlFor="userSelect" className="block text-sm font-medium text-gray-700 mb-1">
                Select User:
              </label>
              {usersLoading ? (
                <div className="text-sm text-gray-500">Loading users...</div>
              ) : users.length === 0 ? (
                <div className="text-sm text-red-500">No users with completed assessments found</div>
              ) : (
                <select
                  id="userSelect"
                  value={userId}
                  onChange={handleUserChange}
                  className="border border-gray-300 rounded-md px-3 py-2 w-full"
                  disabled={usersLoading}
                >
                  {users.map((user) => (
                    <option key={user.id} value={user.id}>
                      {`${user.name}${user.program ? ` - ${user.program}` : ''}`}
                    </option>
                  ))}
                </select>
              )}
            </div>
          </div>
          
          <button 
            onClick={toggleBlindMode}
            className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition disabled:bg-purple-300 disabled:cursor-not-allowed"
            disabled={!userId || isLoading}
          >
            {isBlindMode ? 'Show Full Profile' : 'Switch to Blind Mode'}
          </button>
        </div>

        {isLoading ? (
          <div className="flex justify-center items-center h-64 bg-white rounded shadow">
            <div className="text-xl text-gray-500">Loading profile data...</div>
          </div>
        ) : profileError ? (
          <div className="bg-red-50 p-4 rounded border border-red-200 text-red-700">
            <h2 className="text-lg font-bold mb-2">Error Loading Profile</h2>
            <p>{profileError.message}</p>
          </div>
        ) : profileData ? (
          <StarSynCard
            studentData={profileData}
            initialBlindMode={isBlindMode}
            onConnect={() => console.log('Connected to user:', profileData.candidateId)}
          />
        ) : userId ? (
          <div className="bg-yellow-50 p-4 rounded border border-yellow-200 text-yellow-700">
            <h2 className="text-lg font-bold mb-2">No Profile Data</h2>
            <p>No profile data found for this user. They may need to complete an assessment.</p>
          </div>
        ) : (
          <div className="bg-blue-50 p-4 rounded border border-blue-200 text-blue-700">
            <h2 className="text-lg font-bold mb-2">Select a User</h2>
            <p>Please select a user to view their profile.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
