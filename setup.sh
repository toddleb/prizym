#!/bin/bash

# Define the base directory
BASE_DIR="ontheclock"

# Create directories
mkdir -p $BASE_DIR/src/components
mkdir -p $BASE_DIR/src/data
mkdir -p $BASE_DIR/src/hooks
mkdir -p $BASE_DIR/src/context
mkdir -p $BASE_DIR/src/utils

# Create files
touch $BASE_DIR/src/components/CircularDraftBoard.js
touch $BASE_DIR/src/components/ProspectList.js
touch $BASE_DIR/src/components/TeamCard.js
touch $BASE_DIR/src/components/BettingAnalytics.js
touch $BASE_DIR/src/components/DraftHistory.js
touch $BASE_DIR/src/components/Header.js

touch $BASE_DIR/src/data/teams.js
touch $BASE_DIR/src/data/prospects.js
touch $BASE_DIR/src/data/draftLogic.js

touch $BASE_DIR/src/hooks/useDraftLogic.js

touch $BASE_DIR/src/context/DraftContext.js

touch $BASE_DIR/src/utils/tradeCalculator.js

touch $BASE_DIR/src/App.js
touch $BASE_DIR/src/index.js

touch $BASE_DIR/package.json
touch $BASE_DIR/README.md

echo "Project structure created successfully!"
