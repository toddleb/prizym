// pages/program/dashboard.tsx
import { useState } from 'react';
import { Box, Flex, useColorModeValue } from '@chakra-ui/react';

// Import modular components
import DashboardTopBar from '@/components/program/dashboard/DashboardTopBar';
import InstitutionNavigator from '@/components/program/dashboard/InstitutionNavigator';
import InsightsSidebar from '@/components/program/dashboard/InsightsSidebar';
import DashboardTabs from '@/components/program/dashboard/DashboardTabs';

// Sample data - in a real app, this would come from your API
const programData = {
  name: "Northern Arizona University",
  department: "Computer Science",
  logo: "/api/placeholder/80/40",
  primaryColor: "#00205b",
  accentColor: "#F5BB2D",
  matchCount: 142,
  highMatchCount: 28,
  applicationCount: 17,
  acceptedCount: 5,
  matchRate: 87,
  responseRate: 73,
  signatureStrength: 92,
  campaignStatus: "active",
  lastUpdated: "2 days ago"
};

// Sample university structure data
const institutionData = [
  {
    id: "inst1",
    name: "Northern Arizona University",
    type: "4-Year Public University",
    location: "Flagstaff, AZ",
    schools: [
      {
        id: "sch1",
        name: "College of Engineering, Informatics, & Applied Sciences",
        departments: [
          {
            id: "dept1",
            name: "Computer Science",
            programs: [
              { id: "prog1", name: "B.S. Computer Science" },
              { id: "prog2", name: "B.S. Data Science" },
              { id: "prog3", name: "M.S. Computer Science" }
            ]
          },
          {
            id: "dept2",
            name: "Electrical Engineering",
            programs: [
              { id: "prog4", name: "B.S. Electrical Engineering" }
            ]
          }
        ]
      },
      {
        id: "sch2",
        name: "College of Business",
        departments: [
          {
            id: "dept3",
            name: "Information Systems",
            programs: [
              { id: "prog5", name: "B.S. Information Systems" },
              { id: "prog6", name: "M.S. Business Analytics" }
            ]
          }
        ]
      }
    ]
  },
  {
    id: "inst2",
    name: "Arizona State University",
    type: "4-Year Public University",
    location: "Tempe, AZ",
    schools: [
      {
        id: "sch3",
        name: "School of Computing",
        departments: [
          {
            id: "dept4",
            name: "Software Engineering",
            programs: [
              { id: "prog7", name: "B.S. Software Engineering" }
            ]
          }
        ]
      }
    ]
  }
];

// Sample candidate data
const candidateData = [
  {
    id: 'c145',
    blindId: 'Candidate #145',
    isRevealed: false,
    name: null,
    matchScore: 95,
    program: 'B.S. Data Science',
    department: 'Computer Science',
    school: 'College of Engineering, Informatics, & Applied Sciences',
    institution: 'Northern Arizona University',
    skills: ['Python', 'ML', 'Statistics'],
    intent: 'high',
    signalStrength: 4,
    activity: '3 hours ago'
  },
  {
    id: 'c092',
    blindId: 'Candidate #092',
    isRevealed: true,
    name: 'Taylor Kim',
    matchScore: 92,
    program: 'B.S. Computer Science',
    department: 'Computer Science',
    school: 'College of Engineering, Informatics, & Applied Sciences',
    institution: 'Northern Arizona University',
    skills: ['Python', 'ML/AI', 'Data Viz'],
    intent: 'very-high',
    signalStrength: 5,
    activity: '1 day ago'
  },
  // ... more candidates
];

// Sample insights data
const insightsData = [
  {
    title: "Match Rate",
    value: "87%",
    change: "+3.2%",
    trend: "up"
  },
  {
    title: "Response Rate",
    value: "64%",
    change: "+5.1%",
    trend: "up"
  },
  {
    title: "Conversion",
    value: "28%",
    change: "-1.4%",
    trend: "down"
  }
];

export default function ProgramDashboard() {
  // States for sharing between components
  const [periodFilter, setPeriodFilter] = useState('30d');
  const [selectedInstitution, setSelectedInstitution] = useState(null);
  const [selectedSchool, setSelectedSchool] = useState(null);
  const [selectedDepartment, setSelectedDepartment] = useState(null);
  const [selectedProgram, setSelectedProgram] = useState(null);
  const [isAiChatVisible, setIsAiChatVisible] = useState(false);
  
  // Color values
  const bgColor = useColorModeValue('gray.50', 'gray.800');
  const leftSidebarBg = '#00205b'; // Dark blue background
  
  // Filter candidates based on selected institution/school/department/program
  const getFilteredCandidates = () => {
    let filtered = [...candidateData];
    
    if (selectedInstitution) {
      filtered = filtered.filter(c => c.institution === selectedInstitution.name);
      
      if (selectedSchool) {
        filtered = filtered.filter(c => c.school === selectedSchool.name);
        
        if (selectedDepartment) {
          filtered = filtered.filter(c => c.department === selectedDepartment.name);
          
          if (selectedProgram) {
            filtered = filtered.filter(c => c.program === selectedProgram.name);
          }
        }
      }
    }
    
    // Sort by match score (highest first)
    return filtered.sort((a, b) => b.matchScore - a.matchScore);
  };

  const filteredCandidates = getFilteredCandidates();

  // Determine what to display in the breadcrumb/header
  const getDisplayTitle = () => {
    if (selectedProgram) {
      return selectedProgram.name;
    } else if (selectedDepartment) {
      return selectedDepartment.name;
    } else if (selectedSchool) {
      return selectedSchool.name;
    } else if (selectedInstitution) {
      return selectedInstitution.name;
    } else {
      return "All Programs";
    }
  };

  // Functions for institution navigation
  const handleInstitutionSelect = (institution) => {
    setSelectedInstitution(institution);
    setSelectedSchool(null);
    setSelectedDepartment(null);
    setSelectedProgram(null);
  };

  const handleSchoolSelect = (school) => {
    setSelectedSchool(school);
    setSelectedDepartment(null);
    setSelectedProgram(null);
  };

  const handleDepartmentSelect = (department) => {
    setSelectedDepartment(department);
    setSelectedProgram(null);
  };

  const handleProgramSelect = (program) => {
    setSelectedProgram(program);
  };

  return (
    <Flex height="100vh" direction="column" overflow="hidden" bg={bgColor}>
      {/* Top Navigation Bar */}
      <DashboardTopBar 
        programData={programData}
        isAiChatVisible={isAiChatVisible}
        setIsAiChatVisible={setIsAiChatVisible}
      />
      
      {/* Main Layout - Three Column */}
      <Flex flex="1" overflow="hidden">
        {/* Left Sidebar - Institution Navigator */}
        <InstitutionNavigator 
          institutionData={institutionData}
          selectedInstitution={selectedInstitution}
          selectedSchool={selectedSchool}
          selectedDepartment={selectedDepartment}
          selectedProgram={selectedProgram}
          handleInstitutionSelect={handleInstitutionSelect}
          handleSchoolSelect={handleSchoolSelect}
          handleDepartmentSelect={handleDepartmentSelect}
          handleProgramSelect={handleProgramSelect}
          filteredCandidates={filteredCandidates}
          bgColor={leftSidebarBg}
        />
        
        {/* Main Content Area with Tabs */}
        <DashboardTabs
          programData={programData}
          filteredCandidates={filteredCandidates}
          periodFilter={periodFilter}
          setPeriodFilter={setPeriodFilter}
          getDisplayTitle={getDisplayTitle}
          selectedInstitution={selectedInstitution}
          selectedProgram={selectedProgram}
        />
        
        {/* Right Sidebar - Analytics and Insights */}
        <InsightsSidebar
          programData={programData}
          insightsData={insightsData}
          isAiChatVisible={isAiChatVisible}
          setIsAiChatVisible={setIsAiChatVisible}
        />
      </Flex>
    </Flex>
  );
}