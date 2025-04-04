import { MatchData } from '../components/StarsynCard';

const matchData: MatchData = {
  studentName: "Alex Johnson",
  programName: "Data Science Bootcamp",
  overallMatch: 87,
  categories: [
    { 
      id: 'technical', 
      name: 'Technical Skills', 
      color: '#3B82F6', 
      factors: [
        { id: 't1', name: 'Python Proficiency', score: 95 },
        { id: 't2', name: 'Data Analysis', score: 90 },
        { id: 't3', name: 'Statistics', score: 85 },
        { id: 't4', name: 'Machine Learning', score: 78 },
        { id: 't5', name: 'Database Management', score: 88 }
      ]
    },
    { 
      id: 'learning', 
      name: 'Learning Style', 
      color: '#10B981', 
      factors: [
        { id: 'l1', name: 'Self-Directed', score: 92 },
        { id: 'l2', name: 'Project-Based', score: 96 },
        { id: 'l3', name: 'Collaborative', score: 75 },
        { id: 'l4', name: 'Visual Learning', score: 82 },
        { id: 'l5', name: 'Learning Pace', score: 89 }
      ]
    },
    { 
      id: 'experience', 
      name: 'Practical Experience', 
      color: '#F59E0B', 
      factors: [
        { id: 'e1', name: 'Projects', score: 78 },
        { id: 'e2', name: 'Industry Exposure', score: 68 },
        { id: 'e3', name: 'Problem Complexity', score: 85 },
        { id: 'e4', name: 'Team Collaboration', score: 80 },
        { id: 'e5', name: 'Tool Familiarity', score: 90 }
      ]
    },
    { 
      id: 'goals', 
      name: 'Career Goals', 
      color: '#8B5CF6', 
      factors: [
        { id: 'g1', name: 'Role Alignment', score: 95 },
        { id: 'g2', name: 'Industry Alignment', score: 92 },
        { id: 'g3', name: 'Timeline Fit', score: 90 },
        { id: 'g4', name: 'Salary Expectations', score: 88 },
        { id: 'g5', name: 'Growth Potential', score: 98 }
      ]
    },
    { 
      id: 'soft', 
      name: 'Soft Skills', 
      color: '#EC4899', 
      factors: [
        { id: 's1', name: 'Communication', score: 85 },
        { id: 's2', name: 'Problem Solving', score: 92 },
        { id: 's3', name: 'Adaptability', score: 88 },
        { id: 's4', name: 'Time Management', score: 75 },
        { id: 's5', name: 'Leadership', score: 78 }
      ]
    }
  ]
};

export default matchData;
