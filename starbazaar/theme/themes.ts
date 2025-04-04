// theme/themes.ts

export const THEMES = {
  cosmic: {
    id: 'cosmic',
    label: 'Cosmic Theme',
    accentColor: 'purple.400',
    bgGradient: 'linear(to-b, #1a1a40, #0f0f2d)',
    textColor: 'whiteAlpha.900',
    cardBg: 'gray.700',
    headingFont: 'heading',
    bodyFont: 'body',
  },
  modern: {
    id: 'modern',
    label: 'Modern Theme',
    accentColor: 'blue.500',
    bg: 'gray.50',
    textColor: 'gray.800',
    cardBg: 'white',
    headingFont: 'heading',
    bodyFont: 'body',
  },
  naval: {
    id: 'naval',
    label: 'Structured Naval Theme',
    accentColor: 'teal.500',
    bg: 'gray.900',
    textColor: 'whiteAlpha.800',
    cardBg: 'gray.800',
    headingFont: 'mono',
    bodyFont: 'mono',
  },
};

export type ThemeId = keyof typeof THEMES;
