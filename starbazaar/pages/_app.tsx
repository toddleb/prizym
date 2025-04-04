// pages/_app.tsx
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import type { AppProps } from 'next/app';
import { useMemo } from 'react';
import { ThemeProvider, useThemeContext } from '../lib/ThemeContext';
import Starfield from '../components/Starfield';

function ThemedApp({ Component, pageProps }: AppProps) {
  const { theme } = useThemeContext();

  const chakraTheme = useMemo(
    () =>
      extendTheme({
        colors: {
          brand: {
            starlight: theme.accentColor,
          },
        },
        styles: {
          global: {
            body: {
              bg: theme.bg || theme.bgGradient,
              color: theme.textColor,
            },
          },
        },
        fonts: {
          heading: theme.headingFont,
          body: theme.bodyFont,
        },
      }),
    [theme]
  );

  return (
    <ChakraProvider theme={chakraTheme}>
      <Starfield />
      <Component {...pageProps} />
    </ChakraProvider>
  );
}

export default function App(props: AppProps) {
  return (
    <ThemeProvider>
      <ThemedApp {...props} />
    </ThemeProvider>
  );
}
