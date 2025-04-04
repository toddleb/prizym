// components/Navbar.tsx
import { Box, Flex, Text } from '@chakra-ui/react';

export default function Navbar() {
  return (
    <Flex
      as="nav"
      px={6}
      py={4}
      bg="brand.nebula"
      color="white"
      align="center"
      justify="space-between"
      boxShadow="md"
    >
      <Text fontSize="lg" fontWeight="bold">
        ✨ Star Navigator
      </Text>
    </Flex>
  );
}