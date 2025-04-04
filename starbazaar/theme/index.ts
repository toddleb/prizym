// theme/index.ts
import { extendTheme } from '@chakra-ui/react';
import { THEMES } from './themes';

const theme = extendTheme({
  colors: {
    brand: {
      starlight: THEMES.cosmic.accentColor,
    },
  },
  styles: {
    global: {
      body: {
        bg: THEMES.cosmic.bgGradient,
        color: THEMES.cosmic.textColor,
      },
    },
  },
  fonts: {
    heading: THEMES.cosmic.headingFont,
    body: THEMES.cosmic.bodyFont,
  },
});

export default theme;