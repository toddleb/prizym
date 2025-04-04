// components/Sidebar.tsx
import { Box, VStack, Text, Link as ChakraLink } from '@chakra-ui/react';
import Link from 'next/link';

const navConfig: Record<string, { label: string; path: string }[]> = {
  student: [
    { label: 'Dashboard', path: '/student/dashboard' },
    { label: 'Star Signature', path: '/student/signature' },
    { label: 'Programs', path: '/student/programs' },
  ],
  program: [
    { label: 'Dashboard', path: '/program/dashboard' },
    { label: 'Candidates', path: '/program/candidates' },
    { label: 'Campaigns', path: '/program/campaigns' },
  ],
  agency: [
    { label: 'Dashboard', path: '/agency/dashboard' },
    { label: 'Clients', path: '/agency/clients' },
    { label: 'Analytics', path: '/agency/analytics' },
  ],
  military: [
    { label: 'Dashboard', path: '/military/dashboard' },
    { label: 'Specialties', path: '/military/specialties' },
    { label: 'Transition', path: '/military/transition' },
  ],
};

export default function Sidebar({ role }: { role: string }) {
  const links = navConfig[role] || [];

  return (
    <Box
      w="64"
      bg="gray.800"
      color="white"
      minH="100vh"
      px={4}
      py={6}
      position="sticky"
      top="0"
      display="flex"
      flexDirection="column"
      justifyContent="space-between"
    >
      <Box>
        <Text fontSize="xl" fontWeight="bold" mb={8} textTransform="capitalize">
          {role} Portal
        </Text>
        <VStack align="start" spacing={4}>
          {links.map(({ label, path }) => (
            <ChakraLink
              as={Link}
              href={path}
              key={path}
              _hover={{ color: 'brand.starlight' }}
            >
              {label}
            </ChakraLink>
          ))}
        </VStack>
      </Box>

      <Box pt={6} borderTop="1px" borderColor="gray.700">
        <ChakraLink
          as={Link}
          href="/settings"
          fontSize="sm"
          color="gray.400"
        >
          ⚙️ Theme Settings
        </ChakraLink>
      </Box>
    </Box>
  );
}
