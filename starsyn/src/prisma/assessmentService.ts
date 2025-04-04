// src/prisma/assessmentService.ts

import { PrismaClient } from '@prisma/client';
import type { StudentProfileData, SkillCategory, Skill, SecondaryInfluence, PrimaryType } from '../components/StarsynCard';
import { logDatabaseError, formatDatabaseError } from '../utils/dbUtils';
import { getUserById } from './userService';

const prisma = new PrismaClient();

/**
 * Fetches a user profile with assessment data structured for the StarSynCard component
 * @param userId The user ID to fetch assessment data for
 * @returns Promise with formatted StudentProfileData
 */
export async function getUserProfileData(userId: string): Promise<StudentProfileData | null> {
  try {
    // Get the user with all their associated data
    const user = await getUserById(userId);
    
    if (!user || user.assessment_framework.length === 0) {
      return null;
    }

    // Get the most recent assessment framework
    const assessmentFramework = user.assessment_framework[0];

    // Get the primary type data
    const primaryTypeData = await getPrimaryTypeForUser(userId, user.user_tags);

    // Transform secondary assessment tier data to SecondaryInfluence format
    const secondaryInfluences: SecondaryInfluence[] = assessmentFramework.secondary_assessment_tier.map(tier => ({
      name: tier.name || 'Unknown',
      level: tier.level || 0,
      color: tier.color || '#808080',
      description: tier.description || '',
    }));

    // Transform tertiary assessment tier data to SkillCategory format
    const skillCategories: SkillCategory[] = assessmentFramework.tertiary_assessment_tier.map(tier => {
      // Map skills from profile_attributes
      const skills: Skill[] = tier.profile_attributes.map(attr => ({
        id: attr.id,
        name: attr.name || 'Unknown Skill',
        score: attr.score || 0,
      }));

      return {
        id: tier.id,
        name: tier.name || 'Unknown Category',
        color: tier.color || '#808080',
        description: tier.description || '',
        score: tier.score || 0,
        skills: skills,
      };
    });

    // Build the final StudentProfileData object
    const userProfile: StudentProfileData = {
      candidateId: userId,
      studentName: user.name,
      assessmentDetails: {
        date: assessmentFramework.date.toISOString().split('T')[0], // Format as YYYY-MM-DD
        version: assessmentFramework.version || '1.0',
        completionRate: assessmentFramework.completion_rate || 0,
        reliability: assessmentFramework.reliability || 'Medium',
        questionCount: assessmentFramework.question_count || 0,
      },
      primaryType: primaryTypeData,
      secondaryInfluences: secondaryInfluences,
      skillCategories: skillCategories,
    };

    return userProfile;
  } catch (error) {
    logDatabaseError('getUserProfileData', error);
    throw new Error(`Failed to get user profile: ${formatDatabaseError(error)}`);
  }
}

/**
 * Helper function to determine the primary type for a user
 * This implementation finds the primary type based on user tags
 */
async function getPrimaryTypeForUser(userId: string, userTags: any[] = []): Promise<PrimaryType> {
  try {
    // Look for a tag that indicates the primary type
    const primaryTypeTag = userTags.find(tag => 
      tag.tag.startsWith('primary_type:')
    );
    
    let primaryTypeId: string | null = null;
    
    // If we found a tag with the primary type, extract the ID
    if (primaryTypeTag) {
      primaryTypeId = primaryTypeTag.tag.split(':')[1];
    }
    
    // If we have a primary type ID, fetch that specific primary type
    let primaryTier = null;
    if (primaryTypeId) {
      primaryTier = await prisma.primary_assessment_tier.findUnique({
        where: { id: primaryTypeId }
      });
    }
    
    // If we don't have a specific primary type, get the first one as fallback
    if (!primaryTier) {
      primaryTier = await prisma.primary_assessment_tier.findFirst();
    }
    
    if (!primaryTier) {
      // Fallback if no primary tier found at all
      return {
        name: 'The Explorer',
        description: 'Curious and adaptable',
        color: '#3182CE', // Blue
        strengths: 'Adaptability, Curiosity, Quick learning',
        learningStyle: 'Hands-on experimentation and discovery',
        careerPaths: 'Research, Design, Entrepreneurship',
      };
    }

    return {
      name: primaryTier.name || 'The Explorer',
      description: primaryTier.description || 'Curious and adaptable',
      color: primaryTier.color || '#3182CE',
      strengths: primaryTier.strengths || 'Adaptability, Curiosity, Quick learning',
      learningStyle: primaryTier.learning_style || 'Hands-on experimentation and discovery',
      careerPaths: primaryTier.career_paths || 'Research, Design, Entrepreneurship',
    };
  } catch (error) {
    logDatabaseError('getPrimaryTypeForUser', error);
    // Return default primary type if there's an error
    return {
      name: 'The Explorer',
      description: 'Curious and adaptable',
      color: '#3182CE', // Blue
      strengths: 'Adaptability, Curiosity, Quick learning',
      learningStyle: 'Hands-on experimentation and discovery',
      careerPaths: 'Research, Design, Entrepreneurship',
    };
  }
}

/**
 * Fetches data for multiple users for comparison
 * @param userIds Array of user IDs to fetch and compare
 * @returns Array of user profile data
 */
export async function getMultipleUserProfiles(userIds: string[]): Promise<StudentProfileData[]> {
  const profiles: StudentProfileData[] = [];
  
  for (const userId of userIds) {
    try {
      const profile = await getUserProfileData(userId);
      if (profile) {
        profiles.push(profile);
      }
    } catch (error) {
      logDatabaseError(`getMultipleUserProfiles for user ${userId}`, error);
      // Skip this user if there's an error, but continue processing others
      console.warn(`Skipping profile for user ${userId}: ${formatDatabaseError(error)}`);
    }
  }
  
  return profiles;
}
