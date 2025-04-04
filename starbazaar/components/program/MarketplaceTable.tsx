import React, { useState, useEffect } from 'react';
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Text,
  Badge,
  VStack,
  HStack,
  Flex,
  Select,
  Input,
  Spacer,
  Button,
  ButtonGroup,
  Spinner,
  useToast,
} from '@chakra-ui/react';
import { starsynColors } from '../../theme/starsynColors';

const influenceColorMap = {
  Visionary: 'purple',
  Pragmatist: 'orange',
  Empath: 'pink',
  Scholar: 'blue',
  Artisan: 'yellow',
};

const futureGoalColorMap = {
  Degree: 'blue',
  Course: 'blue',
  Bootcamp: 'purple',
  Job: 'green',
  Internship: 'green',
  Undecided: 'gray',
  'Gap Year': 'gray',
};

const MiniStarsignBadge = ({ color }: { color: string }) => (
  <Box width="30px" height="30px" borderRadius="full" bg={color} borderWidth="2px" borderColor="white" boxShadow="sm" />
);

const MarketplaceTable = () => {
  const toast = useToast();
  const [candidates, setCandidates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedPrimary, setSelectedPrimary] = useState('');
  const [selectedIntent, setSelectedIntent] = useState('');
  const [skillSearch, setSkillSearch] = useState('');
  const [viewMode, setViewMode] = useState<'table' | 'card'>('table');
  const [sortKey, setSortKey] = useState<'matchScore' | 'lastActivity'>('matchScore');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch('/api/candidates');
        const json = await res.json();
        console.log('✅ Loaded candidates:', json.candidates);
        setCandidates(json.candidates || []);
      } catch (err) {
        toast({ title: 'Error loading candidates', status: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [toast]);

  const filtered = candidates
    .filter(c => {
      const matchesPrimary = selectedPrimary ? c.primaryView === selectedPrimary : true;
      const matchesIntent = selectedIntent ? c.intent === selectedIntent : true;
      const matchesSkills = skillSearch
        ? c.skills?.some((s: string) => s.toLowerCase().includes(skillSearch.toLowerCase()))
        : true;
      return matchesPrimary && matchesIntent && matchesSkills;
    })
    .sort((a, b) => (sortKey === 'matchScore' ? b.matchScore - a.matchScore : a.lastActivity.localeCompare(b.lastActivity)));

  const starsynCounts = filtered.reduce<Record<string, number>>((acc, curr) => {
    acc[curr.primaryView] = (acc[curr.primaryView] || 0) + 1;
    return acc;
  }, {});

  return (
    <Box>
      <Flex gap={4} mb={4} align="center" wrap="wrap" bg="white" p={4} borderRadius="lg" boxShadow="sm">
        <Select placeholder="Filter by Starsyn" width="200px" onChange={e => setSelectedPrimary(e.target.value)}>
          {Object.keys(starsynColors.mainTypes).map((type, idx) => (
            <option key={idx} value={type}>{type}</option>
          ))}
        </Select>
        <Select placeholder="Filter by Intent" width="160px" onChange={e => setSelectedIntent(e.target.value)}>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </Select>
        <Input placeholder="Search skills..." width="200px" value={skillSearch} onChange={e => setSkillSearch(e.target.value)} />
        <Select width="160px" value={sortKey} onChange={e => setSortKey(e.target.value as any)}>
          <option value="matchScore">Sort by Match</option>
          <option value="lastActivity">Sort by Activity</option>
        </Select>
        <Spacer />
        <ButtonGroup size="sm" isAttached variant="outline">
          <Button onClick={() => setViewMode('table')} isActive={viewMode === 'table'}>Table</Button>
          <Button onClick={() => setViewMode('card')} isActive={viewMode === 'card'}>Card</Button>
        </ButtonGroup>
      </Flex>

      <Box mb={4} px={4}>
        <Text fontSize="md" fontWeight="semibold">Showing {filtered.length} candidates</Text>
        <HStack spacing={3} mt={2} flexWrap="wrap">
          {Object.entries(starsynCounts).map(([type, count]) => (
            <Badge
              key={type}
              bg={starsynColors.mainTypes[type]?.border ?? 'gray.400'}
              color="white"
              fontSize="xs"
              px={2}
              py={1}
              borderRadius="md"
            >
              {type}: {count}
            </Badge>
          ))}
        </HStack>
      </Box>

      {loading ? (
        <Flex justify="center" align="center" py={10}>
          <Spinner size="lg" />
        </Flex>
      ) : (
        <Box bg="white" borderRadius="lg" boxShadow="xs" overflowX="auto">
          <Table size="sm">
            <Thead>
              <Tr>
                <Th>Candidate</Th>
                <Th>Skills</Th>
                <Th>Match</Th>
                <Th>Intent</Th>
                <Th>Activity</Th>
                <Th>Future Goals</Th>
                <Th>Signature</Th>
              </Tr>
            </Thead>
            <Tbody>
              {filtered.map(candidate => {
                const colors = starsynColors.mainTypes[candidate.primaryView] || {
                  border: '#CBD5E0',
                  text: '#2D3748',
                  bg: '#FFFFFF'
                };
                return (
                  <Tr key={candidate.id}>
                    <Td>
                      <Text fontWeight="medium" color={colors.text}>
                        {candidate.isRevealed ? candidate.name : candidate.blindId}
                      </Text>
                      <HStack spacing={1} mt={1}>
                        <Badge
                          bg={colors.border}
                          color="white"
                          fontWeight="bold"
                          fontSize="xs"
                          px={2}
                          py={0.5}
                          borderRadius="md"
                        >
                          {candidate.primaryView}
                        </Badge>
                        {candidate.secondaryInfluences?.map((inf: string, idx: number) => (
                          <Badge key={idx} colorScheme={influenceColorMap[inf] || 'gray'} variant="subtle" fontSize="xs">
                            {inf}
                          </Badge>
                        ))}
                      </HStack>
                    </Td>
                    <Td>
                      <Flex gap={1} wrap="wrap">
                        {candidate.skills?.map((skill: string, i: number) => (
                          <Badge key={i} colorScheme="blue" variant="subtle" fontSize="xs">{skill}</Badge>
                        ))}
                      </Flex>
                    </Td>
                    <Td>
                      <Badge bg="#e0f2ff" color="#3182ce" fontWeight="bold" fontSize="sm">
                        {candidate.matchScore}%
                      </Badge>
                    </Td>
                    <Td>
                      <Badge color="goldenrod" fontWeight="bold">{candidate.intent?.toUpperCase()}</Badge>
                    </Td>
                    <Td><Text fontSize="sm">{candidate.lastActivity}</Text></Td>
                    <Td>
                      <Flex gap={1} wrap="wrap">
                        {candidate.futureGoals?.map((goal: string, i: number) => (
                          <Badge key={i} colorScheme={futureGoalColorMap[goal] || 'gray'} variant="subtle" fontSize="xs">
                            {goal}
                          </Badge>
                        ))}
                      </Flex>
                    </Td>
                    <Td><MiniStarsignBadge color={colors.border} /></Td>
                  </Tr>
                );
              })}
            </Tbody>
          </Table>
        </Box>
      )}
    </Box>
  );
};

export default MarketplaceTable;
