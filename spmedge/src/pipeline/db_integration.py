import logging
import os
import json
import psycopg2
from psycopg2.extras import execute_values
from typing import Dict, Any, Optional
from config.config import config

# Ensure logs directory exists
LOG_DIR = config.LOG_DIR
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "db_integration.log")

# Centralized logging (avoiding duplicate handlers)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

class DBManager:
    """Handles database operations for the document processing pipeline."""

    def __init__(self):
        """Initialize the database connection."""
        try:
            self.conn = psycopg2.connect(
                dbname=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                host=config.DB_HOST,
                port=config.DB_PORT
            )
            self.conn.autocommit = True  # 🔥 Ensure autocommit is enabled
            self.cursor = self.conn.cursor()
            
            logger.info("✅ Database connection established.")
        except Exception as e:
            logger.error(f"❌ Failed to connect to database: {e}")

    def get_document_type(self, document_id: str) -> Optional[str]:
        """Fetch document type given a document ID."""
        try:
            query = """
                SELECT dt.name 
                FROM documents d
                JOIN document_types dt ON d.document_type_id = dt.id
                WHERE d.id = %s;
            """
            self.cursor.execute(query, (document_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None

        except Exception as e:
            logger.error(f"❌ Error fetching document type for {document_id}: {e}")
            return None

    def update_pipeline_status(self, document_id: str, pipeline_stage: str, status: str, error_message: Optional[str] = None):
        """Update document processing status in the pipeline, ensuring document_type_id is set."""
        try:
            # ✅ Ensure document_type_id is retrieved before updating pipeline
            self.cursor.execute("SELECT document_type_id FROM documents WHERE id = %s;", (document_id,))
            result = self.cursor.fetchone()
    
            if not result or result[0] is None:
                logger.error(f"❌ Cannot update pipeline: document_type_id is NULL for document {document_id}")
                return
    
            document_type_id = result[0]
    
            query = """
                INSERT INTO processing_pipeline (document_id, document_type_id, pipeline_stage, status, error_message, batch_id, updated_at)
                VALUES (%s, %s, %s, %s, %s, (SELECT batch_id FROM documents WHERE id = %s), NOW())
                ON CONFLICT (document_id, pipeline_stage) DO UPDATE 
                SET status = EXCLUDED.status, error_message = EXCLUDED.error_message, updated_at = NOW();
            """
            self.cursor.execute(query, (document_id, document_type_id, pipeline_stage, status, error_message, document_id))
            self.conn.commit()
            logger.info(f"✅ Updated pipeline status: {document_id} | {pipeline_stage} → {status}")
    
        except Exception as e:
            logger.error(f"❌ Error updating pipeline status: {e}")
            self.conn.rollback()

    def transition_document_to_stage(self, document_id: str, from_stage: str, to_stage: str, 
                                   status: str = "pending", error_message: str = None, batch_id: str = None) -> bool:
        """
        Transition a document from one pipeline stage to another.
        
        Args:
            document_id: The document ID
            from_stage: Source pipeline stage
            to_stage: Target pipeline stage
            status: Status to set in the target stage
            error_message: Optional error message
            batch_id: Optional batch ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Mark source stage as completed
            self.update_pipeline_status(document_id, from_stage, "completed")
            
            # Create or update target stage
            self.update_pipeline_status(document_id, to_stage, status, error_message)
            
            logger.info(f"✅ Transitioned document {document_id} from {from_stage} to {to_stage}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to transition document {document_id}: {e}")
            return False

    def fetch_documents_by_stage(self, pipeline_stage: str, status: str = "pending", limit: int = 100):
        """Retrieve documents from the pipeline based on their stage and status."""
        try:
            query = """
                SELECT d.id, d.name, d.document_type_id, pp.status, pp.batch_id
                FROM documents d
                JOIN processing_pipeline pp ON d.id = pp.document_id
                WHERE pp.pipeline_stage = %s AND pp.status = %s
                LIMIT %s;
            """
            self.cursor.execute(query, (pipeline_stage, status, limit))
            documents = self.cursor.fetchall()

            if not documents:
                logger.info(f"ℹ️ No documents found for stage: {pipeline_stage} with status: {status}")
                return []

            return [
                {
                    "id": row[0],
                    "name": row[1],
                    "document_type_id": row[2],
                    "status": row[3],
                    "batch_id": row[4]
                }
                for row in documents
            ]

        except Exception as e:
            logger.error(f"❌ Failed to fetch documents for stage {pipeline_stage}: {e}")
            return []

    def close_connection(self):
        """Close the database connection."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            logger.info("✅ Database connection closed.")
        except Exception as e:
            logger.error(f"❌ Error closing database connection: {e}")
    
    def save_processed_document(self, extracted_data: Dict[str, Any], document_id: str) -> bool:
        """Saves structured data extracted from a processed document."""
        try:
            if not extracted_data:
                logger.warning(f"⚠️ No extracted data to save for document {document_id}")
                return False
    
            extracted_json = json.dumps(extracted_data)  # Convert dict to JSON string
    
            self.cursor.execute(
                "UPDATE documents SET metadata = %s, batch_status = 'completed', updated_at = NOW() WHERE id = %s;",
                (extracted_json, document_id)
            )
            self.conn.commit()
    
            # ✅ Log successful save
            logger.info(f"💾 Successfully saved extracted data for document {document_id}")
    
            return True
        except Exception as e:
            logger.error(f"❌ Error saving extracted document for {document_id}: {e}")
            self.conn.rollback()
            return False
            
    def get_prompt_for_document_type(self, document_type) -> Optional[str]:
        """Retrieve AI processing prompt for a given document type."""
        try:
            # Check if document_type is an integer ID or a string name
            if isinstance(document_type, int) or document_type.isdigit():
                # It's an ID
                self.cursor.execute("SELECT ai_prompt FROM document_prompts WHERE document_type_id = %s;", (document_type,))
            else:
                # It's a name
                self.cursor.execute("SELECT ai_prompt FROM document_prompts WHERE document_type = %s;", (document_type,))
            
            result = self.cursor.fetchone()
            return result[0] if result else None
        
        except Exception as e:
            logger.error(f"❌ Error fetching AI prompt for {document_type}: {e}")
            return None
        
    def get_schema_for_document_type(self, document_type) -> Optional[Dict[str, Any]]:
        """Retrieve document schema definition for a given document type."""
        try:
            # Check if document_type is an integer ID or a string name
            if isinstance(document_type, int) or document_type.isdigit():
                # It's an ID
                self.cursor.execute("SELECT schema_definition FROM document_schema WHERE document_type_id = %s;", (document_type,))
            else:
                # It's a name
                self.cursor.execute("SELECT schema_definition FROM document_schema WHERE document_type = %s;", (document_type,))
            
            result = self.cursor.fetchone()
    
            # Return the result directly if it's already a dictionary
            if result and isinstance(result[0], dict):
                return result[0]
    
            # Ensure JSON parsing only if necessary
            return json.loads(result[0]) if result and isinstance(result[0], str) else None
        
        except Exception as e:
            logger.error(f"❌ Error fetching schema for {document_type}: {e}")
            return None
        
