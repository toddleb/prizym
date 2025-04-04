// components/RecommendedPrograms.tsx
import { Text, SimpleGrid, Button, VStack } from '@chakra-ui/react';
import DashboardCard from './common/DashboardCard';

const mockPrograms = [
  { title: 'Data Science Bootcamp', match: 92 },
  { title: 'UX Design Certificate', match: 88 },
];

export default function RecommendedPrograms() {
  return (
    <DashboardCard title="Recommended Programs">
      <SimpleGrid columns={1} spacing={3}>
        {mockPrograms.map((program, idx) => (
          <VStack
            key={idx}
            align="start"
            spacing={1}
            p={3}
            borderWidth={1}
            borderRadius="lg"
            bg="gray.600"
            fontSize="xs"
          >
            <Text fontWeight="semibold">{program.title}</Text>
            <Text color="gray.300">✨ {program.match}% Match</Text>
            <Button size="xs" colorScheme="blue">View Details</Button>
          </VStack>
        ))}
      </SimpleGrid>
    </DashboardCard>
  );
}