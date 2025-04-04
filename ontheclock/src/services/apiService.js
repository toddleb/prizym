import { teams } from '../data/teams';
import { prospects } from '../data/prospects';

/**
 * Handles data fetching and management for the NFL Draft Simulator
 * JavaScript implementation based on the Python NFLDataFetcher and NFLDataStore
 */
class DataService {
  constructor() {
    this.baseUrl = 'https://api.example.com/nfl/v1'; // Placeholder API URL
    this.apiKey = null;
    this.localStorage = window.localStorage;
    this.mockEnabled = true; // Use mock data when API isn't available
  }

  /**
   * Set API key for authenticated requests
   * @param {string} apiKey - The API key to use
   */
  setApiKey(apiKey) {
    this.apiKey = apiKey;
  }

  /**
   * Get authorization headers for API requests
   * @returns {Object} Headers object with authorization
   */
  getHeaders() {
    return this.apiKey 
      ? { 'Authorization': `Bearer ${this.apiKey}` }
      : {};
  }

  /**
   * Fetch all NFL teams data
   * @returns {Promise<Array>} Array of team objects
   */
  async getTeams() {
    try {
      if (!this.mockEnabled) {
        const response = await fetch(`${this.baseUrl}/teams`, {
          headers: this.getHeaders()
        });
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        return data.data;
      } else {
        // Return mock data from local file
        return teams;
      }
    } catch (error) {
      console.error('Error fetching teams:', error);
      // Fallback to cached data if available
      const cachedData = this.getCachedData('teams');
      if (cachedData) {
        return cachedData;
      }
      return teams; // Use mock data as final fallback
    }
  }

  /**
   * Fetch draft prospects for specified year
   * @param {number} year - Draft year
   * @returns {Promise<Array>} Array of prospect objects
   */
  async getDraftProspects(year = new Date().getFullYear()) {
    try {
      if (!this.mockEnabled) {
        const response = await fetch(`${this.baseUrl}/draft/prospects/${year}`, {
          headers: this.getHeaders()
        });
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        this.cacheData('prospects', data.data);
        return data.data;
      } else {
        // Return mock data from local file
        return prospects;
      }
    } catch (error) {
      console.error('Error fetching prospects:', error);
      // Fallback to cached data if available
      const cachedData = this.getCachedData('prospects');
      if (cachedData) {
        return cachedData;
      }
      return prospects; // Use mock data as final fallback
    }
  }

  /**
   * Fetch historical draft data for a range of years
   * @param {number} startYear - Starting year (inclusive)
   * @param {number} endYear - Ending year (inclusive)
   * @returns {Promise<Array>} Array of historical draft picks
   */
  async getHistoricalDrafts(startYear, endYear) {
    try {
      if (!this.mockEnabled) {
        let allDrafts = [];
        
        for (let year = startYear; year <= endYear; year++) {
          const response = await fetch(`${this.baseUrl}/draft/${year}`, {
            headers: this.getHeaders()
          });
          
          if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
          }
          
          const data = await response.json();
          allDrafts = [...allDrafts, ...data.data];
        }
        
        this.cacheData('historicalDrafts', allDrafts);
        return allDrafts;
      } else {
        // Generate mock historical data
        return this.generateMockHistoricalDrafts(startYear, endYear);
      }
    } catch (error) {
      console.error('Error fetching historical drafts:', error);
      // Fallback to cached data if available
      const cachedData = this.getCachedData('historicalDrafts');
      if (cachedData) {
        return cachedData;
      }
      // Use mock data as final fallback
      return this.generateMockHistoricalDrafts(startYear, endYear);
    }
  }

  /**
   * Generate mock historical draft data
   * @param {number} startYear - Starting year
   * @param {number} endYear - Ending year
   * @returns {Array} Array of mock historical draft picks
   */
  generateMockHistoricalDrafts(startYear, endYear) {
    const mockDrafts = [];
    const positions = ['QB', 'RB', 'WR', 'TE', 'OT', 'OG', 'C', 'DT', 'EDGE', 'LB', 'CB', 'S'];
    const colleges = [
      'Alabama', 'Ohio State', 'Georgia', 'Clemson', 'LSU', 'Michigan', 
      'Oklahoma', 'Notre Dame', 'Florida', 'Penn State', 'Texas', 'Oregon'
    ];
    
    // Generate random names
    const generateName = () => {
      const firstNames = ['Michael', 'Chris', 'John', 'David', 'James', 'Robert', 'William', 'Joseph', 'Thomas', 'Anthony'];
      const lastNames = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor'];
      
      return `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${lastNames[Math.floor(Math.random() * lastNames.length)]}`;
    };
    
    // For each year
    for (let year = startYear; year <= endYear; year++) {
      // For each round
      for (let round = 1; round <= 7; round++) {
        // For each pick in the round
        for (let pick = 1; pick <= 32; pick++) {
          const teamIndex = (pick - 1) % teams.length;
          
          mockDrafts.push({
            year,
            round,
            pick_number: pick,
            team_id: teams[teamIndex].id,
            team_name: teams[teamIndex].name,
            prospect_id: `mock_${year}_${round}_${pick}`,
            prospect_name: generateName(),
            position: positions[Math.floor(Math.random() * positions.length)],
            college: colleges[Math.floor(Math.random() * colleges.length)]
          });
        }
      }
    }
    
    return mockDrafts;
  }

  /**
   * Cache data in localStorage with timestamp
   * @param {string} key - Cache key
   * @param {Array|Object} data - Data to cache
   */
  cacheData(key, data) {
    try {
      const cacheItem = {
        data,
        timestamp: new Date().getTime()
      };
      
      this.localStorage.setItem(`nfl_draft_${key}`, JSON.stringify(cacheItem));
    } catch (error) {
      console.error('Error caching data:', error);
    }
  }

  /**
   * Get cached data if still valid (less than 24 hours old)
   * @param {string} key - Cache key
   * @returns {Array|Object|null} Cached data or null if invalid/expired
   */
  getCachedData(key) {
    try {
      const cacheItem = JSON.parse(this.localStorage.getItem(`nfl_draft_${key}`));
      
      if (!cacheItem) return null;
      
      const now = new Date().getTime();
      const cacheAge = now - cacheItem.timestamp;
      const cacheValidHours = 24; // Cache valid for 24 hours
      
      if (cacheAge < cacheValidHours * 60 * 60 * 1000) {
        return cacheItem.data;
      }
      
      return null;
    } catch (error) {
      console.error('Error retrieving cached data:', error);
      return null;
    }
  }

  /**
   * Save draft results to localStorage
   * @param {Array} draftHistory - Array of draft picks
   */
  saveDraftHistory(draftHistory) {
    try {
      this.localStorage.setItem('nfl_draft_history', JSON.stringify(draftHistory));
    } catch (error) {
      console.error('Error saving draft history:', error);
    }
  }

  /**
   * Load saved draft history from localStorage
   * @returns {Array|null} Saved draft history or null if not found
   */
  loadDraftHistory() {
    try {
      const savedHistory = this.localStorage.getItem('nfl_draft_history');
      return savedHistory ? JSON.parse(savedHistory) : null;
    } catch (error) {
      console.error('Error loading draft history:', error);
      return null;
    }
  }

  /**
   * Export draft history to JSON file for download
   * @param {Array} draftHistory - Draft history to export
   */
  exportDraftHistory(draftHistory) {
    try {
      const dataStr = JSON.stringify(draftHistory, null, 2);
      const dataUri = `data:application/json;charset=utf-8,${encodeURIComponent(dataStr)}`;
      
      const exportFileDefaultName = `nfl_draft_${new Date().toISOString().slice(0, 10)}.json`;
      
      const linkElement = document.createElement('a');
      linkElement.setAttribute('href', dataUri);
      linkElement.setAttribute('download', exportFileDefaultName);
      linkElement.click();
    } catch (error) {
      console.error('Error exporting draft history:', error);
    }
  }
}

// Create a single instance to use throughout the app
const dataService = new DataService();

export default dataService;