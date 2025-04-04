// Updated Multiplayer Draft Module for NFL Draft App
// Converted to use modern JavaScript and adapted for React integration

import { teams } from '../data/teams';

/**
 * MultiplayerService manages draft lobbies, user interactions, and real-time draft state
 * for the multiplayer functionality of the NFL Draft Simulator.
 */
class MultiplayerService {
  constructor(options = {}) {
    this.options = {
      maxPlayers: 32, // Maximum number of human players
      draftTimeout: 120, // Seconds per pick
      autoAssignTeams: true, // Automatically assign teams to players
      fillWithAI: true, // Fill remaining teams with AI
      ...options
    };
    
    // State
    this.lobbies = {}; // All active draft lobbies
    this.connections = {}; // User connections by userId
    this.callbacks = {
      onLobbyUpdate: null,
      onPlayerJoin: null,
      onPlayerLeave: null,
      onPickMade: null,
      onTradeOffer: null,
      onTradeAccepted: null,
      onChatMessage: null,
      onError: null
    };
    
    // Connection status - in a real implementation, this would connect to a WebSocket or similar
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.currentLobby = null;
    
    // In a real implementation, this would connect to a proper backend
    // For this simulator, we're using local state with simulated network delays
  }
  
  /**
   * Initialize the connection to the multiplayer server
   * @param {string} userId - User identifier
   * @param {string} username - Display name
   * @returns {Promise<boolean>} Connection success
   */
  async connect(userId, username) {
    // Simulating connection setup with a delay
    this.userId = userId;
    this.username = username;
    
    try {
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      this.isConnected = true;
      this.reconnectAttempts = 0;
      console.log(`[Multiplayer] Connected as ${username} (${userId})`);
      return true;
    } catch (err) {
      this._handleError('Connection failed', err);
      return false;
    }
  }
  
  /**
   * Disconnect from the multiplayer server
   */
  disconnect() {
    // Leave any active lobbies first
    if (this.currentLobby) {
      this.leaveLobby();
    }
    
    this.isConnected = false;
    this.userId = null;
    this.username = null;
    console.log('[Multiplayer] Disconnected');
  }
  
  /**
   * Set a callback function to handle multiplayer events
   * @param {string} name - Callback name
   * @param {Function} callback - Callback function
   * @returns {boolean} Success
   */
  setCallback(name, callback) {
    if (typeof callback === 'function' && this.callbacks.hasOwnProperty(name)) {
      this.callbacks[name] = callback;
      return true;
    }
    return false;
  }
  
  /**
   * Create a new draft lobby
   * @param {Object} options - Lobby options
   * @returns {Object|null} Lobby object or null if creation failed
   */
  createLobby(options = {}) {
    if (!this.isConnected) {
      this._handleError('Cannot create lobby', 'Not connected');
      return null;
    }
    
    const lobbyId = this._generateLobbyId();
    const createdAt = new Date();
    
    const lobbyOptions = {
      name: options.name || `${this.username}'s Draft`,
      draftType: options.draftType || 'standard',
      maxPlayers: options.maxPlayers || this.options.maxPlayers,
      draftTimeout: options.draftTimeout || this.options.draftTimeout,
      password: options.password || null,
      isPrivate: !!options.password,
      autoStart: options.hasOwnProperty('autoStart') ? options.autoStart : false,
      fillWithAI: options.hasOwnProperty('fillWithAI') ? options.fillWithAI : this.options.fillWithAI,
      teamsPerPlayer: options.teamsPerPlayer || 1
    };
    
    const lobby = {
      id: lobbyId,
      createdAt,
      status: 'waiting', // waiting, starting, active, completed
      options: lobbyOptions,
      creator: {
        userId: this.userId,
        username: this.username
      },
      players: [{
        userId: this.userId,
        username: this.username,
        isReady: false,
        team: null,
        isActive: true,
        isHost: true,
        joinedAt: createdAt
      }],
      teams: [], // Will be filled with team assignments
      draftState: null, // Will be initialized when draft starts
      chat: []
    };
    
    this.lobbies[lobbyId] = lobby;
    this.currentLobby = lobbyId;
    
    console.log(`[Multiplayer] Created lobby ${lobbyId}`);
    this._notifyLobbyUpdate(lobby);
    
    return lobby;
  }
  
  /**
   * Join an existing lobby
   * @param {string} lobbyId - Lobby identifier
   * @param {string|null} password - Lobby password for private lobbies
   * @returns {boolean} Join success
   */
  joinLobby(lobbyId, password = null) {
    if (!this.isConnected) {
      this._handleError('Cannot join lobby', 'Not connected');
      return false;
    }
    
    const lobby = this.lobbies[lobbyId];
    if (!lobby) {
      this._handleError('Cannot join lobby', 'Lobby not found');
      return false;
    }
    
    if (lobby.options.isPrivate && lobby.options.password !== password) {
      this._handleError('Cannot join lobby', 'Incorrect password');
      return false;
    }
    
    if (lobby.status !== 'waiting') {
      this._handleError('Cannot join lobby', 'Lobby is not accepting new players');
      return false;
    }
    
    if (lobby.players.length >= lobby.options.maxPlayers) {
      this._handleError('Cannot join lobby', 'Lobby is full');
      return false;
    }
    
    // Check if already in the lobby
    const existingPlayer = lobby.players.find(p => p.userId === this.userId);
    if (existingPlayer) {
      existingPlayer.isActive = true;
      this._notifyLobbyUpdate(lobby);
      return true;
    }
    
    // Add the player to the lobby
    lobby.players.push({
      userId: this.userId,
      username: this.username,
      isReady: false,
      team: null,
      isActive: true,
      isHost: false,
      joinedAt: new Date()
    });
    
    this.currentLobby = lobbyId;
    
    console.log(`[Multiplayer] Joined lobby ${lobbyId}`);
    this._notifyLobbyUpdate(lobby);
    this._notifyPlayerJoin(this.userId, this.username, lobby);
    
    return true;
  }
  
  /**
   * Leave the current lobby
   * @returns {boolean} Leave success
   */
  leaveLobby() {
    if (!this.currentLobby) {
      return false;
    }
    
    const lobby = this.lobbies[this.currentLobby];
    if (!lobby) {
      this.currentLobby = null;
      return false;
    }
    
    // Find the player in the lobby
    const playerIndex = lobby.players.findIndex(p => p.userId === this.userId);
    if (playerIndex === -1) {
      this.currentLobby = null;
      return false;
    }
    
    const isHost = lobby.players[playerIndex].isHost;
    
    // Remove the player
    lobby.players.splice(playerIndex, 1);
    
    // If the player was the host, assign a new host
    if (isHost && lobby.players.length > 0) {
      lobby.players[0].isHost = true;
    }
    
    // If no players left, remove the lobby
    if (lobby.players.length === 0) {
      delete this.lobbies[this.currentLobby];
    } else {
      this._notifyLobbyUpdate(lobby);
      this._notifyPlayerLeave(this.userId, this.username, lobby);
    }
    
    console.log(`[Multiplayer] Left lobby ${this.currentLobby}`);
    this.currentLobby = null;
    
    return true;
  }
  
  /**
   * Get all available public lobbies
   * @returns {Array} List of public lobbies
   */
  getPublicLobbies() {
    return Object.values(this.lobbies)
      .filter(lobby => !lobby.options.isPrivate && lobby.status === 'waiting')
      .map(lobby => ({
        id: lobby.id,
        name: lobby.options.name,
        creator: lobby.creator.username,
        playerCount: lobby.players.length,
        maxPlayers: lobby.options.maxPlayers,
        draftType: lobby.options.draftType,
        createdAt: lobby.createdAt
      }));
  }
  
  /**
   * Get details about the current lobby
   * @returns {Object|null} Lobby object or null if not in a lobby
   */
  getCurrentLobby() {
    if (!this.currentLobby) {
      return null;
    }
    
    return this.lobbies[this.currentLobby];
  }
  
  /**
   * Set player ready status in the lobby
   * @param {boolean} isReady - Ready state
   * @returns {boolean} Success
   */
  setReady(isReady = true) {
    if (!this.currentLobby) {
      return false;
    }
    
    const lobby = this.lobbies[this.currentLobby];
    if (!lobby) {
      return false;
    }
    
    const player = lobby.players.find(p => p.userId === this.userId);
    if (!player) {
      return false;
    }
    
    player.isReady = isReady;
    
    // Check if all players are ready to start
    this._checkAutoStart(lobby);
    
    this._notifyLobbyUpdate(lobby);
    
    return true;
  }
  
  /**
   * Select a team in the lobby
   * @param {number} teamId - Team identifier
   * @returns {boolean} Success
   */
  selectTeam(teamId) {
    if (!this.currentLobby) {
      return false;
    }
    
    const lobby = this.lobbies[this.currentLobby];
    if (!lobby || lobby.status !== 'waiting') {
      return false;
    }
    
    const player = lobby.players.find(p => p.userId === this.userId);
    if (!player) {
      return false;
    }
    
    // Check if team is already taken
    const isTeamTaken = lobby.players.some(p => 
      p.userId !== this.userId && p.team === teamId
    );
    
    if (isTeamTaken) {
      this._handleError('Cannot select team', 'Team already taken');
      return false;
    }
    
    player.team = teamId;
    this._notifyLobbyUpdate(lobby);
    
    return true;
  }
  
  /**
   * Send a chat message in the lobby
   * @param {string} message - Chat message
   * @returns {boolean} Success
   */
  sendChatMessage(message) {
    if (!this.currentLobby || !message.trim()) {
      return false;
    }
    
    const lobby = this.lobbies[this.currentLobby];
    if (!lobby) {
      return false;
    }
    
    const chatMessage = {
      userId: this.userId,
      username: this.username,
      message: message.trim(),
      timestamp: new Date()
    };
    
    lobby.chat.push(chatMessage);
    
    // Keep only the last 100 messages
    if (lobby.chat.length > 100) {
      lobby.chat = lobby.chat.slice(-100);
    }
    
    if (this.callbacks.onChatMessage) {
      this.callbacks.onChatMessage(chatMessage, lobby);
    }
    
    return true;
  }
  
  /**
   * Start the draft if player is the host
   * @returns {boolean} Success
   */
  startDraft() {
    if (!this.currentLobby) {
      return false;
    }
    
    const lobby = this.lobbies[this.currentLobby];
    if (!lobby || lobby.status !== 'waiting') {
      return false;
    }
    
    const player = lobby.players.find(p => p.userId === this.userId);
    if (!player || !player.isHost) {
      this._handleError('Cannot start draft', 'Only the host can start the draft');
      return false;
    }
    
    // Assign teams to players who haven't selected one
    this._assignRemainingTeams(lobby);
    
    // Initialize the draft state
    lobby.status = 'starting';
    this._initializeDraftState(lobby);
    
    // After a short delay, change status to active
    setTimeout(() => {
      lobby.status = 'active';
      this._notifyLobbyUpdate(lobby);
      
      // Start the first pick timer
      this._startPickTimer(lobby);
    }, 3000);
    
    this._notifyLobbyUpdate(lobby);
    
    return true;
  }
  
  /**
   * Make a draft pick
   * @param {number} prospectId - Prospect identifier
   * @returns {boolean} Success
   */
  makePick(prospectId) {
    if (!this.currentLobby) {
      return false;
    }
    
    const lobby = this.lobbies[this.currentLobby];
    if (!lobby || lobby.status !== 'active' || !lobby.draftState) {
      return false;
    }
    
    const draftState = lobby.draftState;
    const currentPick = draftState.currentPick;
    
    // Check if it's the user's turn
    const currentTeam = draftState.pickOrder[currentPick - 1].teamId;
    const player = lobby.players.find(p => p.team === currentTeam && p.userId === this.userId);
    
    if (!player) {
      this._handleError('Cannot make pick', 'Not your turn');
      return false;
    }
    
    // Check if the prospect is still available
    if (!draftState.availableProspects.includes(prospectId)) {
      this._handleError('Cannot make pick', 'Prospect already drafted');
      return false;
    }
    
    // Make the pick
    draftState.picks.push({
      pickNumber: currentPick,
      teamId: currentTeam,
      prospectId,
      userId: this.userId,
      timestamp: new Date()
    });
    
    // Remove prospect from available list
    draftState.availableProspects = draftState.availableProspects.filter(id => id !== prospectId);
    
    // Move to the next pick
    draftState.currentPick++;
    
    // Check if draft is complete
    if (draftState.currentPick > draftState.pickOrder.length) {
      this._completeDraft(lobby);
    } else {
      // Start timer for the next pick
      this._startPickTimer(lobby);
    }
    
    // Notify all players
    this._notifyLobbyUpdate(lobby);
    if (this.callbacks.onPickMade) {
      this.callbacks.onPickMade({
        pickNumber: draftState.currentPick - 1,
        teamId,
        prospectId,
        isAIPick: true
      }, lobby);
    }
  }
  
  /**
   * Complete the draft
   * @private
   * @param {Object} lobby - Lobby object
   */
  _completeDraft(lobby) {
    lobby.status = 'completed';
    clearTimeout(this.pickTimeout);
    
    // Calculate draft grades (simplified)
    const grades = {};
    lobby.players.forEach(player => {
      if (player.team) {
        grades[player.team] = this._calculateDraftGrade(lobby, player.team);
      }
    });
    
    lobby.draftState.grades = grades;
    this._notifyLobbyUpdate(lobby);
  }
  
  /**
   * Calculate a draft grade for a team (simplified)
   * @private
   * @param {Object} lobby - Lobby object
   * @param {number} teamId - Team identifier
   * @returns {Object} Draft grade
   */
  _calculateDraftGrade(lobby, teamId) {
    const teamPicks = lobby.draftState.picks.filter(pick => pick.teamId === teamId);
    const team = teams.find(t => t.id === teamId);
    
    // Get the team's needs
    const teamNeeds = team ? [...team.needs] : [];
    
    // Calculate position breakdown
    const positionCounts = {};
    let totalPositionScore = 0;
    let needsAddressed = 0;
    
    // Check if each pick addressed a need
    teamPicks.forEach(pick => {
      // In a real implementation, we would get the prospect's position from a database
      // For now, we'll generate a random position
      const pickRound = Math.floor(pick.pickNumber / 32) + 1;
      const randomPositionIndex = (pick.prospectId + teamId) % teamNeeds.length;
      const position = teamNeeds[randomPositionIndex];
      
      // Count positions
      positionCounts[position] = (positionCounts[position] || 0) + 1;
      
      // Award points for addressing needs
      if (teamNeeds.includes(position)) {
        // Prioritize addressing top needs early
        const needIndex = teamNeeds.indexOf(position);
        const needImportance = 1 - (needIndex / teamNeeds.length);
        const roundValue = 1 / pickRound; // Earlier rounds are worth more
        
        totalPositionScore += needImportance * roundValue * 10;
        
        // Mark this need as addressed (remove from high priority)
        if (needIndex < 3) {
          teamNeeds.splice(needIndex, 1);
          needsAddressed++;
        }
      }
    });
    
    // Value-based scoring (mock calculation)
    let valueScore = 70 + Math.min(20, teamPicks.length * 2);
    
    // Needs-based adjustment
    const needsScore = needsAddressed / 3 * 30; // Up to 30 points for addressing all top 3 needs
    
    // Calculate final grade
    const finalScore = Math.min(99, Math.round((valueScore * 0.7) + (needsScore * 0.3)));
    
    // Convert numerical grade to letter grade
    let letterGrade;
    if (finalScore >= 90) letterGrade = 'A';
    else if (finalScore >= 80) letterGrade = 'B';
    else if (finalScore >= 70) letterGrade = 'C';
    else if (finalScore >= 60) letterGrade = 'D';
    else letterGrade = 'F';
    
    // Add plus/minus modifiers
    const modScore = finalScore % 10;
    if (finalScore >= 60) { // Only add modifiers to passing grades
      if (modScore >= 7 && finalScore < 90) letterGrade += '+';
      else if (modScore <= 2) letterGrade += '-';
    }
    
    return {
      teamId,
      teamName: team ? team.name : `Team ${teamId}`,
      pickCount: teamPicks.length,
      value: finalScore,
      grade: letterGrade,
      needsAddressed,
      positionBreakdown: positionCounts,
      description: this._generateGradeDescription(letterGrade, teamPicks.length, needsAddressed)
    };
  }
  
  /**
   * Generate a description for a team's draft grade
   * @private
   * @param {string} grade - Letter grade
   * @param {number} pickCount - Number of picks
   * @param {number} needsAddressed - Number of needs addressed
   * @returns {string} Draft grade description
   */
  _generateGradeDescription(grade, pickCount, needsAddressed) {
    // Base description by grade
    let description;
    if (grade.startsWith('A')) {
      description = "Outstanding draft with excellent value and need fulfillment. ";
    } else if (grade.startsWith('B')) {
      description = "Solid draft that addressed key needs with good value picks. ";
    } else if (grade.startsWith('C')) {
      description = "Average draft with some good picks but missed opportunities. ";
    } else if (grade.startsWith('D')) {
      description = "Below average draft that failed to maximize value or address needs. ";
    } else {
      description = "Poor draft with questionable decisions and missed value. ";
    }
    
    // Add details about pick quantity
    if (pickCount >= 10) {
      description += "Accumulated an impressive number of selections. ";
    } else if (pickCount >= 7) {
      description += "Made a full complement of draft choices. ";
    } else if (pickCount <= 4) {
      description += "Limited number of selections reduced overall impact. ";
    }
    
    // Add details about needs
    if (needsAddressed >= 3) {
      description += "Successfully addressed all top positional needs.";
    } else if (needsAddressed >= 2) {
      description += "Addressed most critical team needs.";
    } else if (needsAddressed >= 1) {
      description += "Addressed some needs but left others unfilled.";
    } else {
      description += "Failed to address key positional needs.";
    }
    
    return description;
  }
  
  /**
   * Create a mock multiplayer draft for testing
   * @returns {Object} Lobby object
   */
  createMockDraft() {
    // Create a mock user if not connected
    if (!this.isConnected) {
      this.userId = 'user_mock';
      this.username = 'Mock User';
      this.isConnected = true;
    }
    
    // Create a lobby
    const lobby = this.createLobby({
      name: 'Mock Draft',
      maxPlayers: 32,
      fillWithAI: true
    });
    
    if (!lobby) return null;
    
    // Add AI players for each team
    teams.forEach(team => {
      if (team.id !== 1) { // Assuming user is team 1
        lobby.players.push({
          userId: `ai_${team.id}`,
          username: `AI ${team.abbreviation}`,
          isReady: true,
          team: team.id,
          isActive: true,
          isHost: false,
          isAI: true,
          joinedAt: new Date()
        });
      }
    });
    
    // Start the draft
    this.startDraft();
    
    return lobby;
  }
}

// Create and export a singleton instance
const multiplayerService = new MultiplayerService();
export default multiplayerService; available list
    draftState.availableProspects = draftState.availableProspects.filter(id => id !== prospectId);
    
    // Move to the next pick
    draftState.currentPick++;
    
    // Check if draft is complete
    if (draftState.currentPick > draftState.pickOrder.length) {
      this._completeDraft(lobby);
    } else {
      // Start timer for the next pick
      this._startPickTimer(lobby);
    }
    
    // Notify all players
    this._notifyLobbyUpdate(lobby);
    if (this.callbacks.onPickMade) {
      this.callbacks.onPickMade({
        pickNumber: currentPick,
        teamId: currentTeam,
        prospectId,
        userId: this.userId,
        username: this.username
      }, lobby);
    }
    
    return true;
  }
  
  /**
   * Make a trade offer to another team
   * @param {number} toTeamId - Team receiving the offer
   * @param {Array} receivingPicks - Picks received in the trade
   * @param {Array} givingPicks - Picks given in the trade
   * @returns {Object|boolean} Trade offer or false if failed
   */
  makeTradeOffer(toTeamId, receivingPicks, givingPicks) {
    if (!this.currentLobby) {
      return false;
    }
    
    const lobby = this.lobbies[this.currentLobby];
    if (!lobby || lobby.status !== 'active' || !lobby.draftState) {
      return false;
    }
    
    const player = lobby.players.find(p => p.userId === this.userId);
    if (!player || !player.team) {
      return false;
    }
    
    const fromTeamId = player.team;
    
    // Check if the toTeam exists and is controlled by a different player
    const toPlayer = lobby.players.find(p => p.team === toTeamId && p.userId !== this.userId);
    if (!toPlayer) {
      this._handleError('Cannot make trade offer', 'Invalid trade partner');
      return false;
    }
    
    // Validate the picks being traded
    const draftState = lobby.draftState;
    
    // Check that all receiving picks belong to the toTeam and are not used
    const isValidReceiving = receivingPicks.every(pickId => {
      const pick = draftState.pickOrder.find(p => p.id === pickId);
      return pick && pick.teamId === toTeamId && pick.pickNumber >= draftState.currentPick;
    });
    
    // Check that all giving picks belong to the fromTeam and are not used
    const isValidGiving = givingPicks.every(pickId => {
      const pick = draftState.pickOrder.find(p => p.id === pickId);
      return pick && pick.teamId === fromTeamId && pick.pickNumber >= draftState.currentPick;
    });
    
    if (!isValidReceiving || !isValidGiving) {
      this._handleError('Cannot make trade offer', 'Invalid picks in trade offer');
      return false;
    }
    
    // Create the trade offer
    const tradeOffer = {
      id: this._generateTradeId(),
      fromTeamId,
      toTeamId,
      fromUserId: this.userId,
      toUserId: toPlayer.userId,
      receivingPicks,
      givingPicks,
      status: 'pending', // pending, accepted, declined, expired
      createdAt: new Date(),
      expiresAt: new Date(Date.now() + 2 * 60 * 1000) // 2 minute expiration
    };
    
    // Add the offer to the draft state
    if (!draftState.tradeOffers) {
      draftState.tradeOffers = [];
    }
    
    draftState.tradeOffers.push(tradeOffer);
    
    // Notify players
    this._notifyLobbyUpdate(lobby);
    if (this.callbacks.onTradeOffer) {
      this.callbacks.onTradeOffer(tradeOffer, lobby);
    }
    
    return tradeOffer;
  }
  
  /**
   * Respond to a trade offer
   * @param {string} tradeOfferId - Trade offer identifier
   * @param {boolean} accept - Whether to accept the offer
   * @returns {boolean} Success
   */
  respondToTradeOffer(tradeOfferId, accept) {
    if (!this.currentLobby) {
      return false;
    }
    
    const lobby = this.lobbies[this.currentLobby];
    if (!lobby || lobby.status !== 'active' || !lobby.draftState) {
      return false;
    }
    
    const draftState = lobby.draftState;
    if (!draftState.tradeOffers) {
      return false;
    }
    
    // Find the trade offer
    const tradeOfferIndex = draftState.tradeOffers.findIndex(
      offer => offer.id === tradeOfferId && offer.toUserId === this.userId && offer.status === 'pending'
    );
    
    if (tradeOfferIndex === -1) {
      this._handleError('Cannot respond to trade offer', 'Trade offer not found or not for you');
      return false;
    }
    
    const tradeOffer = draftState.tradeOffers[tradeOfferIndex];
    
    // Update the offer status
    tradeOffer.status = accept ? 'accepted' : 'declined';
    tradeOffer.respondedAt = new Date();
    
    // If accepted, execute the trade
    if (accept) {
      // Update team ownership for the picks
      tradeOffer.receivingPicks.forEach(pickId => {
        const pick = draftState.pickOrder.find(p => p.id === pickId);
        if (pick) {
          pick.teamId = tradeOffer.fromTeamId;
          pick.originalTeamId = pick.originalTeamId || tradeOffer.toTeamId; // Track original team
        }
      });
      
      tradeOffer.givingPicks.forEach(pickId => {
        const pick = draftState.pickOrder.find(p => p.id === pickId);
        if (pick) {
          pick.teamId = tradeOffer.toTeamId;
          pick.originalTeamId = pick.originalTeamId || tradeOffer.fromTeamId; // Track original team
        }
      });
      
      // Notify players of the accepted trade
      if (this.callbacks.onTradeAccepted) {
        this.callbacks.onTradeAccepted(tradeOffer, lobby);
      }
    }
    
    this._notifyLobbyUpdate(lobby);
    
    return true;
  }
  
  // Private helper methods
  
  /**
   * Generate a random lobby ID
   * @private
   * @returns {string} Lobby ID
   */
  _generateLobbyId() {
    return `draft_${Math.random().toString(36).substring(2, 10)}`;
  }
  
  /**
   * Generate a random trade ID
   * @private
   * @returns {string} Trade ID
   */
  _generateTradeId() {
    return `trade_${Math.random().toString(36).substring(2, 10)}`;
  }
  
  /**
   * Handle errors
   * @private
   * @param {string} message - Error message
   * @param {*} error - Error object or details
   */
  _handleError(message, error) {
    console.error(`[Multiplayer] ${message}:`, error);
    
    if (this.callbacks.onError) {
      this.callbacks.onError(message, error);
    }
  }
  
  /**
   * Notify lobby update
   * @private
   * @param {Object} lobby - Lobby object
   */
  _notifyLobbyUpdate(lobby) {
    if (this.callbacks.onLobbyUpdate) {
      this.callbacks.onLobbyUpdate(lobby);
    }
  }
  
  /**
   * Notify player join
   * @private
   * @param {string} userId - User identifier
   * @param {string} username - User display name
   * @param {Object} lobby - Lobby object
   */
  _notifyPlayerJoin(userId, username, lobby) {
    if (this.callbacks.onPlayerJoin) {
      this.callbacks.onPlayerJoin({ userId, username }, lobby);
    }
  }
  
  /**
   * Notify player leave
   * @private
   * @param {string} userId - User identifier
   * @param {string} username - User display name
   * @param {Object} lobby - Lobby object
   */
  _notifyPlayerLeave(userId, username, lobby) {
    if (this.callbacks.onPlayerLeave) {
      this.callbacks.onPlayerLeave({ userId, username }, lobby);
    }
  }
  
  /**
   * Check if we should auto-start the draft
   * @private
   * @param {Object} lobby - Lobby object
   */
  _checkAutoStart(lobby) {
    if (lobby.options.autoStart && lobby.players.every(p => p.isReady)) {
      // Everyone is ready, start the draft after a brief delay
      setTimeout(() => this.startDraft(), 2000);
    }
  }
  
  /**
   * Assign teams to players who haven't selected one
   * @private
   * @param {Object} lobby - Lobby object
   */
  _assignRemainingTeams(lobby) {
    if (!lobby.options.autoAssignTeams) {
      return;
    }
    
    // Get all team IDs
    const allTeamIds = teams.map(team => team.id);
    
    // Get already assigned teams
    const assignedTeams = lobby.players
      .filter(p => p.team !== null)
      .map(p => p.team);
    
    // Get players without teams
    const playersWithoutTeams = lobby.players.filter(p => p.team === null);
    
    // Get available teams
    const availableTeams = allTeamIds.filter(id => !assignedTeams.includes(id));
    
    // Randomly assign teams
    playersWithoutTeams.forEach(player => {
      if (availableTeams.length > 0) {
        const randomIndex = Math.floor(Math.random() * availableTeams.length);
        player.team = availableTeams[randomIndex];
        availableTeams.splice(randomIndex, 1);
      }
    });
    
    // If we should fill with AI, create AI players for remaining teams
    if (lobby.options.fillWithAI && availableTeams.length > 0) {
      availableTeams.forEach(teamId => {
        const team = teams.find(t => t.id === teamId);
        lobby.players.push({
          userId: `ai_${teamId}`,
          username: `AI ${team ? team.abbreviation : teamId}`,
          isReady: true,
          team: teamId,
          isActive: true,
          isHost: false,
          isAI: true,
          joinedAt: new Date()
        });
      });
    }
  }
  
  /**
   * Initialize the draft state
   * @private
   * @param {Object} lobby - Lobby object
   */
  _initializeDraftState(lobby) {
    const pickOrder = [];
    const totalRounds = lobby.options.draftType === 'firstRound' ? 1 : 
                        lobby.options.draftType === 'threeRounds' ? 3 : 7;
    
    // Generate the pick order
    for (let round = 1; round <= totalRounds; round++) {
      // Get teams in draft order
      const teamsInOrder = lobby.players
        .filter(p => p.team !== null)
        .map(p => p.team)
        .sort((a, b) => {
          // Sort by team.picks[0] if available
          const teamA = teams.find(t => t.id === a);
          const teamB = teams.find(t => t.id === b);
          if (teamA && teamB && teamA.picks && teamB.picks) {
            return teamA.picks[0] - teamB.picks[0];
          }
          return a - b;
        });
      
      teamsInOrder.forEach((teamId, index) => {
        pickOrder.push({
          id: `pick_${round}_${index + 1}`,
          round,
          pickNumber: (round - 1) * teamsInOrder.length + index + 1,
          teamId,
          originalTeamId: teamId
        });
      });
    }
    
    // Get available prospects
    const availableProspects = [];
    
    // In a real implementation, this would come from the prospect database
    // For now, we'll use the IDs from 1 to the number of total picks needed
    const totalPicks = pickOrder.length;
    for (let i = 1; i <= Math.max(300, totalPicks * 1.5); i++) {
      availableProspects.push(i);
    }
    
    lobby.draftState = {
      currentPick: 1,
      pickOrder,
      picks: [],
      availableProspects,
      tradeOffers: [],
      timerEndTime: null
    };
  }
  
  /**
   * Start the timer for the current pick
   * @private
   * @param {Object} lobby - Lobby object
   */
  _startPickTimer(lobby) {
    const draftState = lobby.draftState;
    const currentPick = draftState.currentPick;
    
    if (currentPick > draftState.pickOrder.length) {
      this._completeDraft(lobby);
      return;
    }
    
    // Set the timer end time
    draftState.timerEndTime = new Date(Date.now() + lobby.options.draftTimeout * 1000);
    
    // Check if the current team is controlled by AI
    const currentTeam = draftState.pickOrder[currentPick - 1].teamId;
    const isAITeam = lobby.players.some(p => p.team === currentTeam && p.isAI);
    
    if (isAITeam) {
      // AI makes a pick after a short delay
      setTimeout(() => {
        this._makeAIPick(lobby, currentTeam);
      }, Math.random() * 5000 + 2000); // 2-7 second delay
    } else {
      // Set a timeout for the human player
      clearTimeout(this.pickTimeout);
      this.pickTimeout = setTimeout(() => {
        // Auto-pick when timer expires
        if (lobby.draftState && lobby.draftState.currentPick === currentPick) {
          this._makeAIPick(lobby, currentTeam);
        }
      }, lobby.options.draftTimeout * 1000);
    }
    
    this._notifyLobbyUpdate(lobby);
  }
  
  /**
   * Make an AI pick
   * @private
   * @param {Object} lobby - Lobby object
   * @param {number} teamId - Team making the pick
   */
  _makeAIPick(lobby, teamId) {
    const draftState = lobby.draftState;
    
    if (draftState.availableProspects.length === 0) {
      console.error("[Multiplayer] No available prospects for AI pick");
      draftState.currentPick++;
      this._startPickTimer(lobby);
      return;
    }
    
    // Pick a random prospect from available ones
    const randomIndex = Math.floor(Math.random() * draftState.availableProspects.length);
    const prospectId = draftState.availableProspects[randomIndex];
    
    // Record the pick
    draftState.picks.push({
      pickNumber: draftState.currentPick,
      teamId,
      prospectId,
      userId: `ai_${teamId}`,
      isAIPick: true,
      timestamp: new Date()
    });
    
    // Remove prospect from