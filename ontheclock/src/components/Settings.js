import React, { useState, useContext, useEffect } from 'react';
import { DraftContext } from '../context/DraftContext';
import { ThemeManager } from '../context/ThemeContext';

/**
 * Settings component for the NFL Draft Simulator
 * Allows users to customize their draft experience
 */
const Settings = () => {
  const { 
    userTeam, 
    selectTeam,
    draftMode, 
    setDraftMode,
    resetDraft
  } = useContext(DraftContext);
  
  // Local state for settings
  const [activeSection, setActiveSection] = useState('general');
  const [themeMode, setThemeMode] = useState('default');
  const [draftSpeed, setDraftSpeed] = useState('normal');
  const [soundEffects, setSoundEffects] = useState(true);
  const [notifications, setNotifications] = useState(true);
  const [autoSave, setAutoSave] = useState(true);
  const [userPreferences, setUserPreferences] = useState({
    showTradeValues: true,
    showProspectGrades: true,
    showTeamNeeds: true,
    confirmSelections: true,
    autoAdvance: true
  });
  const [multiplayerSettings, setMultiplayerSettings] = useState({
    draftTimeout: 120,
    allowTrading: true,
    autoAssignTeams: true,
    fillWithAI: true
  });
  const [isDirty, setIsDirty] = useState(false);
  const [showResetConfirm, setShowResetConfirm] = useState(false);
  
  // Load settings from localStorage on mount
  useEffect(() => {
    const savedSettings = localStorage.getItem('nfl_draft_settings');
    if (savedSettings) {
      try {
        const parsedSettings = JSON.parse(savedSettings);
        
        // Apply saved settings to state
        if (parsedSettings.themeMode) setThemeMode(parsedSettings.themeMode);
        if (parsedSettings.draftSpeed) setDraftSpeed(parsedSettings.draftSpeed);
        if (parsedSettings.soundEffects !== undefined) setSoundEffects(parsedSettings.soundEffects);
        if (parsedSettings.notifications !== undefined) setNotifications(parsedSettings.notifications);
        if (parsedSettings.autoSave !== undefined) setAutoSave(parsedSettings.autoSave);
        if (parsedSettings.userPreferences) setUserPreferences({
          ...userPreferences,
          ...parsedSettings.userPreferences
        });
        if (parsedSettings.multiplayerSettings) setMultiplayerSettings({
          ...multiplayerSettings,
          ...parsedSettings.multiplayerSettings
        });
        
        console.log('[Settings] Loaded settings from localStorage');
      } catch (error) {
        console.error('Error loading settings:', error);
      }
    }
  }, []);
  
  // Save settings to localStorage when changed
  useEffect(() => {
    if (isDirty && autoSave) {
      saveSettings();
      setIsDirty(false);
    }
  }, [
    themeMode, 
    draftSpeed, 
    soundEffects, 
    notifications, 
    userPreferences, 
    multiplayerSettings,
    isDirty,
    autoSave
  ]);
  
  // Apply theme when themeMode changes
  useEffect(() => {
    const themeManager = new ThemeManager(themeMode);
    themeManager.applyToDocument();
  }, [themeMode]);
  
  // Save all settings to localStorage
  const saveSettings = () => {
    try {
      const settingsToSave = {
        themeMode,
        draftSpeed,
        soundEffects,
        notifications,
        autoSave,
        userPreferences,
        multiplayerSettings
      };
      
      localStorage.setItem('nfl_draft_settings', JSON.stringify(settingsToSave));
      console.log('[Settings] Saved settings to localStorage');
      return true;
    } catch (error) {
      console.error('Error saving settings:', error);
      return false;
    }
  };
  
  // Reset all settings to defaults
  const resetSettings = () => {
    setThemeMode('default');
    setDraftSpeed('normal');
    setSoundEffects(true);
    setNotifications(true);
    setAutoSave(true);
    setUserPreferences({
      showTradeValues: true,
      showProspectGrades: true,
      showTeamNeeds: true,
      confirmSelections: true,
      autoAdvance: true
    });
    setMultiplayerSettings({
      draftTimeout: 120,
      allowTrading: true,
      autoAssignTeams: true,
      fillWithAI: true
    });
    
    setIsDirty(true);
    setShowResetConfirm(false);
  };
  
  // Handle checkbox changes for preferences
  const handlePreferenceChange = (key, value) => {
    setUserPreferences({
      ...userPreferences,
      [key]: value
    });
    setIsDirty(true);
  };
  
  // Handle multiplayer settings changes
  const handleMultiplayerSettingChange = (key, value) => {
    setMultiplayerSettings({
      ...multiplayerSettings,
      [key]: value
    });
    setIsDirty(true);
  };
  
  // Export settings as JSON file
  const exportSettings = () => {
    try {
      const settingsToExport = {
        themeMode,
        draftSpeed,
        soundEffects,
        notifications,
        autoSave,
        userPreferences,
        multiplayerSettings,
        exportDate: new Date().toISOString()
      };
      
      const jsonString = JSON.stringify(settingsToExport, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = 'nfl_draft_settings.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      return true;
    } catch (error) {
      console.error('Error exporting settings:', error);
      return false;
    }
  };
  
  // Import settings from JSON file
  const importSettings = (event) => {
    try {
      const file = event.target.files[0];
      if (!file) return;
      
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importedSettings = JSON.parse(e.target.result);
          
          // Validate imported settings
          if (!importedSettings.userPreferences || !importedSettings.multiplayerSettings) {
            throw new Error('Invalid settings file');
          }
          
          // Apply imported settings
          setThemeMode(importedSettings.themeMode || 'default');
          setDraftSpeed(importedSettings.draftSpeed || 'normal');
          setSoundEffects(importedSettings.soundEffects !== undefined ? importedSettings.soundEffects : true);
          setNotifications(importedSettings.notifications !== undefined ? importedSettings.notifications : true);
          setAutoSave(importedSettings.autoSave !== undefined ? importedSettings.autoSave : true);
          setUserPreferences({
            ...userPreferences,
            ...importedSettings.userPreferences
          });
          setMultiplayerSettings({
            ...multiplayerSettings,
            ...importedSettings.multiplayerSettings
          });
          
          setIsDirty(true);
          
          // Clear file input
          event.target.value = null;
        } catch (error) {
          console.error('Error parsing settings file:', error);
          alert('Invalid settings file. Please try again with a valid file.');
          event.target.value = null;
        }
      };
      reader.readAsText(file);
    } catch (error) {
      console.error('Error importing settings:', error);
    }
  };
  
  // Handler for reset draft button
  const handleResetDraft = () => {
    if (showResetConfirm) {
      resetDraft();
      setShowResetConfirm(false);
    } else {
      setShowResetConfirm(true);
    }
  };
  
  return (
    <div className="bg-white rounded-lg shadow-md h-full flex flex-col">
      <div className="p-4 border-b">
        <h2 className="text-xl font-bold">Settings</h2>
        <p className="text-sm text-gray-600">Customize your draft experience</p>
      </div>
      
      {/* Navigation tabs */}
      <div className="border-b">
        <nav className="flex">
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeSection === 'general' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveSection('general')}
          >
            General
          </button>
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeSection === 'appearance' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveSection('appearance')}
          >
            Appearance
          </button>
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeSection === 'preferences' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveSection('preferences')}
          >
            Preferences
          </button>
          <button
            className={`px-4 py-2 text-sm font-medium ${
              activeSection === 'multiplayer' ? 'border-b-2 border-blue-500 text-blue-600' : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveSection('multiplayer')}
          >
            Multiplayer
          </button>
        </nav>
      </div>
      
      {/* Content area */}
      <div className="flex-1 overflow-y-auto p-4">
        {activeSection === 'general' && (
          <div>
            <h3 className="font-bold text-lg mb-4">General Settings</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Draft Mode</label>
              <select
                className="w-full p-2 border rounded"
                value={draftMode}
                onChange={(e) => {
                  setDraftMode(e.target.value);
                  setIsDirty(true);
                }}
              >
                <option value="solo">Solo Mode</option>
                <option value="spectator">Spectator Mode</option>
                <option value="multiplayer">Multiplayer Mode</option>
              </select>
              <p className="mt-1 text-xs text-gray-500">
                Solo: Control one team | Spectator: Watch AI draft | Multiplayer: Draft with others
              </p>
            </div>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Draft Speed</label>
              <select
                className="w-full p-2 border rounded"
                value={draftSpeed}
                onChange={(e) => {
                  setDraftSpeed(e.target.value);
                  setIsDirty(true);
                }}
              >
                <option value="slow">Slow (15 seconds)</option>
                <option value="normal">Normal (8 seconds)</option>
                <option value="fast">Fast (3 seconds)</option>
                <option value="instant">Instant</option>
              </select>
              <p className="mt-1 text-xs text-gray-500">
                Controls how quickly AI teams make their picks
              </p>
            </div>
            
            <div className="space-y-4 mb-6">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Sound Effects</span>
                  <p className="text-xs text-gray-500">Play sounds for picks and trades</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={multiplayerSettings.allowTrading}
                    onChange={(e) => handleMultiplayerSettingChange('allowTrading', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Auto-assign Teams</span>
                  <p className="text-xs text-gray-500">Automatically assign teams to players</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={multiplayerSettings.autoAssignTeams}
                    onChange={(e) => handleMultiplayerSettingChange('autoAssignTeams', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Fill with AI</span>
                  <p className="text-xs text-gray-500">Fill remaining teams with AI players</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={multiplayerSettings.fillWithAI}
                    onChange={(e) => handleMultiplayerSettingChange('fillWithAI', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
            </div>
            
            <div className="bg-blue-50 border border-blue-300 p-4 rounded-lg mb-6">
              <h4 className="font-medium text-blue-800 mb-2">Multiplayer Mode</h4>
              <p className="text-sm text-blue-700 mb-2">
                Draft with friends or join public lobbies. Create a room and invite others to join your draft experience.
              </p>
              <p className="text-sm text-blue-700">
                These settings only apply when hosting your own draft lobby.
              </p>
            </div>
            
            <div className="border-t pt-4 mt-4">
              <h3 className="font-bold mb-3">Connection Status</h3>
              <div className="flex items-center">
                <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
                <span className="text-sm text-gray-700">Connected to multiplayer services</span>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                Multiplayer features are available. You can join or create draft lobbies.
              </p>
            </div>
          </div>
        )}
      </div>
      
      <div className="p-4 border-t bg-gray-50 flex items-center justify-between">
        <div className="text-xs text-gray-500">
          Settings are {autoSave ? 'automatically saved' : 'not being auto-saved'}
        </div>
        {!autoSave && (
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            onClick={saveSettings}
          >
            Save Settings
          </button>
        )}
      </div>
    </div>
  );
};

export default Settings;
                    className="sr-only peer"
                    checked={soundEffects}
                    onChange={(e) => {
                      setSoundEffects(e.target.checked);
                      setIsDirty(true);
                    }}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Notifications</span>
                  <p className="text-xs text-gray-500">Show alerts for important events</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={notifications}
                    onChange={(e) => {
                      setNotifications(e.target.checked);
                      setIsDirty(true);
                    }}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Auto-save Settings</span>
                  <p className="text-xs text-gray-500">Automatically save your preferences</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={autoSave}
                    onChange={(e) => setAutoSave(e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
            </div>
            
            <div className="border-t pt-4 mt-4">
              <h3 className="font-bold mb-3">Reset Draft</h3>
              <p className="text-sm text-gray-600 mb-3">
                This will reset the entire draft to the beginning. All picks will be lost.
              </p>
              <button
                className={`px-4 py-2 rounded ${
                  showResetConfirm 
                    ? 'bg-red-600 hover:bg-red-700 text-white' 
                    : 'bg-gray-200 hover:bg-gray-300 text-gray-800'
                }`}
                onClick={handleResetDraft}
              >
                {showResetConfirm ? 'Confirm Reset' : 'Reset Draft'}
              </button>
              {showResetConfirm && (
                <button
                  className="ml-2 px-4 py-2 border border-gray-300 rounded hover:bg-gray-100"
                  onClick={() => setShowResetConfirm(false)}
                >
                  Cancel
                </button>
              )}
            </div>
          </div>
        )}
        
        {activeSection === 'appearance' && (
          <div>
            <h3 className="font-bold text-lg mb-4">Appearance Settings</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Theme</label>
              <select
                className="w-full p-2 border rounded"
                value={themeMode}
                onChange={(e) => {
                  setThemeMode(e.target.value);
                  setIsDirty(true);
                }}
              >
                <option value="default">Default</option>
                <option value="dark">Dark Mode</option>
                <option value="light">Light Mode</option>
                <option value="contrast">High Contrast</option>
                <option value="retro">Retro</option>
                <option value="modern">Modern</option>
              </select>
              <p className="mt-1 text-xs text-gray-500">
                Choose your preferred visual style
              </p>
            </div>
            
            <div className="grid grid-cols-3 gap-3 mb-6">
              <div 
                className={`p-4 border rounded-lg cursor-pointer ${themeMode === 'default' ? 'ring-2 ring-blue-500' : 'hover:bg-gray-50'}`}
                onClick={() => {
                  setThemeMode('default');
                  setIsDirty(true);
                }}
              >
                <div className="h-20 bg-gradient-to-r from-blue-500 to-blue-600 rounded mb-2"></div>
                <div className="text-center text-sm font-medium">Default</div>
              </div>
              
              <div 
                className={`p-4 border rounded-lg cursor-pointer ${themeMode === 'dark' ? 'ring-2 ring-blue-500' : 'hover:bg-gray-50'}`}
                onClick={() => {
                  setThemeMode('dark');
                  setIsDirty(true);
                }}
              >
                <div className="h-20 bg-gradient-to-r from-gray-800 to-gray-900 rounded mb-2"></div>
                <div className="text-center text-sm font-medium">Dark Mode</div>
              </div>
              
              <div 
                className={`p-4 border rounded-lg cursor-pointer ${themeMode === 'light' ? 'ring-2 ring-blue-500' : 'hover:bg-gray-50'}`}
                onClick={() => {
                  setThemeMode('light');
                  setIsDirty(true);
                }}
              >
                <div className="h-20 bg-gradient-to-r from-gray-100 to-white rounded mb-2"></div>
                <div className="text-center text-sm font-medium">Light Mode</div>
              </div>
            </div>
            
            <div className="border-t py-4">
              <h4 className="font-medium mb-2">Preview</h4>
              <div className={`p-4 ${
                themeMode === 'dark' ? 'bg-gray-800 text-white' : 
                themeMode === 'light' ? 'bg-white text-gray-900' :
                themeMode === 'contrast' ? 'bg-white text-black' :
                themeMode === 'retro' ? 'bg-amber-50 text-gray-900' :
                themeMode === 'modern' ? 'bg-slate-900 text-white' :
                'bg-gray-100 text-gray-900'
              } rounded-lg`}>
                <h5 className="font-bold mb-2">Theme Preview</h5>
                <p className="text-sm mb-2">This is how your theme will look across the application.</p>
                <div className="flex space-x-2 mb-2">
                  <button className={`px-3 py-1 ${
                    themeMode === 'dark' ? 'bg-blue-600' : 
                    themeMode === 'light' ? 'bg-blue-600' :
                    themeMode === 'contrast' ? 'bg-blue-700' :
                    themeMode === 'retro' ? 'bg-blue-800' :
                    themeMode === 'modern' ? 'bg-blue-500' :
                    'bg-blue-500'
                  } text-white rounded`}>
                    Primary Button
                  </button>
                  <button className={`px-3 py-1 ${
                    themeMode === 'dark' ? 'bg-gray-700 text-white' : 
                    themeMode === 'light' ? 'bg-gray-200 text-gray-800' :
                    themeMode === 'contrast' ? 'bg-gray-200 text-black' :
                    themeMode === 'retro' ? 'bg-amber-200 text-gray-900' :
                    themeMode === 'modern' ? 'bg-slate-700 text-white' :
                    'bg-gray-200 text-gray-800'
                  } rounded`}>
                    Secondary Button
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {activeSection === 'preferences' && (
          <div>
            <h3 className="font-bold text-lg mb-4">User Preferences</h3>
            
            <div className="space-y-4 mb-6">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Show Trade Values</span>
                  <p className="text-xs text-gray-500">Display pick value charts during trades</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={userPreferences.showTradeValues}
                    onChange={(e) => handlePreferenceChange('showTradeValues', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Show Prospect Grades</span>
                  <p className="text-xs text-gray-500">Display grades and analytics for prospects</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={userPreferences.showProspectGrades}
                    onChange={(e) => handlePreferenceChange('showProspectGrades', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Show Team Needs</span>
                  <p className="text-xs text-gray-500">Highlight team needs during drafting</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={userPreferences.showTeamNeeds}
                    onChange={(e) => handlePreferenceChange('showTeamNeeds', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Confirm Selections</span>
                  <p className="text-xs text-gray-500">Ask for confirmation before drafting</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={userPreferences.confirmSelections}
                    onChange={(e) => handlePreferenceChange('confirmSelections', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Auto-advance</span>
                  <p className="text-xs text-gray-500">Automatically advance to next pick</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    className="sr-only peer"
                    checked={userPreferences.autoAdvance}
                    onChange={(e) => handlePreferenceChange('autoAdvance', e.target.checked)}
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                </label>
              </div>
            </div>
            
            <div className="border-t pt-4 mt-4">
              <h3 className="font-bold mb-3">Import/Export Settings</h3>
              <div className="flex space-x-2">
                <button
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                  onClick={exportSettings}
                >
                  Export Settings
                </button>
                
                <label className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300 cursor-pointer">
                  Import Settings
                  <input
                    type="file"
                    accept=".json"
                    className="hidden"
                    onChange={importSettings}
                  />
                </label>
                
                <button
                  className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100"
                  onClick={resetSettings}
                >
                  Reset to Defaults
                </button>
              </div>
            </div>
          </div>
        )}
        
        {activeSection === 'multiplayer' && (
          <div>
            <h3 className="font-bold text-lg mb-4">Multiplayer Settings</h3>
            
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Draft Timer</label>
              <select
                className="w-full p-2 border rounded"
                value={multiplayerSettings.draftTimeout}
                onChange={(e) => handleMultiplayerSettingChange('draftTimeout', parseInt(e.target.value))}
              >
                <option value="60">1 Minute</option>
                <option value="120">2 Minutes</option>
                <option value="180">3 Minutes</option>
                <option value="300">5 Minutes</option>
              </select>
              <p className="mt-1 text-xs text-gray-500">
                Time each player has to make their draft selection
              </p>
            </div>
            
            <div className="space-y-4 mb-6">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-sm font-medium text-gray-700">Allow Trading</span>
                  <p className="text-xs text-gray-500">Enable player-to-player trades</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"