// lib/ThemeContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { THEMES, ThemeId } from '@/theme/themes';

interface ThemeContextProps {
  themeId: ThemeId;
  setThemeId: (id: ThemeId) => void;
  theme: typeof THEMES[ThemeId];
}

const ThemeContext = createContext<ThemeContextProps | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [themeId, setThemeId] = useState<ThemeId>('cosmic');

  useEffect(() => {
    const stored = localStorage.getItem('star-theme') as ThemeId;
    if (stored && THEMES[stored]) {
      setThemeId(stored);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('star-theme', themeId);
  }, [themeId]);

  const value: ThemeContextProps = {
    themeId,
    setThemeId,
    theme: THEMES[themeId],
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};

export const useThemeContext = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useThemeContext must be used within ThemeProvider');
  return context;
};