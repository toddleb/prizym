// src/prisma/index.ts

// Export all services for easy importing
export * from './userService';
export * from './assessmentService';

// Export types
export type { UserBasicInfo } from './userService';
export type { StudentProfileData, PrimaryType, SecondaryInfluence, SkillCategory, Skill } from '../components/StarsynCard';
