// pages/student/dashboard.tsx
import Layout from '@/components/Layout';
import {
  Box,
  Flex,
  Heading,
  Text,
  IconButton,
  SimpleGrid,
  Stack,
} from '@chakra-ui/react';
import { SettingsIcon } from '@chakra-ui/icons';
import StarSignProgress from '@/components/StarSignProgress';
import DailyStarBurst from '@/components/DailyStarBurst';
import RecommendedPrograms from '@/components/RecommendedPrograms';
import YourProgress from '@/components/YourProgress';
import StarSignature from '@/components/StarSignature';
import MarketplaceGrid from '@/components/MarketplaceGrid';
import CosmicAlignment from '@/components/CosmicAlignment';
import StarBurstAssessment from '@/components/StarBurstAssessment';
import StudentTimeline from '@/components/StudentTimeline';

export default function StudentDashboard() {
  return (
    <Layout>
      <Box p={6}>
        {/* Header */}
        <Flex align="center" mb={6}>
          <Heading size="lg">Student Dashboard</Heading>
          <Box ml="auto">
            <Text mr={4} display="inline-block">Cosmic Credits: 475</Text>
            <IconButton aria-label="Settings" icon={<SettingsIcon />} />
          </Box>
        </Flex>

        {/* 🌌 COSMIC OVERVIEW */}
        <Heading size="md" mb={4}>🌌 Your Cosmic Overview</Heading>
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} mb={10}>
          <StarSignProgress percent={45} />
          <StarSignature />
        </SimpleGrid>

        {/* 🌟 DAILY INTERACTION */}
        <Heading size="md" mb={4}>🌟 Daily Engagement</Heading>
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6} mb={10}>
          <DailyStarBurst onStart={() => console.log('Start assessment')} />
          <StarBurstAssessment />
        </SimpleGrid>

        {/* 🎓 OPPORTUNITY HUB */}
        <Heading size="md" mb={4}>🎓 Opportunity Hub</Heading>
        <Stack spacing={6} mb={10}>
          <RecommendedPrograms />
          <MarketplaceGrid />
          <CosmicAlignment />
        </Stack>

        {/* 🚀 JOURNEY & GROWTH */}
        <Heading size="md" mb={4}>🚀 Your Journey</Heading>
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
          <YourProgress />
          <StudentTimeline />
        </SimpleGrid>
      </Box>
    </Layout>
  );
}
