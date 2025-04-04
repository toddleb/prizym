import { Box } from '@chakra-ui/react';
import { keyframes } from '@emotion/react';
import { useIsClient } from '../lib/useIsClient';

const twinkle = keyframes`
  0%, 100% { opacity: 0.8; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
`;

export default function Starfield() {
  const isClient = useIsClient();

  if (!isClient) return null; // ✅ No server-side render

  const stars = Array.from({ length: 80 }).map((_, i) => {
    const size = Math.random() * 3 + 1;
    const top = Math.random() * 100;
    const left = Math.random() * 100;
    const duration = Math.random() * 4 + 3;

    return (
      <Box
        key={i}
        position="absolute"
        top={`${top}%`}
        left={`${left}%`}
        width={`${size}px`}
        height={`${size}px`}
        bg="whiteAlpha.700"
        borderRadius="full"
        animation={`${twinkle} ${duration}s ease-in-out infinite`}
        zIndex="0"
      />
    );
  });

  return (
    <Box
      position="fixed"
      top="0"
      left="0"
      w="100%"
      h="100%"
      overflow="hidden"
      zIndex="0"
      pointerEvents="none"
    >
      {stars}
    </Box>
  );
}