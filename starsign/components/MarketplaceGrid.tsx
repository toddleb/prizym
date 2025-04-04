// components/MarketplaceGrid.tsx
import {
  Text,
  SimpleGrid,
  Input,
  Button,
  VStack,
} from '@chakra-ui/react';
import DashboardCard from './common/DashboardCard';

const mockPrograms = [
  {
    title: 'Data Science Bootcamp',
    match: 92,
    location: 'Online',
    cost: '$12,500',
  },
  {
    title: 'UX Design Certificate',
    match: 88,
    location: 'NYC',
    cost: '$8,000',
  },
];

export default function MarketplaceGrid() {
  return (
    <DashboardCard title="Explore More Programs">
      <Input
        placeholder="Search Programs..."
        size="sm"
        mb={3}
        bg="gray.800"
        borderColor="gray.600"
      />
      <SimpleGrid columns={1} spacing={3}>
        {mockPrograms.map((program, idx) => (
          <VStack
            key={idx}
            align="start"
            spacing={1}
            p={3}
            borderWidth={1}
            borderRadius="md"
            bg="gray.600"
            fontSize="xs"
          >
            <Text fontWeight="semibold">{program.title}</Text>
            <Text color="gray.300">{program.location} · {program.cost}</Text>
            <Text color="purple.300">✨ {program.match}% Match</Text>
            <Button size="xs" colorScheme="blue">View Details</Button>
          </VStack>
        ))}
      </SimpleGrid>
    </DashboardCard>
  );
}