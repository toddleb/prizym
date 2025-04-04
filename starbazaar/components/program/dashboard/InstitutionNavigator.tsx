// components/program/dashboard/InstitutionNavigator.tsx
import React from 'react';
import {
  Box,
  VStack,
  Heading,
  Button,
  Text,
  Badge,
  Divider,
  HStack,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon
} from '@chakra-ui/react';
import { 
  FaUniversity, 
  FaBuilding, 
  FaCodeBranch, 
  FaBook,
  FaStar,
  FaUserFriends,
  FaRegCalendarAlt
} from 'react-icons/fa';

// Define prop interface
interface InstitutionNavigatorProps {
  institutionData: any[];
  selectedInstitution: any;
  selectedSchool: any;
  selectedDepartment: any;
  selectedProgram: any;
  handleInstitutionSelect: (institution: any) => void;
  handleSchoolSelect: (school: any) => void;
  handleDepartmentSelect: (department: any) => void;
  handleProgramSelect: (program: any) => void;
  filteredCandidates: any[];
  bgColor: string;
}

const InstitutionNavigator: React.FC<InstitutionNavigatorProps> = ({
  institutionData,
  selectedInstitution,
  selectedSchool,
  selectedDepartment,
  selectedProgram,
  handleInstitutionSelect,
  handleSchoolSelect,
  handleDepartmentSelect,
  handleProgramSelect,
  filteredCandidates,
  bgColor
}) => {
  return (
    <Box 
      width="280px" 
      bg={bgColor} 
      color="white" 
      p={4}
      overflowY="auto"
      boxShadow="md"
    >
      <VStack align="stretch" spacing={4}>
        <Heading size="sm" color="gray.300">Institution Navigator</Heading>
        
        <Accordion allowToggle defaultIndex={[0]} borderColor="transparent">
          {institutionData.map(institution => (
            <AccordionItem key={institution.id} border="none">
              <AccordionButton 
                py={2} 
                px={3} 
                _hover={{ bg: 'blue.900' }} 
                borderRadius="md"
                bg={selectedInstitution?.id === institution.id ? 'blue.800' : 'transparent'}
                fontWeight={selectedInstitution?.id === institution.id ? 'medium' : 'normal'}
                onClick={() => handleInstitutionSelect(institution)}
              >
                <Box flex="1" textAlign="left" fontSize="sm">
                  <FaUniversity style={{ display: 'inline', marginRight: '8px' }} />
                  {institution.name}
                </Box>
                <AccordionIcon />
              </AccordionButton>
              
              <AccordionPanel pb={4} pl={6}>
                {institution.schools.map(school => (
                  <Accordion key={school.id} allowToggle borderColor="transparent">
                    <AccordionItem border="none">
                      <AccordionButton 
                        py={2} 
                        _hover={{ bg: 'blue.900' }} 
                        borderRadius="md"
                        bg={selectedSchool?.id === school.id ? 'blue.800' : 'transparent'}
                        fontWeight={selectedSchool?.id === school.id ? 'medium' : 'normal'}
                        onClick={() => {
                          handleInstitutionSelect(institution);
                          handleSchoolSelect(school);
                        }}
                      >
                        <Box flex="1" textAlign="left" fontSize="sm">
                          <FaBuilding style={{ display: 'inline', marginRight: '8px' }} />
                          {school.name}
                        </Box>
                        <AccordionIcon />
                      </AccordionButton>
                      
                      <AccordionPanel pb={4} pl={5}>
                        {school.departments.map(dept => (
                          <Accordion key={dept.id} allowToggle borderColor="transparent">
                            <AccordionItem border="none">
                              <AccordionButton 
                                py={2} 
                                _hover={{ bg: 'blue.900' }} 
                                borderRadius="md"
                                bg={selectedDepartment?.id === dept.id ? 'blue.800' : 'transparent'}
                                fontWeight={selectedDepartment?.id === dept.id ? 'medium' : 'normal'}
                                onClick={() => {
                                  handleInstitutionSelect(institution);
                                  handleSchoolSelect(school);
                                  handleDepartmentSelect(dept);
                                }}
                              >
                                <Box flex="1" textAlign="left" fontSize="sm">
                                  <FaCodeBranch style={{ display: 'inline', marginRight: '8px' }} />
                                  {dept.name}
                                </Box>
                                <AccordionIcon />
                              </AccordionButton>
                              
                              <AccordionPanel pb={4} pl={4}>
                                <VStack align="stretch" spacing={1}>
                                  {dept.programs.map(program => (
                                    <Button 
                                      key={program.id} 
                                      variant="ghost" 
                                      justifyContent="flex-start" 
                                      size="sm"
                                      py={2}
                                      pl={4}
                                      rightIcon={<FaBook />}
                                      _hover={{ bg: 'blue.900' }}
                                      bg={selectedProgram?.id === program.id ? 'blue.800' : 'transparent'}
                                      fontWeight={selectedProgram?.id === program.id ? 'medium' : 'normal'}
                                      onClick={() => {
                                        handleInstitutionSelect(institution);
                                        handleSchoolSelect(school);
                                        handleDepartmentSelect(dept);
                                        handleProgramSelect(program);
                                      }}
                                      color="white"
                                    >
                                      {program.name}
                                    </Button>
                                  ))}
                                </VStack>
                              </AccordionPanel>
                            </AccordionItem>
                          </Accordion>
                        ))}
                      </AccordionPanel>
                    </AccordionItem>
                  </Accordion>
                ))}
              </AccordionPanel>
            </AccordionItem>
          ))}
        </Accordion>
      </VStack>
      
      <Divider my={6} borderColor="blue.800" />
      
      <VStack align="stretch" spacing={4}>
        <Heading size="sm" color="gray.300">Quick Links</Heading>
        
        <Button 
          leftIcon={<FaStar />} 
          justifyContent="flex-start" 
          bg="blue.800" 
          _hover={{ bg: 'blue.700' }} 
          color="white" 
          size="sm"
        >
          Top Matches
        </Button>
        
        <Button 
          leftIcon={<FaUserFriends />} 
          justifyContent="flex-start" 
          bg="blue.800" 
          _hover={{ bg: 'blue.700' }} 
          color="white" 
          size="sm"
        >
          All Candidates
        </Button>
        
        <Button 
          leftIcon={<FaRegCalendarAlt />} 
          justifyContent="flex-start" 
          bg="blue.800" 
          _hover={{ bg: 'blue.700' }} 
          color="white" 
          size="sm"
        >
          Upcoming Events
        </Button>
      </VStack>
      
      <Divider my={6} borderColor="blue.800" />
      
      <HStack spacing={2} justify="center">
        <Box>
          <Badge colorScheme="green" variant="solid" borderRadius="full">
            {filteredCandidates.length}
          </Badge>
        </Box>
        <Text fontSize="sm">Candidates in view</Text>
      </HStack>
    </Box>
  );
};

export default InstitutionNavigator;