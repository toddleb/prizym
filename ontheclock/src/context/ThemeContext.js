// Theme system for the NFL Draft App
// Provides various theme options and color utilities

// Pre-defined themes
const themes = {
  default: {
    name: 'default',
    primaryColor: '#3B82F6',  // Blue-500
    secondaryColor: '#10B981', // Emerald-500
    accentColor: '#F59E0B',    // Amber-500
    backgroundColor: '#F3F4F6', // Gray-100
    surfaceColor: '#FFFFFF',    // White
    textColor: '#111827',       // Gray-900
    textSecondaryColor: '#6B7280', // Gray-500
    errorColor: '#EF4444',      // Red-500
    warningColor: '#F59E0B',    // Amber-500
    successColor: '#10B981',    // Emerald-500
    fieldStyle: 'standard',
    useTeamColors: true,
    fontSize: 'medium',
    borderRadius: 'medium',
    shadows: 'medium',
    isDark: false
  },
  
  dark: {
    name: 'dark',
    primaryColor: '#60A5FA',  // Blue-400
    secondaryColor: '#34D399', // Emerald-400
    accentColor: '#FBBF24',    // Amber-400
    backgroundColor: '#1F2937', // Gray-800
    surfaceColor: '#111827',    // Gray-900
    textColor: '#F9FAFB',       // Gray-50
    textSecondaryColor: '#9CA3AF', // Gray-400
    errorColor: '#F87171',      // Red-400
    warningColor: '#FBBF24',    // Amber-400
    successColor: '#34D399',    // Emerald-400
    fieldStyle: 'turf',
    useTeamColors: true,
    fontSize: 'medium',
    borderRadius: 'medium',
    shadows: 'large',
    isDark: true
  },
  
  light: {
    name: 'light',
    primaryColor: '#2563EB',  // Blue-600
    secondaryColor: '#059669', // Emerald-600
    accentColor: '#D97706',    // Amber-600
    backgroundColor: '#FFFFFF', // White
    surfaceColor: '#F9FAFB',    // Gray-50
    textColor: '#111827',       // Gray-900
    textSecondaryColor: '#4B5563', // Gray-600
    errorColor: '#DC2626',      // Red-600
    warningColor: '#D97706',    // Amber-600
    successColor: '#059669',    // Emerald-600
    fieldStyle: 'standard',
    useTeamColors: true,
    fontSize: 'medium',
    borderRadius: 'small',
    shadows: 'small',
    isDark: false
  },
  
  contrast: {
    name: 'contrast',
    primaryColor: '#1D4ED8',  // Blue-700
    secondaryColor: '#047857', // Emerald-700
    accentColor: '#B45309',    // Amber-700
    backgroundColor: '#FFFFFF', // White
    surfaceColor: '#F9FAFB',    // Gray-50
    textColor: '#000000',       // Black
    textSecondaryColor: '#1F2937', // Gray-800
    errorColor: '#B91C1C',      // Red-700
    warningColor: '#B45309',    // Amber-700
    successColor: '#047857',    // Emerald-700
    fieldStyle: 'standard',
    useTeamColors: false,
    fontSize: 'large',
    borderRadius: 'small',
    shadows: 'none',
    isDark: false
  },
  
  retro: {
    name: 'retro',
    primaryColor: '#1E40AF',  // Blue-800
    secondaryColor: '#065F46', // Emerald-800
    accentColor: '#92400E',    // Amber-800
    backgroundColor: '#FEF3C7', // Amber-100
    surfaceColor: '#FFFBEB',    // Amber-50
    textColor: '#1F2937',       // Gray-800
    textSecondaryColor: '#4B5563', // Gray-600
    errorColor: '#991B1B',      // Red-800
    warningColor: '#92400E',    // Amber-800
    successColor: '#065F46',    // Emerald-800
    fieldStyle: 'retro',
    useTeamColors: true,
    fontSize: 'medium',
    borderRadius: 'large',
    shadows: 'inner',
    isDark: false
  },
  
  modern: {
    name: 'modern',
    primaryColor: '#2563EB',  // Blue-600
    secondaryColor: '#10B981', // Emerald-500
    accentColor: '#F59E0B',    // Amber-500
    backgroundColor: '#0F172A', // Slate-900
    surfaceColor: '#1E293B',    // Slate-800
    textColor: '#F1F5F9',       // Slate-100
    textSecondaryColor: '#94A3B8', // Slate-400
    errorColor: '#EF4444',      // Red-500
    warningColor: '#F59E0B',    // Amber-500
    successColor: '#10B981',    // Emerald-500
    fieldStyle: 'modern',
    useTeamColors: true,
    fontSize: 'medium',
    borderRadius: 'large',
    shadows: 'colored',
    isDark: true
  },
  
  custom: {
    name: 'custom',
    primaryColor: '#3B82F6',  // Default starting point
    secondaryColor: '#10B981',
    accentColor: '#F59E0B',
    backgroundColor: '#F3F4F6',
    surfaceColor: '#FFFFFF',
    textColor: '#111827',
    textSecondaryColor: '#6B7280',
    errorColor: '#EF4444',
    warningColor: '#F59E0B',
    successColor: '#10B981',
    fieldStyle: 'standard',
    useTeamColors: true,
    fontSize: 'medium',
    borderRadius: 'medium',
    shadows: 'medium',
    isDark: false
  }
};

// Field styles definitions
const fieldStyles = {
  standard: {
    fieldColor: '#55A630', // Standard grass green
    lineColor: '#FFFFFF',
    endZoneColor1: '#D00000',
    endZoneColor2: '#3185FC',
    lineOpacity: 0.3,
    texture: 'linear'
  },
  turf: {
    fieldColor: '#36A151', // Artificial turf
    lineColor: '#FFFFFF',
    endZoneColor1: '#FF0000',
    endZoneColor2: '#0000FF',
    lineOpacity: 0.4,
    texture: 'striped'
  },
  retro: {
    fieldColor: '#5A8F29', // Older style grass
    lineColor: '#FFFFFF',
    endZoneColor1: '#B22234',
    endZoneColor2: '#233B76',
    lineOpacity: 0.25,
    texture: 'grainy'
  },
  modern: {
    fieldColor: '#1A8D38', // Modern stadium turf
    lineColor: '#FFFFFF',
    endZoneColor1: '#CC0000',
    endZoneColor2: '#0033A0',
    lineOpacity: 0.5,
    texture: 'glossy'
  }
};

// Font size options
const fontSizes = {
  small: {
    base: '0.875rem', // 14px
    h1: '1.5rem',     // 24px
    h2: '1.25rem',    // 20px
    h3: '1.125rem',   // 18px
    body: '0.875rem',  // 14px
    small: '0.75rem'   // 12px
  },
  medium: {
    base: '1rem',      // 16px
    h1: '1.75rem',     // 28px
    h2: '1.5rem',      // 24px
    h3: '1.25rem',     // 20px
    body: '1rem',      // 16px
    small: '0.875rem'  // 14px
  },
  large: {
    base: '1.125rem',  // 18px
    h1: '2rem',        // 32px
    h2: '1.75rem',     // 28px
    h3: '1.5rem',      // 24px
    body: '1.125rem',  // 18px
    small: '1rem'      // 16px
  }
};

// Border radius options
const borderRadii = {
  none: '0',
  small: '0.25rem',  // 4px
  medium: '0.375rem', // 6px
  large: '0.5rem',    // 8px
  full: '9999px'      // Circle
};

// Shadow options
const shadows = {
  none: 'none',
  small: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  medium: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  large: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
  colored: (color) => `0 4px 6px -1px ${color}33, 0 2px 4px -1px ${color}26` // With opacity
};

// Theme manager class
class ThemeManager {
  constructor(initialTheme = 'default') {
    this.activeTheme = themes[initialTheme] || themes.default;
    this.listeners = [];
  }
  
  // Get the current theme
  getTheme() {
    return { ...this.activeTheme };
  }
  
  // Get all available themes
  getAvailableThemes() {
    return Object.keys(themes);
  }
  
  // Switch to a different theme
  setTheme(themeName) {
    if (themes[themeName]) {
      this.activeTheme = themes[themeName];
      this.notifyListeners();
      return true;
    }
    return false;
  }
  
  // Update a custom theme
  updateCustomTheme(customProperties) {
    themes.custom = {
      ...themes.custom,
      ...customProperties,
      name: 'custom' // Ensure name stays as 'custom'
    };
    
    if (this.activeTheme.name === 'custom') {
      this.activeTheme = themes.custom;
      this.notifyListeners();
    }
    
    return themes.custom;
  }
  
  // Get field style for the current theme
  getFieldStyle() {
    return fieldStyles[this.activeTheme.fieldStyle] || fieldStyles.standard;
  }
  
  // Get font sizes for the current theme
  getFontSizes() {
    return fontSizes[this.activeTheme.fontSize] || fontSizes.medium;
  }
  
  // Get border radius for the current theme
  getBorderRadius() {
    return borderRadii[this.activeTheme.borderRadius] || borderRadii.medium;
  }
  
  // Get shadow style for current theme
  getShadow() {
    const shadowStyle = this.activeTheme.shadows;
    
    if (shadowStyle === 'colored') {
      return shadows.colored(this.activeTheme.primaryColor);
    }
    
    return shadows[shadowStyle] || shadows.medium;
  }
  
  // Add a change listener
  addChangeListener(listener) {
    if (typeof listener === 'function') {
      this.listeners.push(listener);
    }
  }
  
  // Remove a change listener
  removeChangeListener(listener) {
    this.listeners = this.listeners.filter(l => l !== listener);
  }
  
  // Notify all listeners of theme change
  notifyListeners() {
    this.listeners.forEach(listener => {
      try {
        listener(this.activeTheme);
      } catch (e) {
        console.error('Error in theme change listener:', e);
      }
    });
  }
  
  // Apply theme to the document (for web applications)
  applyToDocument() {
    // Create or update CSS variables in the document root
    const root = document.documentElement;
    
    Object.entries(this.activeTheme).forEach(([key, value]) => {
      if (typeof value === 'string' && (value.startsWith('#') || value.startsWith('rgb'))) {
        root.style.setProperty(`--theme-${kebabCase(key)}`, value);
      }
    });
    
    // Apply font sizes
    const sizes = this.getFontSizes();
    Object.entries(sizes).forEach(([key, value]) => {
      root.style.setProperty(`--font-${key}`, value);
    });
    
    // Apply border radius
    root.style.setProperty('--border-radius', this.getBorderRadius());
    
    // Apply shadows
    root.style.setProperty('--shadow', this.getShadow());
    
    // Apply dark/light mode class
    if (this.activeTheme.isDark) {
      document.body.classList.add('dark-mode');
      document.body.classList.remove('light-mode');
    } else {
      document.body.classList.add('light-mode');
      document.body.classList.remove('dark-mode');
    }
  }
  
  // Get CSS classes based on the current theme
  getThemeClasses(componentType) {
    // This would return appropriate Tailwind CSS classes
    // Here's a simplified example
    const classes = {
      button: {
        primary: `bg-[${this.activeTheme.primaryColor}] text-white font-medium py-2 px-4 rounded hover:bg-opacity-90`,
        secondary: `bg-[${this.activeTheme.secondaryColor}] text-white font-medium py-2 px-4 rounded hover:bg-opacity-90`,
        accent: `bg-[${this.activeTheme.accentColor}] text-white font-medium py-2 px-4 rounded hover:bg-opacity-90`
      },
      card: `bg-[${this.activeTheme.surfaceColor}] rounded-lg ${this.activeTheme.shadows !== 'none' ? 'shadow-md' : ''}`,
      text: {
        primary: `text-[${this.activeTheme.textColor}]`,
        secondary: `text-[${this.activeTheme.textSecondaryColor}]`
      }
      // Add more component types as needed
    };
    
    return componentType ? classes[componentType] : classes;
  }
}

// Utility to convert camelCase to kebab-case for CSS variables
function kebabCase(str) {
  return str.replace(/([a-z0-9]|(?=[A-Z]))([A-Z])/g, '$1-$2').toLowerCase();
}

// Export the theme manager and related constants
export { 
  ThemeManager, 
  themes as predefinedThemes, 
  fieldStyles, 
  fontSizes, 
  borderRadii, 
  shadows 
};