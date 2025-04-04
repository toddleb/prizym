// components/CosmicAlignment.tsx
import {
  Text,
  VStack,
  HStack,
  Divider,
  Button,
} from '@chakra-ui/react';
import DashboardCard from './common/DashboardCard';

export default function CosmicAlignment() {
  return (
    <DashboardCard title="Cosmic Alignment">
      <Text fontSize="xs" color="gray.300" mb={2}>
        Alignment Score: <strong>92%</strong>
      </Text>
      <HStack spacing={3} mb={3} fontSize="xs">
        <VStack flex={1} bg="gray.600" p={2} borderRadius="md">
          <Text textAlign="center">[Student Pattern]</Text>
        </VStack>
        <VStack flex={1} bg="gray.600" p={2} borderRadius="md">
          <Text textAlign="center">[Program Pattern]</Text>
        </VStack>
      </HStack>
      <Divider mb={2} />
      <VStack align="start" spacing={1} fontSize="xs">
        <Text fontWeight="semibold">Perfect Matches:</Text>
        <Text color="gray.300">• Python Programming</Text>
        <Text color="gray.300">• Learning Pace</Text>
        <Text color="gray.300">• Problem-solving</Text>
      </VStack>
      <HStack spacing={3} mt={3} justify="flex-end">
        <Button size="xs" colorScheme="green">Express Interest</Button>
        <Button size="xs">Message</Button>
        <Button size="xs" variant="outline">Save</Button>
      </HStack>
    </DashboardCard>
  );
}