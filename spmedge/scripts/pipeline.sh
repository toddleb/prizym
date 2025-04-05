#!/bin/bash
# pipeline.sh - SPM Edge Pipeline Management Script

# Set the directory paths using script location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_PATH="$( dirname "$SCRIPT_DIR" )"  # Parent of scripts directory
DATA_PATH="$REPO_PATH/data"
PYTHON="/opt/homebrew/bin/python3"  # Hardcoded path based on your environment

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load database configuration from .env file
if [ -f "$REPO_PATH/.env" ]; then
    source "$REPO_PATH/.env"
else
    echo -e "${RED}Error: .env file not found at $REPO_PATH/.env${NC}"
    exit 1
fi

# Function to display help
function show_help {
    echo -e "${BLUE}SPM Edge Pipeline Management${NC}"
    echo "----------------------------------------"
    echo "Usage: pipeline.sh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  process [type]     Process documents of specified type"
    echo "  list               List active batches and pipeline status"
    echo "  status [batch-id]  Show detailed status of a batch"
    echo "  reset [stage]      Reset a pipeline stage (or all stages)"
    echo "  cleanup            Clean up orphaned documents and batches"
    echo "  run-all [type]     Run the complete pipeline for a document type"
    echo "  types              List available document types"
    echo "  help               Show this help information"
    echo ""
    echo "Options:"
    echo "  --archive          Archive original files after processing"
    echo "  --delete           Delete original files after processing"
    echo "  --batch [id]       Specify a batch ID (for reset command)"
    echo "  --batch-size [n]   Set the batch size for processing (default: 500)"
    echo ""
    echo "Examples:"
    echo "  pipeline.sh process compensation_plan --archive"
    echo "  pipeline.sh reset --stage clean"
    echo "  pipeline.sh run-all compensation_plan --batch-size 200"
    echo ""
}

function run_cmd {
    echo -e "${YELLOW}Running: $1${NC}"
    echo "----------------------------------------"
    # Save current directory
    local current_dir=$(pwd)
    # Change to project root
    cd $REPO_PATH
    # Run the command
    eval "$1"
    local status=$?
    # Return to original directory
    cd $current_dir
    echo "----------------------------------------"
    if [ $status -eq 0 ]; then
        echo -e "${GREEN}Command completed successfully${NC}"
    else
        echo -e "${RED}Command failed with exit code $status${NC}"
    fi
    echo ""
}

# Function to list document types from database
function list_document_types {
    echo -e "${BLUE}Available Document Types:${NC}"
    echo "----------------------------------------"
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "SELECT id, name, description FROM document_types ORDER BY name;" | \
    while read line; do
        id=$(echo $line | awk '{print $1}')
        name=$(echo $line | awk '{print $2}')
        desc=$(echo $line | cut -d ' ' -f 3-)
        echo -e "${GREEN}$id${NC}\t${YELLOW}$name${NC}\t$desc"
    done
    
    # Show document count by type
    echo -e "\n${BLUE}Document Count by Type:${NC}"
    echo "----------------------------------------"
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -t -c "
        SELECT dt.name AS type, COUNT(d.id) AS count 
        FROM document_types dt 
        LEFT JOIN documents d ON dt.id = d.document_type_id 
        GROUP BY dt.name 
        ORDER BY count DESC;" | \
    while read line; do
        type=$(echo $line | awk '{print $1}')
        count=$(echo $line | awk '{print $2}')
        echo -e "${YELLOW}$type${NC}\t${GREEN}$count${NC} documents"
    done
}

# Function to run the complete pipeline for a document type
function run_pipeline {
    DOC_TYPE=$1
    BATCH_SIZE=${2:-500}  # Default to 500 if not specified
    
    echo -e "${BLUE}Running complete pipeline for document type: ${YELLOW}$DOC_TYPE${NC} with batch size: ${GREEN}$BATCH_SIZE${NC}"
    echo "----------------------------------------"
    
    # Process the batch
    run_cmd "$PYTHON src/pipeline/batch_manager.py process $DOC_TYPE --archive"
    
    # Wait for user confirmation before continuing
    read -p "$(echo -e ${YELLOW}Continue to document loading stage? [y/N]: ${NC})" continue
    if [[ ! $continue =~ ^[Yy]$ ]]; then
        echo "Pipeline stopped after batch processing."
        exit 0
    fi
    
    # Run document loader with batch size
    run_cmd "$PYTHON src/pipeline/document_loader.py --limit $BATCH_SIZE"
    
    # Show status and wait for confirmation
    run_cmd "$PYTHON src/pipeline/batch_manager.py list"
    read -p "$(echo -e ${YELLOW}Continue to document cleaning stage? [y/N]: ${NC})" continue
    if [[ ! $continue =~ ^[Yy]$ ]]; then
        echo "Pipeline stopped after document loading."
        exit 0
    fi
    
    # Run document cleaner with batch size
    run_cmd "$PYTHON src/pipeline/document_cleaner.py --limit $BATCH_SIZE"
    
    # Show status and wait for confirmation before proceeding to document processor
    run_cmd "$PYTHON src/pipeline/batch_manager.py list"
    read -p "$(echo -e ${YELLOW}Continue to document processing stage? [y/N]: ${NC})" continue
    if [[ ! $continue =~ ^[Yy]$ ]]; then
        echo "Pipeline stopped after document cleaning."
        exit 0
    fi
    
    # Run document processor with batch size
    run_cmd "$PYTHON src/pipeline/document_processor.py --limit $BATCH_SIZE --batch-size $((BATCH_SIZE/5))"
    
    # Continue with other stages, passing the batch size where appropriate
    # ... existing code ...
    
    echo -e "${GREEN}Pipeline complete!${NC}"
}

# Main script execution
case "$1" in
    process)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Document type required${NC}"
            show_help
            exit 1
        fi
        
        # Check for options
        ARCHIVE=""
        DELETE=""
        BATCH_SIZE="500"  # Default batch size
        
        for ((i=3; i<=$#; i++)); do
            arg="${!i}"
            next_idx=$((i+1))
            next_arg="${!next_idx}"
            
            if [ "$arg" == "--archive" ]; then
                ARCHIVE="--archive"
            elif [ "$arg" == "--delete" ]; then
                DELETE="--delete"
            elif [ "$arg" == "--batch-size" ] && [ -n "$next_arg" ]; then
                BATCH_SIZE="$next_arg"
                i=$next_idx
            fi
        done
        
        run_cmd "$PYTHON src/pipeline/batch_manager.py process $2 $ARCHIVE $DELETE --batch-size $BATCH_SIZE"
        ;;
        
    list)
        run_cmd "$PYTHON src/pipeline/batch_manager.py list"
        ;;
        
    status)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Batch ID required${NC}"
            show_help
            exit 1
        fi
        run_cmd "$PYTHON src/pipeline/batch_manager.py status $2"
        ;;
        
    reset)
        STAGE=""
        BATCH=""
        
        # Parse arguments
        for ((i=2; i<=$#; i++)); do
            arg="${!i}"
            next_idx=$((i+1))
            next_arg="${!next_idx}"
            
            if [ "$arg" == "--stage" ] && [ -n "$next_arg" ]; then
                STAGE="--stage $next_arg"
                i=$next_idx
            elif [ "$arg" == "--batch" ] && [ -n "$next_arg" ]; then
                BATCH="--batch $next_arg"
                i=$next_idx
            fi
        done
        
        run_cmd "$PYTHON src/pipeline/batch_manager.py reset $STAGE $BATCH"
        ;;
        
    cleanup)
        run_cmd "$PYTHON src/pipeline/batch_manager.py cleanup"
        ;;
    
    run-all)
        if [ -z "$2" ]; then
            echo -e "${RED}Error: Document type required${NC}"
            show_help
            exit 1
        fi
        
        # Parse for batch size option
        DOC_TYPE="$2"
        BATCH_SIZE="500"  # Default batch size
        
        for ((i=3; i<=$#; i++)); do
            arg="${!i}"
            next_idx=$((i+1))
            next_arg="${!next_idx}"
            
            if [ "$arg" == "--batch-size" ] && [ -n "$next_arg" ]; then
                BATCH_SIZE="$next_arg"
                i=$next_idx
            fi
        done
        
        run_pipeline "$DOC_TYPE" "$BATCH_SIZE"
        ;;
        
    types)
        list_document_types
        ;;
        
    help|--help|-h)
        show_help
        ;;
        
    *)
        echo -e "${RED}Error: Unknown command '$1'${NC}"
        show_help
        exit 1
        ;;
esac

exit 0