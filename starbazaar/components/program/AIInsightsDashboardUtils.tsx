// components/Program/AIInsightsDashboardUtils.tsx
import { ReactNode } from 'react';

// Types for AI Insights data structure
export interface InsightData {
  overview: {
    candidateCount: number;
    highQualityCount: number;
    averageMatchScore: number;
    matchScoreTrend: number;
    responseRateTrend: number;
    conversionRateTrend: number;
    topPrograms: ProgramMatch[];
  };
  trends: {
    candidateGrowth: number;
    engagementGrowth: number;
    skillTrends: SkillTrend[];
    institutionTrends: InstitutionTrend[];
  };
  recommendations: {
    programSuggestions: Recommendation[];
    outreachSuggestions: Recommendation[];
  };
  predictions: {
    candidateVolume: {
      nextQuarter: number;
      nextYear: number;
      growthRate: number;
    };
    skillGaps: SkillGap[];
    upcomingTrends: UpcomingTrend[];
  };
}

export interface ProgramMatch {
  name: string;
  candidateCount: number;
  matchQuality: number;
}

export interface SkillTrend {
  name: string;
  growth: number;
  prevalence: number;
}

export interface InstitutionTrend {
  name: string;
  growth: number;
  matchQuality: number;
}

export interface Recommendation {
  action: string;
  impact: 'high' | 'medium' | 'low';
  reasoning: string;
  difficulty: 'high' | 'medium' | 'low';
}

export interface SkillGap {
  skill: string;
  currentCoverage: number;
  futureImportance: number;
}

export interface UpcomingTrend {
  trend: string;
  confidence: number;
}

// Helper functions
export const getImpactColor = (impact: string): string => {
  switch (impact) {
    case 'high': return 'green';
    case 'medium': return 'blue';
    case 'low': return 'yellow';
    default: return 'gray';
  }
};

export const getDifficultyColor = (difficulty: string): string => {
  switch (difficulty) {
    case 'high': return 'red';
    case 'medium': return 'yellow';
    case 'low': return 'green';
    default: return 'gray';
  }
};

export const getMatchQualityColorScheme = (quality: number): string => {
  if (quality >= 85) return "green";
  if (quality >= 75) return "blue";
  return "yellow";
};

// Sample data for development and testing
export const getSampleInsightsData = (): InsightData => {
  return {
    overview: {
      candidateCount: 142,
      highQualityCount: 28,
      averageMatchScore: 78.4,
      matchScoreTrend: 3.2,
      responseRateTrend: 5.5,
      conversionRateTrend: -1.2,
      topPrograms: [
        { name: 'B.S. Computer Science', candidateCount: 45, matchQuality: 82 },
        { name: 'B.S. Data Science', candidateCount: 38, matchQuality: 89 },
        { name: 'M.S. Computer Science', candidateCount: 22, matchQuality: 76 },
        { name: 'B.S. Information Systems', candidateCount: 16, matchQuality: 70 },
        { name: 'M.S. Business Analytics', candidateCount: 12, matchQuality: 80 }
      ],
    },
    trends: {
      candidateGrowth: 14.5,
      engagementGrowth: 8.2,
      skillTrends: [
        { name: 'Machine Learning', growth: 18.5, prevalence: 68 },
        { name: 'Python', growth: 12.3, prevalence: 82 },
        { name: 'Data Visualization', growth: 15.7, prevalence: 60 },
        { name: 'Cloud Computing', growth: 24.8, prevalence: 42 },
        { name: 'Deep Learning', growth: 32.1, prevalence: 35 }
      ],
      institutionTrends: [
        { name: 'Northern Arizona University', growth: 15.2, matchQuality: 88 },
        { name: 'Arizona State University', growth: 8.5, matchQuality: 75 },
        { name: 'University of Arizona', growth: 5.2, matchQuality: 72 }
      ]
    },
    recommendations: {
      programSuggestions: [
        { 
          action: 'Create specialized AI track', 
          impact: 'high', 
          reasoning: 'Growing demand in candidate skill profiles shows 32% increase in AI-related interests',
          difficulty: 'medium'
        },
        { 
          action: 'Develop cloud computing partnerships', 
          impact: 'medium', 
          reasoning: 'Cloud skills growing 24.8% with limited program coverage',
          difficulty: 'high'
        },
        { 
          action: 'Add data visualization workshop', 
          impact: 'medium', 
          reasoning: '60% of high-matching candidates show interest in visualization skills',
          difficulty: 'low'
        }
      ],
      outreachSuggestions: [
        { 
          action: 'Target Computer Science juniors at NAU', 
          impact: 'high', 
          reasoning: '88% match quality with 15.2% growth in qualified candidates',
          difficulty: 'low'
        },
        { 
          action: 'Host virtual ML competition', 
          impact: 'medium', 
          reasoning: 'High engagement rates among ML-interested candidates',
          difficulty: 'medium'
        },
        { 
          action: 'Develop early connection with sophomore students', 
          impact: 'high', 
          reasoning: 'Data shows 45% higher conversion when relationships start early',
          difficulty: 'medium'
        }
      ]
    },
    predictions: {
      candidateVolume: {
        nextQuarter: 165,
        nextYear: 210,
        growthRate: 12.5
      },
      skillGaps: [
        { skill: 'Neural Networks', currentCoverage: 35, futureImportance: 70 },
        { skill: 'MLOps', currentCoverage: 25, futureImportance: 65 },
        { skill: 'Data Ethics', currentCoverage: 40, futureImportance: 75 }
      ],
      upcomingTrends: [
        { trend: 'Specialized AI certifications', confidence: 85 },
        { trend: 'Cloud-native development focus', confidence: 80 },
        { trend: 'Cross-disciplinary data science', confidence: 75 }
      ]
    }
  };
};

// Function to format dates consistently
export const formatDate = (date: Date): string => {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  }).format(date);
};

// Function to format time
export const formatTime = (date: Date): string => {
  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: true
  }).format(date);
};

// Function to calculate percentage change
export const calculatePercentChange = (current: number, previous: number): number => {
  if (previous === 0) return 0;
  return parseFloat(((current - previous) / previous * 100).toFixed(1));
};

// Helper to get readable time ranges
export const getTimeRangeLabel = (range: string): string => {
  switch (range) {
    case '7d': return 'Last 7 Days';
    case '30d': return 'Last 30 Days';
    case '90d': return 'Last 90 Days';
    case '1y': return 'Last Year';
    case 'all': return 'All Time';
    default: return 'Custom Range';
  }
};