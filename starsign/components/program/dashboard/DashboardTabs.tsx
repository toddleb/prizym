// components/program/dashboard/DashboardTabs.tsx
import React, { useState } from 'react';
import {
  Box,
  Flex,
  Heading,
  Text,
  Badge,
  Button,
  HStack,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  VStack,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  SimpleGrid
} from '@chakra-ui/react';
import { StarIcon, TimeIcon, ExternalLinkIcon } from '@chakra-ui/icons';
import { FaBrain, FaFilter } from 'react-icons/fa';

// Import components
import ProgramStats from '../ProgramStats';
import AIInsightsDashboard from './AIInsightsDashboard';
import ProgramIntelligence from '../ProgramIntelligence';
import CandidateSignals from '../CandidateSignals';
import RelationshipPipeline from '../RelationshipPipeline';
import ProgramForecasting from '../ProgramForecasting';
import TopCandidates from '../TopCandidates';
import CosmicSignature from '../CosmicSignature';
import UpcomingActions from '../UpcomingActions';

interface DashboardTabsProps {
  programData: any;
  filteredCandidates: any[];
  periodFilter: string;
  setPeriodFilter: (period: string) => void;
  getDisplayTitle: () => string;
  selectedInstitution: any;
  selectedProgram: any;
}

const DashboardTabs: React.FC<DashboardTabsProps> = ({
  programData,
  filteredCandidates,
  periodFilter,
  setPeriodFilter,
  getDisplayTitle,
  selectedInstitution,
  selectedProgram
}) => {
  // Function to get color based on intent level
  const getIntentColor = (intent: string) => {
    switch (intent) {
      case 'very-high': return 'green';
      case 'high': return 'blue';
      case 'medium': return 'yellow';
      case 'low': return 'gray';
      default: return 'gray';
    }
  };

  return (
    <Box 
      flex="1" 
      p={6}
      overflowY="auto"
    >
      {/* Header with breadcrumb */}
      <Flex justify="space-between" align="center" mb={6}>
        <Heading size="lg">
          {getDisplayTitle()}
          {selectedInstitution && !selectedProgram && (
            <Badge ml={2} colorScheme="blue" fontSize="0.5em" verticalAlign="middle">
              {selectedInstitution.type}
            </Badge>
          )}
        </Heading>
        
        <HStack>
          <Badge colorScheme="green">{programData.campaignStatus}</Badge>
          <Text fontSize="sm" color="gray.500">
            <TimeIcon mr={1} />
            Last updated: {programData.lastUpdated}
          </Text>
        </HStack>
      </Flex>
      
      {/* Key Stats - Always visible at top */}
      <ProgramStats 
        data={programData} 
        periodFilter={periodFilter} 
        setPeriodFilter={setPeriodFilter} 
      />
      
      {/* Single row of tabs */}
      <Tabs 
        variant="soft-rounded" 
        colorScheme="purple"
        mt={8}
      >
        <TabList mb={4}>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Program Intelligence</Tab>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Candidate Signals</Tab>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Relationship Pipeline</Tab>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>ROI + Forecasting</Tab>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Top Candidates</Tab>
          <Tab _selected={{ color: 'white', bg: 'blue.500' }}>
            <Flex align="center">
              <FaBrain style={{ marginRight: '8px' }} />
              AI Insights
            </Flex>
          </Tab>
        </TabList>
        
        <TabPanels>
          {/* Program Intelligence Tab */}
          <TabPanel px={0}>
            <SimpleGrid columns={{ base: 1, xl: 3 }} spacing={6}>
              <ProgramIntelligence 
                columns={2} 
                gridColumn={{ base: "auto", xl: "span 2" }} 
              />
              <Box>
                <SimpleGrid columns={1} spacing={6}>
                  <Box p={5} bg="white" borderRadius="lg" boxShadow="sm">
                    <Flex justify="space-between" align="center" mb={4}>
                      <Heading size="md">
                        <StarIcon mr={2} color="purple.500" />
                        Program Cosmic Signature
                      </Heading>
                      <Button size="xs" variant="outline" rightIcon={<ExternalLinkIcon />}>
                        Edit
                      </Button>
                    </Flex>
                    <CosmicSignature signatureStrength={programData.signatureStrength} />
                  </Box>
                  
                  <Box p={5} bg="white" borderRadius="lg" boxShadow="sm">
                    <Flex justify="space-between" align="center" mb={4}>
                      <Heading size="md">Upcoming Actions</Heading>
                      <Button size="xs" variant="outline">View All</Button>
                    </Flex>
                    <UpcomingActions />
                  </Box>
                </SimpleGrid>
              </Box>
            </SimpleGrid>
          </TabPanel>
          
          {/* Candidate Signals Tab */}
          <TabPanel px={0}>
            <SimpleGrid columns={{ base: 1, xl: 3 }} spacing={6}>
              <CandidateSignals 
                columns={2} 
                gridColumn={{ base: "auto", xl: "span 2" }} 
              />
              <Box>
                <SimpleGrid columns={1} spacing={6}>
                  <Box p={5} bg="white" borderRadius="lg" boxShadow="sm">
                    <Flex justify="space-between" align="center" mb={4}>
                      <Heading size="md">Hot Talent</Heading>
                      <Button size="xs" variant="outline">View All</Button>
                    </Flex>
                    <TopCandidates highMatchCount={programData.highQualityCount || 28} />
                  </Box>
                </SimpleGrid>
              </Box>
            </SimpleGrid>
          </TabPanel>
          
          {/* Relationship Pipeline Tab */}
          <TabPanel px={0}>
            <RelationshipPipeline 
              matched={programData.matchCount}
              contacted={63}
              responded={46}
              applied={programData.applicationCount}
              accepted={programData.acceptedCount}
            />
          </TabPanel>
          
          {/* ROI + Forecasting Tab */}
          <TabPanel px={0}>
            <ProgramForecasting />
          </TabPanel>

          {/* Top Candidates Tab - Dedicated to the candidates table */}
          <TabPanel px={0}>
            <Box bg="white" borderRadius="lg" boxShadow="sm" p={5}>
              <Flex justify="space-between" align="center" mb={4}>
                <Heading size="md">
                  <StarIcon mr={2} color="blue.500" />
                  Top Matching Candidates
                </Heading>
                <HStack>
                  <Badge colorScheme="blue">{filteredCandidates.length} Results</Badge>
                  <Button size="xs" variant="outline" rightIcon={<FaFilter />}>
                    Filter
                  </Button>
                </HStack>
              </Flex>
              
              <Box overflowX="auto">
                <Table size="sm" variant="simple">
                  <Thead>
                    <Tr>
                      <Th>Candidate</Th>
                      <Th>Program</Th>
                      <Th>Skills</Th>
                      <Th isNumeric>Match</Th>
                      <Th>Intent</Th>
                      <Th>Last Activity</Th>
                      <Th></Th>
                    </Tr>
                  </Thead>
                  <Tbody>
                    {filteredCandidates.map(candidate => (
                      <Tr key={candidate.id}>
                        <Td>
                          {candidate.isRevealed ? (
                            <Text fontWeight="medium">{candidate.name}</Text>
                          ) : (
                            <HStack>
                              <Text>{candidate.blindId}</Text>
                              <Badge colorScheme="gray" variant="outline" size="sm">
                                Blind
                              </Badge>
                            </HStack>
                          )}
                        </Td>
                        <Td>
                          <VStack align="start" spacing={0}>
                            <Text fontSize="sm">{candidate.program}</Text>
                            <Text fontSize="xs" color="gray.500">{candidate.department}</Text>
                          </VStack>
                        </Td>
                        <Td>
                          <Flex gap={1} flexWrap="wrap">
                            {candidate.skills.map((skill, i) => (
                              <Badge key={i} colorScheme="blue" variant="subtle" fontSize="xs">
                                {skill}
                              </Badge>
                            ))}
                          </Flex>
                        </Td>
                        <Td isNumeric>
                          <Badge colorScheme="blue" variant="solid">
                            {candidate.matchScore}%
                          </Badge>
                        </Td>
                        <Td>
                          <Badge 
                            colorScheme={getIntentColor(candidate.intent)}
                          >
                            {candidate.intent.replace('-', ' ').replace(/^\w/, c => c.toUpperCase())}
                          </Badge>
                        </Td>
                        <Td fontSize="sm">{candidate.activity}</Td>
                        <Td>
                          <Button size="xs" colorScheme="blue">
                            Profile
                          </Button>
                        </Td>
                      </Tr>
                    ))}
                  </Tbody>
                </Table>
              </Box>
              
              <Button width="full" mt={4} size="sm" variant="outline">
                View All Candidates
              </Button>
            </Box>
          </TabPanel>
          
          {/* AI Insights Tab */}
          <TabPanel px={0}>
            <AIInsightsDashboard />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default DashboardTabs;