#!/usr/bin/env python3
"""
Fixed Document Processor - Handles Medtronic nested JSON files correctly.
"""

import os
import sys
import json
import logging
import argparse
import time
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Fix the import path issue - use absolute imports
sys.path.insert(0, '/Users/toddlebaron/prizym/spmedge')

from config.config import config
from src.pipeline.db_integration import DBManager
from src.pipeline.pipeline_processor import PipelineProcessor, PipelineStage

# Ensure logs directory exists
os.makedirs(config.LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(config.LOG_DIR, "document_processor_debug.log")

# Configure logging with propagation disabled
logger = logging.getLogger("document_processor")
logger.propagate = False  # CRITICAL: Disable propagation to parent loggers

if not logger.handlers:
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# Initialize pipeline processor for PROCESS stage
processor = PipelineProcessor(PipelineStage.PROCESS)
db_manager = DBManager()

class DocumentProcessor:
    """Handles OpenAI integration and structured extraction from cleaned documents."""
    
    def __init__(self, api_key=None, model=None):
        """Initialize processor with OpenAI credentials and API model settings."""
        import os
        import openai

        # Load API key from config or environment
        self.api_key = api_key or config.OPENAI_API_KEY
        openai.api_key = self.api_key
        
        # Load OpenAI model from config or parameter
        self.model = model or config.OPENAI_MODEL
        logger.info(f"🔧 Initializing processor with model: {self.model}")

        # Initialize OpenAI client
        self.client = openai.OpenAI()
        
        # Rate limit tracking
        self.last_request_time = 0
        self.min_request_interval = 3.0  # Minimum seconds between requests
    
    def _clean_json_response(self, response_text: str) -> str:
        """Clean JSON response from OpenAI by removing markdown code blocks."""
        # Remove markdown code blocks if present
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        # Remove any trailing or leading characters that might break JSON parsing
        response_text = response_text.strip()
        
        return response_text
    
    def _rate_limit_wait(self):
        """Enforce a minimum wait time between API requests to avoid rate limits."""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        
        if elapsed < self.min_request_interval:
            wait_time = self.min_request_interval - elapsed
            logger.info(f"⏱️ Rate limit protection: Waiting {wait_time:.2f}s between requests")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
        
    def extract_structured_data(self, content: str, document_type: str = None) -> Dict[str, Any]:
        """Extract structured data from a cleaned document using OpenAI with retry logic."""
        logger.info(f"🧠 Processing document with type: {document_type}")
    
        # Load custom prompt if available
        try:
            custom_prompt = db_manager.get_prompt_for_document_type(document_type)
            if custom_prompt:
                logger.info(f"✅ Using custom prompt for {document_type}")
                
                # Add Medtronic-specific context to the prompt
                custom_prompt = custom_prompt + "\n\nNote: This document is from Medtronic, a medical device company. Extract the actual data from the document, not fictional information."
            else:
                logger.info(f"ℹ️ No custom prompt found for {document_type}, using default")
                custom_prompt = "Extract structured data from this document. This document is from Medtronic, a medical device company. Extract only factual information from the document."
    
        except Exception as e:
            logger.warning(f"⚠️ Error getting prompt for {document_type}: {str(e)}")
            custom_prompt = "Extract structured data from this document. This document is from Medtronic, a medical device company. Extract only factual information from the document."
    
        # Load schema if available
        try:
            schema = db_manager.get_schema_for_document_type(document_type)
            if schema:
                logger.info(f"✅ Successfully loaded schema for {document_type}")
                # Add schema to prompt if available
                schema_json = json.dumps(schema, indent=2)
                custom_prompt += f"\n\nReturn your response in the following JSON schema:\n{schema_json}"
            else:
                logger.warning(f"⚠️ No schema found for document type: {document_type}")
    
        except Exception as e:
            logger.error(f"❌ Error loading schema for {document_type}: {str(e)}")
    
        # ✅ Call OpenAI API for document processing with retry logic
        max_retries = 5
        retry_count = 0
        base_delay = 2
        
        # Limit content length to avoid token limits
        max_content_length = 15000  # Adjust based on model capabilities
        if len(content) > max_content_length:
            logger.warning(f"⚠️ Content too long ({len(content)} chars), truncating to {max_content_length}")
            content = content[:max_content_length] + "... [content truncated]"
            
        # Log the first 500 characters of content for debugging
        logger.info(f"📝 Content Sample (first 500 chars): {content[:500]}")
        
        while True:
            try:
                # Wait to respect rate limits
                self._rate_limit_wait()
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an AI assistant skilled in structured data extraction for Medtronic, a medical device company. Extract only ACTUAL information from the document, not fictional data."},
                        {"role": "user", "content": f"{custom_prompt}\n\n{content}"}
                    ],
                    temperature=0.1,  # Lower temperature for more consistent results
                    max_tokens=2000,  # Increased token limit for complex documents
                    response_format={"type": "json_object"}  # Request JSON format explicitly
                )
        
                raw_response = response.choices[0].message.content.strip()
                logger.info(f"✅ OpenAI Response received: {len(raw_response)} chars")
        
                # Attempt to parse response as JSON
                try:
                    # Clean the response to handle markdown formatting
                    cleaned_response = self._clean_json_response(raw_response)
                    structured_data = json.loads(cleaned_response)
                    logger.info("✅ Successfully parsed JSON response")
                    return structured_data
                    
                except json.JSONDecodeError as e:
                    # If we can't parse as JSON but have a raw response, return it as-is
                    logger.warning(f"⚠ OpenAI response is not valid JSON: {e}")
                    return {"raw_text": raw_response}
        
            except Exception as e:
                retry_count += 1
                error_msg = str(e)
                
                # Check if this is a rate limit error
                if "rate_limit" in error_msg.lower() or "429" in error_msg:
                    if retry_count <= max_retries:
                        # Calculate exponential backoff with jitter
                        delay = min(60, base_delay * (2 ** (retry_count - 1)))
                        delay = delay * (0.5 + random.random())  # Add jitter
                        
                        logger.warning(f"⚠️ Rate limit hit. Retry {retry_count}/{max_retries} - waiting {delay:.2f}s")
                        time.sleep(delay)
                        continue
                    else:
                        logger.error(f"❌ Max retries exceeded for rate limits")
                        break
                else:
                    # Not a rate limit error
                    logger.error(f"❌ OpenAI API call failed: {e}")
                    break

        # If we get here, all retries failed
        return {"status": "failed", "message": f"OpenAI API call failed after {retry_count} retries"}

    def extract_actual_content(self, json_str):
        """Extract the actual document content from nested JSON structures."""
        try:
            # First level JSON parsing
            data = json.loads(json_str)
            if not isinstance(data, dict):
                return json_str  # Not a JSON object, return as-is
                
            # Check if this is our nested structure
            if 'content' in data:
                content = data['content']
                
                # Check if content itself is a JSON string that needs parsing
                if isinstance(content, str) and (content.startswith('{') or content.startswith('{"')):
                    try:
                        # Try to parse the nested JSON
                        nested_data = json.loads(content)
                        if isinstance(nested_data, dict) and 'content' in nested_data:
                            # Found our target structure - return the actual document content
                            extracted_content = nested_data['content']
                            logger.info(f"✅ Successfully extracted content from nested JSON (length: {len(extracted_content)})")
                            return extracted_content
                        else:
                            # Just a regular JSON, return it
                            return content
                    except json.JSONDecodeError:
                        # Not valid JSON, just return the content string
                        return content
                else:
                    # Content exists but is not a JSON string
                    return content
            
            # No obvious content field, return original
            return json_str
            
        except json.JSONDecodeError:
            # Not valid JSON, return as-is
            return json_str
        except Exception as e:
            logger.error(f"❌ Error extracting content from JSON: {e}")
            return json_str

    def find_document_content(self, document_id: str) -> Optional[str]:
        """Find document content from previous pipeline stage."""
        dirs = processor.get_base_dirs()
        stage_clean_dir = dirs["stage_clean"]
        
        # First, look for files in the clean stage directory
        clean_files = list(stage_clean_dir.glob(f"*doc{str(document_id).replace('-', '')[:12]}*"))
        
        if clean_files:
            try:
                clean_file = clean_files[0]
                logger.info(f"✅ Found clean file: {clean_file}")
                
                with open(clean_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Handle nested JSON content structure
                    actual_content = self.extract_actual_content(content)
                    return actual_content

            except Exception as e:
                logger.warning(f"⚠️ Error reading clean file: {e}")
        
        # If not found in stage directory, check batch files as fallback
        processed_dir = dirs["processed"]
        batch_files = list(processed_dir.glob("pipeline_clean_*.json"))
        
        for batch_file in batch_files:
            try:
                with open(batch_file, 'r', encoding='utf-8') as f:
                    batch_data = json.load(f)
                    for batch_doc in batch_data:
                        if str(batch_doc.get('id')) == str(document_id):
                            if "cleaned_content" in batch_doc:
                                content = batch_doc.get('cleaned_content', "")
                                if content:
                                    # Handle nested JSON content structure
                                    actual_content = self.extract_actual_content(content)
                                    logger.info(f"✅ Found content in batch file {batch_file}")
                                    return actual_content
            except Exception as e:
                logger.warning(f"⚠️ Error loading batch file {batch_file}: {e}")
                
        logger.warning(f"⚠️ Could not find content for document {document_id}")
        return None

def process_documents(limit=10, model=None, batch_size=2):
    """Processes documents that are ready for OpenAI extraction with rate limit protection."""
    try:
        model = model or config.OPENAI_MODEL
        logger.info(f"🚀 Starting document processor with model={model}, batch_size={batch_size}")

        # Initialize processor
        processor_instance = DocumentProcessor(model=model)

        # Get documents from clean stage
        documents = processor.get_documents_for_stage(current_stage="clean", status="completed", limit=limit)

        if not documents:
            logger.warning("⚠ No documents found ready for processing")
            return

        # Create processing batch
        batch_name = f"process_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        batch_id = processor.record_batch_processing(batch_name, len(documents), status="processing")

        processed_documents = []
        total_count = len(documents)
        success_count = 0

        # Process documents in small batches to avoid rate limits
        for i in range(0, total_count, batch_size):
            current_batch = documents[i:i+batch_size]
            logger.info(f"⚙️ Processing batch {i//batch_size + 1}/{(total_count+batch_size-1)//batch_size} ({len(current_batch)} documents)")
            
            for doc in current_batch:
                result = process_document(doc, processor_instance, batch_id)
                if result:
                    processed_documents.append(result)
                    success_count += 1
                    
                # Add a small delay between documents in the same batch
                if batch_size > 1:
                    time.sleep(1)
            
            # Report progress
            logger.info(f"📊 Progress: {success_count}/{total_count} documents processed successfully")

        # Save processed documents
        if processed_documents:
            processor.save_document_batch(documents=processed_documents, batch_name=batch_name)
            logger.info(f"✅ Successfully processed {len(processed_documents)} documents")
            processor.finalize_batch(batch_id, "completed" if len(processed_documents) == total_count else "partial")
        else:
            logger.warning("⚠ No documents were successfully processed")
            processor.finalize_batch(batch_id, "failed")

    except Exception as e:
        logger.error(f"❌ Failed to process documents: {e}")

def process_document(doc, processor_instance, batch_id):
    """Processes a single document using OpenAI."""
    document_id = doc['id']
    
    # Get document type from database
    document_type = db_manager.get_document_type(document_id)
    if not document_type:
        document_type = "unknown"
    
    logger.info(f"🔍 Processing document {document_id} of type {document_type}")

    # Update status to processing
    processor.update_document_stage(document_id, status="processing", batch_id=batch_id)

    try:
        # Search for document content in clean stage
        content = processor_instance.find_document_content(document_id)
        
        if not content or not content.strip():
            logger.warning(f"⚠ Document {document_id} has no content to process")
            processor.update_document_stage(document_id, status="failed", error_message="No content found", batch_id=batch_id)
            return None

        # Process with OpenAI
        structured_data = processor_instance.extract_structured_data(content, document_type)
        
        # Generate processed filename
        new_filename = processor.generate_stage_filename(
            original_filename=doc.get('name', f"doc_{document_id}.json"),
            document_id=document_id,
            batch_id=batch_id
        )
        
        # Save JSON to process stage directory
        dirs = processor.get_base_dirs()
        process_dir = dirs["stage_process"]
        process_file_path = process_dir / new_filename
        
        with open(process_file_path, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=2)
        
        logger.info(f"✅ Saved processed data to {process_file_path}")

        # Create processed document object
        processed_doc = {
            "id": document_id,
            "name": doc.get('name'),
            "pipeline_filename": new_filename,
            "document_type_id": doc.get('document_type_id'),
            "document_type": document_type,
            "structured_data": structured_data,
            "content_length": len(content) if content else 0,
            "previous_stage": "clean",
            "pipeline_stage": "process",
            "batch_id": batch_id,
            "status": "completed"
        }

        # Save processed data to database - only call once
        success = db_manager.save_processed_document(structured_data, document_id)
        if not success:
            logger.warning(f"⚠️ Failed to save processed data for document {document_id}")

        # Update status to completed
        processor.update_document_stage(document_id, status="completed", batch_id=batch_id)

        logger.info(f"✅ Successfully processed document {document_id}")
        return processed_doc

    except Exception as e:
        logger.error(f"❌ Error processing document {document_id}: {e}")
        processor.update_document_stage(document_id, status="failed", error_message=str(e), batch_id=batch_id)
        return None

def main():
    """Main entry point for document processing."""
    parser = argparse.ArgumentParser(description="Document Processor - Extract structured data with OpenAI")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Max documents to process")
    parser.add_argument("--model", "-m", type=str, default=None, help="OpenAI model to use")
    parser.add_argument("--batch-size", "-b", type=int, default=2, help="Number of documents per batch")
    args = parser.parse_args()

    process_documents(limit=args.limit, model=args.model, batch_size=args.batch_size)

if __name__ == "__main__":
    main()