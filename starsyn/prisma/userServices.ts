// src/prisma/userService.ts

import { PrismaClient } from '@prisma/client';
import { logDatabaseError, formatDatabaseError } from '../utils/dbUtils';

const prisma = new PrismaClient();

/**
 * UserBasicInfo interface represents the minimal information needed 
 * to display a user in a selection list
 */
export interface UserBasicInfo {
  id: string;
  name: string;
  email?: string | null;
  userType: string;
  program?: string;
  assessmentComplete: boolean;
  tags: string[];
}

/**
 * Get a list of all users with basic info
 * @param userType Optional user type filter (e.g., 'STUDENT')
 * @returns Promise with array of user basic info
 */
export async function getAllUsers(userType?: string): Promise<UserBasicInfo[]> {
  try {
    // Build the where clause
    const where = userType ? { user_type: userType } : {};
    
    // Get users with their org affiliations, tags, and assessment data
    const users = await prisma.users.findMany({
      where,
      include: {
        user_org_affiliations: {
          include: {
            organizations: true
          }
        },
        user_tags: true,
        assessment_framework: {
          orderBy: {
            date: 'desc'
          },
          take: 1
        }
      }
    });

    // Transform to UserBasicInfo format
    return users.map(user => {
      // Get program info from organization affiliation if available
      const programOrg = user.user_org_affiliations.find(
        affiliation => affiliation.organizations?.type === 'PROGRAM'
      );
      
      const programName = programOrg?.organizations?.name || undefined;

      return {
        id: user.id,
        name: user.name,
        email: user.email,
        userType: user.user_type || 'UNKNOWN',
        program: programName,
        assessmentComplete: user.assessment_framework.length > 0,
        tags: user.user_tags.map(tag => tag.tag)
      };
    });
  } catch (error) {
    logDatabaseError('getAllUsers', error);
    throw new Error(formatDatabaseError(error));
  }
}

/**
 * Get users with completed assessments
 * @param userType Optional user type filter
 * @returns Promise with array of users who have completed assessments
 */
export async function getUsersWithAssessments(userType?: string): Promise<UserBasicInfo[]> {
  try {
    const allUsers = await getAllUsers(userType);
    return allUsers.filter(user => user.assessmentComplete);
  } catch (error) {
    logDatabaseError('getUsersWithAssessments', error);
    throw new Error(`Failed to get users with assessments: ${formatDatabaseError(error)}`);
  }
}

/**
 * Search for users by name, email, or program
 * @param searchTerm Search string to filter users
 * @param userType Optional user type filter
 * @returns Filtered list of users
 */
export async function searchUsers(searchTerm: string, userType?: string): Promise<UserBasicInfo[]> {
  try {
    const allUsers = await getAllUsers(userType);
    
    if (!searchTerm) {
      return allUsers;
    }
    
    const lowerSearchTerm = searchTerm.toLowerCase();
    
    return allUsers.filter(user => 
      user.name.toLowerCase().includes(lowerSearchTerm) || 
      (user.email && user.email.toLowerCase().includes(lowerSearchTerm)) ||
      (user.program && user.program.toLowerCase().includes(lowerSearchTerm))
    );
  } catch (error) {
    logDatabaseError('searchUsers', error);
    throw new Error(`Search failed: ${formatDatabaseError(error)}`);
  }
}

/**
 * Get a user by ID with full details
 * @param userId The user ID to fetch
 * @returns User with all related data
 */
export async function getUserById(userId: string) {
  try {
    return await prisma.users.findUnique({
      where: { id: userId },
      include: {
        user_tags: true,
        user_segments: true,
        user_org_affiliations: {
          include: { organizations: true },
        },
        user_permissions: true,
        user_role_history: true,
        assessment_framework: {
          orderBy: { date: 'desc' },
          take: 1,
          include: {
            secondary_assessment_tier: true,
            tertiary_assessment_tier: {
              include: {
                profile_attributes: true
              }
            }
          }
        },
        gamification_state: true
      },
    });
  } catch (error) {
    logDatabaseError('getUserById', error);
    throw new Error(`Failed to get user: ${formatDatabaseError(error)}`);
  }
}
