// components/StarSignProgress.tsx
import { Text, Progress, Icon, VStack, HStack } from '@chakra-ui/react';
import { FaStar } from 'react-icons/fa';
import DashboardCard from './common/DashboardCard';

export default function StarSignProgress({ percent = 45 }) {
  return (
    <DashboardCard title="Your Star Sign">
      <HStack spacing={3} align="center" mb={2}>
        <Icon as={FaStar} boxSize={6} color="yellow.400" />
        <Text fontSize="md" fontWeight="semibold">{percent}% Complete</Text>
      </HStack>
      <Progress value={percent} colorScheme="purple" borderRadius="lg" mb={2} />
      <Text fontSize="sm" mb={1} color="gray.300">Status: Developing Constellation</Text>
      <Text fontSize="xs" color="gray.400">
        Your cosmic profile is forming. Keep engaging with assessments and daily bursts to reveal your full Star Signature.
      </Text>
    </DashboardCard>
  );
}