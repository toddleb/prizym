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
import MarketplaceHome from '../MarketplaceHome';

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
    <Box flex="1" p={6} overflowY="auto">
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

      <ProgramStats data={programData} periodFilter={periodFilter} setPeriodFilter={setPeriodFilter} />

      <Tabs variant="soft-rounded" colorScheme="purple" mt={8}>
        <TabList mb={4} flexWrap="wrap" gap={2}>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Marketplace</Tab>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Top Candidates</Tab>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Relationship Pipeline</Tab>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>ROI + Forecasting</Tab>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Upcoming Actions</Tab>
          <Tab _selected={{ color: 'white', bg: 'blue.500' }}>
            <Flex align="center">
              <FaBrain style={{ marginRight: '8px' }} />
              AI Insights
            </Flex>
          </Tab>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Program Intelligence</Tab>
          <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Candidate Signals</Tab>
        </TabList>

        <TabPanels>
          <TabPanel px={0}>
            <MarketplaceHome />
          </TabPanel>

          <TabPanel px={0}>
            <TopCandidates highMatchCount={programData.highQualityCount || 28} />
          </TabPanel>

          <TabPanel px={0}>
            <RelationshipPipeline
              matched={programData.matchCount}
              contacted={63}
              responded={46}
              applied={programData.applicationCount}
              accepted={programData.acceptedCount}
            />
          </TabPanel>

          <TabPanel px={0}>
            <ProgramForecasting />
          </TabPanel>

          <TabPanel px={0}>
            <UpcomingActions />
          </TabPanel>

          <TabPanel px={0}>
            <AIInsightsDashboard />
          </TabPanel>

          <TabPanel px={0}>
            <SimpleGrid columns={{ base: 1, xl: 3 }} spacing={6}>
              <ProgramIntelligence columns={2} gridColumn={{ base: "auto", xl: "span 2" }} />
              <Box>
                <SimpleGrid columns={1} spacing={6}>
                  <Box p={5} bg="white" borderRadius="lg" boxShadow="sm">
                    <Flex justify="space-between" align="center" mb={4}>
                      <Heading size="md">
                        <StarIcon mr={2} color="purple.500" />
                        Program Cosmic Signature
                      </Heading>
                      <Button size="xs" variant="outline" rightIcon={<ExternalLinkIcon />}>Edit</Button>
                    </Flex>
                    <CosmicSignature signatureStrength={programData.signatureStrength} />
                  </Box>
                </SimpleGrid>
              </Box>
            </SimpleGrid>
          </TabPanel>

          <TabPanel px={0}>
            <SimpleGrid columns={{ base: 1, xl: 3 }} spacing={6}>
              <CandidateSignals columns={2} gridColumn={{ base: "auto", xl: "span 2" }} />
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
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default DashboardTabs;
