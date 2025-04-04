// DraftEngine.js - Core simulation logic for the NFL Draft app

// Class for handling the draft logic, team behaviors, and trade calculations
class DraftEngine {
  constructor(teams, prospects, settings = {}) {
    this.teams = teams;
    this.prospects = prospects;
    this.settings = {
      draftType: 'standard',
      tradesEnabled: true,
      tradeFrequency: 'realistic',
      autoPickEnabled: true,
      pickTimeSeconds: 60,
      ...settings
    };
    
    // Initialize the draft state
    this.currentRound = 1;
    this.currentPick = 1;
    this.activeTeamIndex = 0;
    this.draftHistory = [];
    this.remainingProspects = [...prospects];
    this.draftOrder = this.generateDraftOrder();
    this.tradeOffers = [];
    
    // Draft value chart (similar to Jimmy Johnson's)
    this.pickValueChart = {
      1: 3000, 2: 2600, 3: 2200, 4: 1800, 5: 1700, 6: 1600, 7: 1500, 8: 1400, 9: 1350, 10: 1300,
      11: 1250, 12: 1200, 13: 1150, 14: 1100, 15: 1050, 16: 1000, 17: 950, 18: 900, 19: 875, 20: 850,
      // ...more values for all 260+ picks
    };
    
    // Set up pick timer
    this.timeRemaining = this.settings.pickTimeSeconds;
    this.timerActive = false;
    this.onTimerTick = null;
    this.onTimerExpired = null;
  }
  
  // Generate the draft order based on team records/draft positions
  generateDraftOrder() {
    const order = [];
    const totalRounds = this.getDraftRoundCount();
    
    // For each round, add the teams in draft order
    for (let round = 1; round <= totalRounds; round++) {
      const roundPicks = this.teams.map((team, index) => ({
        round,
        pickNumber: (round - 1) * this.teams.length + index + 1,
        teamId: team.id,
        originalTeamId: team.id, // Track original team for traded picks
        isUsed: false,
        prospectId: null
      }));
      
      order.push(...roundPicks);
    }
    
    return order;
  }
  
  // Get the number of rounds based on draft type setting
  getDraftRoundCount() {
    switch (this.settings.draftType) {
      case 'firstRound': return 1;
      case 'threeRounds': return 3;
      case 'custom': return this.settings.customRoundCount || 7;
      case 'standard':
      default: return 7;
    }
  }
  
  // Get the current active team
  getActiveTeam() {
    return this.teams[this.activeTeamIndex];
  }
  
  // Get the current draft pick information
  getCurrentPick() {
    const currentPickIndex = this.draftHistory.length;
    return this.draftOrder[currentPickIndex];
  }
  
  // Make a draft selection
  makePick(prospectId, teamId = null) {
    // Default to active team if not specified
    const draftingTeamId = teamId || this.getActiveTeam().id;
    const prospect = this.remainingProspects.find(p => p.id === prospectId);
    
    if (!prospect) {
      throw new Error("Prospect not found or already drafted");
    }
    
    // Get current pick and update it
    const currentPickIndex = this.draftHistory.length;
    const currentPick = {...this.draftOrder[currentPickIndex]};
    
    // If this is a traded pick, the teamId might be different from the original
    currentPick.teamId = draftingTeamId;
    currentPick.isUsed = true;
    currentPick.prospectId = prospectId;
    
    // Update the draft order
    this.draftOrder[currentPickIndex] = currentPick;
    
    // Add to draft history
    this.draftHistory.push({
      round: currentPick.round,
      pick: currentPick.pickNumber,
      teamId: draftingTeamId,
      prospectId,
      timestamp: new Date()
    });
    
    // Remove prospect from available list
    this.remainingProspects = this.remainingProspects.filter(p => p.id !== prospectId);
    
    // Move to the next pick
    this.advancePick();
    
    return {
      success: true,
      pick: currentPick,
      prospect,
      team: this.teams.find(t => t.id === draftingTeamId)
    };
  }
  
  // Advance to the next pick
  advancePick() {
    // If we've reached the end of the draft, finish
    if (this.draftHistory.length >= this.draftOrder.length) {
      this.endDraft();
      return;
    }
    
    // Update round and pick counters
    const nextPick = this.draftOrder[this.draftHistory.length];
    this.currentRound = nextPick.round;
    this.currentPick = nextPick.pickNumber;
    
    // Find the team with the next pick (accounting for trades)
    this.activeTeamIndex = this.teams.findIndex(team => team.id === nextPick.teamId);
    
    // Reset the pick timer
    this.resetTimer();
    
    // Auto-pick for AI teams if enabled
    if (this.settings.autoPickEnabled && !this.getActiveTeam().isHuman) {
      this.makeAIPick();
    }
    
    // Generate AI trade offers
    if (this.settings.tradesEnabled) {
      this.generateTradeOffers();
    }
    
    return nextPick;
  }
  
  // AI makes a pick based on team needs and best player available
  makeAIPick() {
    const team = this.getActiveTeam();
    const prospect = this.getBestProspectForTeam(team);
    
    // Add some delay to simulate thinking
    setTimeout(() => {
      this.makePick(prospect.id, team.id);
    }, Math.random() * 3000 + 1000); // 1-4 second delay
    
    return prospect;
  }
  
  // Find the best prospect for a team based on needs and value
  getBestProspectForTeam(team) {
    // Get team needs
    const teamNeeds = this.getTeamNeeds(team.id);
    
    // Score each prospect based on need and value
    const scoredProspects = this.remainingProspects.map(prospect => {
      // Base value is the prospect's grade
      let score = prospect.grade;
      
      // Check if position is a need
      const needForPosition = teamNeeds.find(need => need.position === prospect.position);
      if (needForPosition) {
        // Boost score based on need priority
        switch (needForPosition.priority) {
          case 'High': score *= 1.3; break;
          case 'Medium': score *= 1.15; break;
          case 'Low': score *= 1.05; break;
        }
      }
      
      return { prospect, score };
    });
    
    // Sort by score and return the best prospect
    scoredProspects.sort((a, b) => b.score - a.score);
    return scoredProspects[0].prospect;
  }
  
  // Get team needs (could be more sophisticated in a real app)
  getTeamNeeds(teamId) {
    const team = this.teams.find(t => t.id === teamId);
    // In a real app, this would analyze the team's roster
    // For this example, we'll return dummy needs
    return [
      { position: 'QB', priority: 'High' },
      { position: 'WR', priority: 'Medium' },
      { position: 'OT', priority: 'Medium' },
      { position: 'CB', priority: 'Low' }
    ];
  }
  
  // Generate AI trade offers based on the current pick
  generateTradeOffers() {
    // Check if should generate offers based on frequency setting
    const shouldGenerateOffer = this.checkTradeFrequency();
    
    if (!shouldGenerateOffer) {
      return [];
    }
    
    const currentPick = this.getCurrentPick();
    const currentPickValue = this.getPickValue(currentPick.pickNumber);
    const tradesCount = Math.floor(Math.random() * 2) + 1; // 1-2 offers
    
    const offers = [];
    
    // Find teams that might want to trade up
    for (let i = 0; i < tradesCount; i++) {
      // Pick a random team (not the active team)
      const tradingTeamIndex = this.getRandomTradePartner();
      const tradingTeam = this.teams[tradingTeamIndex];
      
      // Generate the offer
      const offer = this.generateTradeOffer(tradingTeam, currentPick, currentPickValue);
      
      if (offer) {
        offers.push(offer);
      }
    }
    
    this.tradeOffers = offers;
    return offers;
  }
  
  // Check if a trade should be generated based on frequency setting
  checkTradeFrequency() {
    let chance = 0;
    
    switch (this.settings.tradeFrequency) {
      case 'rare': chance = 0.1; break;
      case 'occasional': chance = 0.2; break;
      case 'frequent': chance = 0.4; break;
      case 'realistic': 
        // More likely in early rounds
        chance = this.currentRound === 1 ? 0.3 : 
                this.currentRound === 2 ? 0.2 : 
                this.currentRound === 3 ? 0.15 : 0.05;
        
        // More likely for top 10 picks
        if (this.currentPick <= 10) {
          chance += 0.2;
        } else if (this.currentPick <= 32) {
          chance += 0.1;
        }
        break;
    }
    
    return Math.random() < chance;
  }
  
  // Get a random team as a trade partner (not the active team)
  getRandomTradePartner() {
    let validTeams = [];
    
    // Consider teams that might want to trade up
    for (let i = 0; i < this.teams.length; i++) {
      if (i !== this.activeTeamIndex) {
        // Teams later in the draft are more likely to want to trade up
        const weight = i > this.activeTeamIndex ? 2 : 1;
        for (let j = 0; j < weight; j++) {
          validTeams.push(i);
        }
      }
    }
    
    // If no valid teams, return null
    if (validTeams.length === 0) {
      return null;
    }
    
    // Select a random team from the weighted list
    const randomIndex = Math.floor(Math.random() * validTeams.length);
    return validTeams[randomIndex];
  }
  
  // Generate a trade offer from a team
  generateTradeOffer(tradingTeam, currentPick, currentPickValue) {
    // Find the trading team's picks
    const tradingTeamPicks = this.draftOrder.filter(pick => 
      pick.teamId === tradingTeam.id && 
      !pick.isUsed && 
      (pick.round === this.currentRound || pick.round === this.currentRound + 1)
    );
    
    if (tradingTeamPicks.length === 0) {
      return null; // Team has no viable picks to trade
    }
    
    // Sort picks by value (earlier picks are more valuable)
    tradingTeamPicks.sort((a, b) => this.getPickValue(a.pickNumber) - this.getPickValue(b.pickNumber));
    
    // Start with the earliest pick
    const basePick = tradingTeamPicks[0];
    const basePickValue = this.getPickValue(basePick.pickNumber);
    
    // If this pick is more valuable than current, no need for extra picks
    if (basePickValue >= currentPickValue) {
      return {
        fromTeamId: tradingTeam.id,
        toTeamId: this.getActiveTeam().id,
        fromTeamGets: [currentPick],
        toTeamGets: [basePick],
        timestamp: new Date()
      };
    }
    
    // Otherwise, need to add picks to make up the value
    let valueDifference = currentPickValue - basePickValue;
    const additionalPicks = [];
    
    for (let i = 1; i < tradingTeamPicks.length && valueDifference > 0; i++) {
      const pick = tradingTeamPicks[i];
      const pickValue = this.getPickValue(pick.pickNumber);
      
      if (pickValue <= valueDifference * 1.2) { // Allow some flexibility
        additionalPicks.push(pick);
        valueDifference -= pickValue;
      }
    }
    
    // If we couldn't make up the value, offer a future pick (simplified)
    if (valueDifference > 0 && Math.random() < 0.7) {
      additionalPicks.push({
        round: 1,
        pickNumber: 16, // Assume a mid-first round pick next year
        teamId: tradingTeam.id,
        isUsed: false,
        isFuture: true,
        futureYear: new Date().getFullYear() + 1
      });
    }
    
    // Create the offer
    return {
      fromTeamId: tradingTeam.id,
      toTeamId: this.getActiveTeam().id,
      fromTeamGets: [currentPick],
      toTeamGets: [basePick, ...additionalPicks],
      timestamp: new Date()
    };
  }
  
  // Accept a trade offer
  acceptTradeOffer(offerId) {
    const offer = this.tradeOffers.find(o => o.id === offerId);
    
    if (!offer) {
      throw new Error("Trade offer not found");
    }
    
    // Update picks in the draft order
    offer.fromTeamGets.forEach(pick => {
      const pickIndex = this.draftOrder.findIndex(p => 
        p.round === pick.round && 
        p.pickNumber === pick.pickNumber && 
        !p.isUsed
      );
      
      if (pickIndex >= 0) {
        this.draftOrder[pickIndex].teamId = offer.fromTeamId;
      }
    });
    
    offer.toTeamGets.forEach(pick => {
      // Skip future picks as they're not in the current draft
      if (pick.isFuture) return;
      
      const pickIndex = this.draftOrder.findIndex(p => 
        p.round === pick.round && 
        p.pickNumber === pick.pickNumber && 
        !p.isUsed
      );
      
      if (pickIndex >= 0) {
        this.draftOrder[pickIndex].teamId = offer.toTeamId;
      }
    });
    
    // Clear trade offers after accepting one
    this.tradeOffers = [];
    
    return { success: true, offer };
  }
  
  // Decline a trade offer
  declineTradeOffer(offerId) {
    this.tradeOffers = this.tradeOffers.filter(o => o.id !== offerId);
    return { success: true };
  }
  
  // Get the value of a pick based on the value chart
  getPickValue(pickNumber) {
    if (this.pickValueChart[pickNumber]) {
      return this.pickValueChart[pickNumber];
    }
    
    // For picks beyond the chart, use a formula
    return Math.max(0, 3000 - (pickNumber * 10));
  }
  
  // Handle the draft timer
  startTimer() {
    this.timerActive = true;
    
    this.timerInterval = setInterval(() => {
      this.timeRemaining--;
      
      // Call the tick callback if provided
      if (this.onTimerTick) {
        this.onTimerTick(this.timeRemaining);
      }
      
      // If timer expires, trigger auto-pick
      if (this.timeRemaining <= 0) {
        this.handleTimerExpired();
      }
    }, 1000);
  }
  
  // Handle timer expiration
  handleTimerExpired() {
    clearInterval(this.timerInterval);
    this.timerActive = false;
    
    // Call the expired callback if provided
    if (this.onTimerExpired) {
      this.onTimerExpired();
    }
    
    // If auto-pick is enabled, make the pick
    if (this.settings.autoPickEnabled) {
      this.makeAIPick();
    }
  }
  
  // Reset the pick timer
  resetTimer() {
    clearInterval(this.timerInterval);
    this.timeRemaining = this.settings.pickTimeSeconds;
    this.timerActive = false;
    
    // Start the timer immediately
    this.startTimer();
  }
  
  // Pause the timer
  pauseTimer() {
    clearInterval(this.timerInterval);
    this.timerActive = false;
  }
  
  // Resume the timer
  resumeTimer() {
    if (!this.timerActive) {
      this.startTimer();
    }
  }
  
  // Register a callback for timer ticks
  registerTimerTickCallback(callback) {
    this.onTimerTick = callback;
  }
  
  // Register a callback for timer expiration
  registerTimerExpiredCallback(callback) {
    this.onTimerExpired = callback;
  }
  
  // End the draft
  endDraft() {
    // Clear any timers
    clearInterval(this.timerInterval);
    this.timerActive = false;
    
    // Calculate draft grades for each team (simplified)
    const draftGrades = this.calculateDraftGrades();
    
    return {
      complete: true,
      draftHistory: this.draftHistory,
      draftGrades
    };
  }
  
  // Calculate draft grades for each team
  calculateDraftGrades() {
    const grades = {};
    
    this.teams.forEach(team => {
      // Get all picks by this team
      const teamPicks = this.draftHistory.filter(pick => pick.teamId === team.id);
      
      // Calculate the value acquired
      let valueAcquired = teamPicks.reduce((total, pick) => {
        const prospect = this.prospects.find(p => p.id === pick.prospectId);
        return total + (prospect ? prospect.grade * 10 : 0);
      }, 0);
      
      // Adjust for needs
      const teamNeeds = this.getTeamNeeds(team.id);
      const needsAddressed = new Set();
      
      teamPicks.forEach(pick => {
        const prospect = this.prospects.find(p => p.id === pick.prospectId);
        if (prospect) {
          const matchedNeed = teamNeeds.find(need => need.position === prospect.position);
          if (matchedNeed) {
            needsAddressed.add(matchedNeed.position);
            
            // Bonus for addressing high-priority needs
            if (matchedNeed.priority === 'High') {
              valueAcquired += 20;
            } else if (matchedNeed.priority === 'Medium') {
              valueAcquired += 10;
            }
          }
        }
      });
      
      // Penalty for missing high-priority needs
      const missedHighPriorityNeeds = teamNeeds
        .filter(need => need.priority === 'High' && !needsAddressed.has(need.position))
        .length;
      
      valueAcquired -= missedHighPriorityNeeds * 15;
      
      // Calculate letter grade
      let letterGrade;
      if (valueAcquired >= 100) letterGrade = 'A+';
      else if (valueAcquired >= 90) letterGrade = 'A';
      else if (valueAcquired >= 85) letterGrade = 'A-';
      else if (valueAcquired >= 80) letterGrade = 'B+';
      else if (valueAcquired >= 75) letterGrade = 'B';
      else if (valueAcquired >= 70) letterGrade = 'B-';
      else if (valueAcquired >= 65) letterGrade = 'C+';
      else if (valueAcquired >= 60) letterGrade = 'C';
      else if (valueAcquired >= 55) letterGrade = 'C-';
      else if (valueAcquired >= 50) letterGrade = 'D+';
      else if (valueAcquired >= 45) letterGrade = 'D';
      else letterGrade = 'F';
      
      grades[team.id] = {
        letterGrade,
        valueAcquired,
        needsAddressed: [...needsAddressed],
        description: this.generateGradeDescription(letterGrade, teamPicks, needsAddressed)
      };
    });
    
    return grades;
  }
  
  // Generate a description for a team's draft grade
  generateGradeDescription(grade, picks, needsAddressed) {
    // This would be more sophisticated in a real app
    if (grade.startsWith('A')) {
      return "Outstanding draft that addressed key needs with high-value selections.";
    } else if (grade.startsWith('B')) {
      return "Solid draft with good value selections that addressed most team needs.";
    } else if (grade.startsWith('C')) {
      return "Average draft that addressed some needs but missed opportunities for better value.";
    } else if (grade.startsWith('D')) {
      return "Below average draft that failed to address key needs effectively.";
    } else {
      return "Poor draft with questionable selections that didn't address team needs.";
    }
  }
}

// Export the DraftEngine class
export default DraftEngine;