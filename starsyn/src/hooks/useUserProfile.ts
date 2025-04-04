// src/hooks/useUserProfile.ts

import { useState, useEffect } from 'react';
import { getUserProfileData } from '../prisma/assessmentService';
import type { StudentProfileData } from '../components/StarsynCard';

/**
 * Hook to fetch and manage user profile data
 * @param userId User ID to fetch profile data for
 * @param initialBlindMode Whether to start in blind mode
 * @returns Object containing user data and loading state
 */
export function useUserProfile(userId: string, initialBlindMode = true) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [profileData, setProfileData] = useState<StudentProfileData | null>(null);
  const [isBlindMode, setIsBlindMode] = useState(initialBlindMode);

  useEffect(() => {
    async function fetchData() {
      // Reset states when user ID changes
      setLoading(true);
      setError(null);
      setProfileData(null);
      
      // Don't fetch if no userId is provided
      if (!userId) {
        setLoading(false);
        return;
      }
      
      try {
        const data = await getUserProfileData(userId);
        setProfileData(data);
      } catch (err) {
        console.error('Error fetching user profile:', err);
        setError(err instanceof Error ? err : new Error('Unknown error'));
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [userId]);

  const toggleBlindMode = () => {
    setIsBlindMode(prev => !prev);
  };

  return {
    loading,
    error,
    profileData,
    isBlindMode,
    toggleBlindMode,
  };
}

export default useUserProfile;
