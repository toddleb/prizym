// pages/program/dashboard.tsx
import { useState } from 'react';
import { 
  Box, 
  Flex, 
  Heading, 
  Text, 
  SimpleGrid, 
  Tabs, 
  TabList, 
  Tab, 
  TabPanels, 
  TabPanel,
  IconButton,
  Button,
  Badge,
  HStack,
  Image,
  InputGroup,
  Input,
  InputRightElement,
  Menu,
  MenuButton,
  MenuList,
  MenuItem
} from '@chakra-ui/react';
import { 
  SettingsIcon, 
  SearchIcon,
  StarIcon, 
  TimeIcon, 
  ChevronDownIcon,
  ExternalLinkIcon
} from '@chakra-ui/icons';
import Layout from '@/components/Layout';
import ProgramStats from '@/components/program/ProgramStats';
import ProgramIntelligence from '@/components/program/ProgramIntelligence';
import CandidateSignals from '@/components/program/CandidateSignals';
import RelationshipPipeline from '@/components/program/RelationshipPipeline';
import ProgramForecasting from '@/components/program/ProgramForecasting';
import TopCandidates from '@/components/program/TopCandidates';
import CosmicSignature from '@/components/program/CosmicSignature';
import UpcomingActions from '@/components/program/UpcomingActions';

export default function ProgramDashboard() {
  const [periodFilter, setPeriodFilter] = useState('30d');
  const [activeTab, setActiveTab] = useState('intelligence');
  
  // Sample data - in a real app, this would come from your API
  const programData = {
    name: "Data Science Bootcamp",
    organization: "Tech Academy",
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

  return (
    <Layout role="program">
      {/* Header */}
      <Flex align="center" mb={6}>
        <Box>
          <Heading size="lg">🌠 Talent Intelligence Hub</Heading>
          <Flex align="center" mt={1}>
            <Text color="gray.600" fontSize="md">{programData.organization} • {programData.name}</Text>
            <Badge ml={2} colorScheme="green">{programData.campaignStatus}</Badge>
            <Text fontSize="xs" color="gray.500" ml={4}>
              <TimeIcon mr={1} />Last updated: {programData.lastUpdated}
            </Text>
          </Flex>
        </Box>
        <Box ml="auto">
          <InputGroup size="sm" width="260px" mr={3} display="inline-flex">
            <Input placeholder="Search candidates, programs, or schools..." />
            <InputRightElement>
              <SearchIcon color="gray.500" />
            </InputRightElement>
          </InputGroup>
          
          <Menu>
            <MenuButton as={Button} rightIcon={<ChevronDownIcon />} colorScheme="purple" size="sm" mr={2}>
              Actions
            </MenuButton>
            <MenuList>
              <MenuItem>Edit Cosmic Signature</MenuItem>
              <MenuItem>Create New Campaign</MenuItem>
              <MenuItem>Import Candidates</MenuItem>
              <MenuItem>Connect APIs</MenuItem>
            </MenuList>
          </Menu>
          
          <IconButton 
            aria-label="Settings" 
            icon={<SettingsIcon />} 
            variant="ghost" 
            size="sm" 
          />
        </Box>
      </Flex>

      {/* Key stats */}
      <ProgramStats 
        data={programData} 
        periodFilter={periodFilter} 
        setPeriodFilter={setPeriodFilter} 
      />
      
      {/* Main tabbed interface */}
      <Box mt={8}>
        <Tabs 
          variant="soft-rounded" 
          colorScheme="purple" 
          onChange={(index) => {
            const tabs = ['intelligence', 'signals', 'pipeline', 'forecasting'];
            setActiveTab(tabs[index]);
          }}
        >
          <TabList mb={4}>
            <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Program Intelligence</Tab>
            <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Candidate Signals</Tab>
            <Tab _selected={{ color: 'white', bg: 'purple.500' }}>Relationship Pipeline</Tab>
            <Tab _selected={{ color: 'white', bg: 'purple.500' }}>ROI + Forecasting</Tab>
          </TabList>
          
          <TabPanels>
            {/* Program Intelligence Hub */}
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
            
            {/* Candidate Signals Feed */}
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
                      <TopCandidates highMatchCount={programData.highMatchCount} />
                    </Box>
                  </SimpleGrid>
                </Box>
              </SimpleGrid>
            </TabPanel>
            
            {/* Relationship Pipeline */}
            <TabPanel px={0}>
              <RelationshipPipeline 
                matched={programData.matchCount}
                contacted={63}
                responded={46}
                applied={programData.applicationCount}
                accepted={programData.acceptedCount}
              />
            </TabPanel>
            
            {/* ROI + Forecasting */}
            <TabPanel px={0}>
              <ProgramForecasting />
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>
    </Layout>
  );
}