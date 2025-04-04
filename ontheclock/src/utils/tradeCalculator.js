export const calculateTradeValue = (pickNumber) => {
  // Simple draft value chart based on historical trades
  const tradeChart = {
    1: 3000, 2: 2600, 3: 2200, 4: 1800, 5: 1500,
    10: 1000, 15: 850, 20: 650, 30: 450, 50: 300
  };
  
  return tradeChart[pickNumber] || 100;
};