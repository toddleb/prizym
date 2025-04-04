// pages/settings.tsx
import { useState } from 'react';
import {
  Box,
  Heading,
  Text,
  RadioGroup,
  Stack,
  Radio,
  Button,
} from '@chakra-ui/react';
import { useRouter } from 'next/router';
import { THEMES, ThemeId } from '@/theme/themes';
import { useThemeContext } from '@/lib/ThemeContext';

export default function SettingsPage() {
  const { themeId, setThemeId } = useThemeContext();
  const [selectedTheme, setSelectedTheme] = useState<ThemeId>(themeId);
  const router = useRouter();

  const handleSave = () => {
    setThemeId(selectedTheme);
    localStorage.setItem('star-theme', selectedTheme);
    console.log('Theme saved:', selectedTheme);
  };

  return (
    <Box maxW="600px" mx="auto" p={6}>
      <Heading size="lg" mb={4}>Theme Settings</Heading>
      <Text mb={2}>Select your preferred theme:</Text>

      <RadioGroup
        value={selectedTheme}
        onChange={(val) => setSelectedTheme(val as ThemeId)}
      >
        <Stack spacing={4}>
          {Object.entries(THEMES).map(([key, theme]) => (
            <Radio key={key} value={key} colorScheme="purple">
              <Box>
                <Text fontWeight="bold">{theme.label}</Text>
                <Text fontSize="sm" color="gray.500">
                  Accent: {theme.accentColor}, Background: {theme.bg || theme.bgGradient}
                </Text>
              </Box>
            </Radio>
          ))}
        </Stack>
      </RadioGroup>

      <Stack direction="row" mt={6} spacing={4}>
        <Button colorScheme="purple" onClick={handleSave}>
          Save Theme
        </Button>
        <Button variant="outline" onClick={() => router.push('/student/dashboard')}>
          Back to Dashboard
        </Button>
      </Stack>
    </Box>
  );
}