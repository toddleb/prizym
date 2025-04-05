#!/usr/bin/env python3
"""
Batch Document Processor - Extracts structured data at scale using OpenAI's Batch API.
- Integrates with SPM Edge pipeline
- Uses OpenAI Batch API for large-scale processing
- Tracks document progression through pipeline stages
"""

import os
import json
import logging
import argparse
import openai
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from config.config import config
from src.pipeline.db_integration import DBManager
from src.pipeline.pipeline_processor import PipelineProcessor, PipelineStage

# Ensure logs directory exists
os.makedirs(config.LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(config.LOG_DIR, "document_processor_batch.log")

# Configure logging
logger = logging.getLogger("document_processor_batch")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Initialize processors
processor = PipelineProcessor(PipelineStage.PROCESS)
db_manager = DBManager()

class BatchDocumentProcessor:
    """Handles OpenAI Batch API processing for large document sets."""

    def __init__(self, api_key=None, model=None, batch_size=5000):
        """Initialize batch processor with OpenAI credentials."""
        self.api_key = api_key or config.OPENAI_API_KEY
        openai.api_key = self.api_key
        self.model = model or config.OPENAI_MODEL
        self.batch_size = batch_size  # Limit per batch (max: 50,000)
        self.client = openai.OpenAI()
        logger.info(f"🔧 Initialized Batch Processor with model: {self.model}, batch_size: {self.batch_size}")

    def find_cleaned_document(self, doc_id):
        """Finds the cleaned document from the stage_clean directory or batch files."""
        dirs = processor.get_base_dirs()
        stage_clean_dir = dirs["stage_clean"]

        # First, look for files in the clean stage directory
        clean_files = list(stage_clean_dir.glob(f"*doc{str(doc_id).replace('-', '')[:12]}*"))

        if clean_files:
            try:
                clean_file = clean_files[0]
                logger.info(f"✅ Found clean file: {clean_file}")

                with open(clean_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return {"id": doc_id, "cleaned_content": content}
            except Exception as e:
                logger.warning(f"⚠️ Error reading clean file: {e}")

        # If not found in stage directory, check batch files as fallback
        processed_dir = dirs["processed"]
        cleaned_files = list(processed_dir.glob("pipeline_clean_*.json"))

        if not cleaned_files:
            logger.error("❌ No cleaned document batch files found.")
            return None

        for file in cleaned_files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    documents = json.load(f)

                    for doc in documents:
                        if doc.get("id") == doc_id:
                            return doc  # Return the cleaned document

            except Exception as e:
                logger.warning(f"⚠️ Error reading {file}: {e}")

        logger.warning(f"⚠️ Could not find cleaned content for document {doc_id}")
        return None

    def create_jsonl_file(self, documents: List[Dict[str, Any]], batch_file: str):
        """Convert cleaned documents into JSONL format for OpenAI Batch API."""
        # Create the batch file in the process stage directory
        dirs = processor.get_base_dirs()
        stage_process_dir = dirs["stage_process"]
        batch_file_path = stage_process_dir / batch_file

        with open(batch_file_path, "w", encoding="utf-8") as outfile:
            valid_documents = 0  # Track valid docs

            for doc in documents:
                cleaned_doc = self.find_cleaned_document(doc["id"])

                if not cleaned_doc or "cleaned_content" not in cleaned_doc:
                    logger.warning(f"⚠ Document {doc['id']} has no cleaned content. Skipping.")
                    continue  # Skip missing documents

                cleaned_content = cleaned_doc["cleaned_content"].strip()

                # Get document type for better prompting
                document_type = db_manager.get_document_type(doc["id"]) or "unknown"

                # Try to get custom prompt
                custom_prompt = "Extract structured data from this document."
                try:
                    prompt = db_manager.get_prompt_for_document_type(document_type)
                    if prompt:
                        custom_prompt = prompt
                except Exception:
                    pass

                request = {
                    "custom_id": doc["id"],
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": "You are an AI assistant skilled in structured data extraction."},
                            {"role": "user", "content": f"{custom_prompt}\n\n{cleaned_content}"}
                        ],
                        "max_tokens": 1500,
                        "temperature": 0.2
                    }
                }
                json.dump(request, outfile)
                outfile.write("\n")
                valid_documents += 1

        logger.info(f"✅ Created JSONL batch file: {batch_file_path} with {valid_documents} valid documents")
        return batch_file_path
        
    def upload_and_submit_batch(self, batch_file: Path):
        """Uploads JSONL and submits OpenAI Batch API job."""
        try:
            # Upload file
            with open(batch_file, "rb") as file:
                response = openai.files.create(file=file, purpose="batch")
    
            file_id = response.id
            logger.info(f"📤 Uploaded JSONL file. File ID: {file_id}")
    
            # Submit batch
            batch_response = openai.batches.create(
                input_file_id=file_id,
                endpoint="/v1/chat/completions",
                completion_window="24h"
            )
    
            batch_id = batch_response.id
            logger.info(f"🚀 Batch job submitted! Batch ID: {batch_id}")
    
            return batch_id
    
        except Exception as e:
            logger.error(f"❌ Batch processing failed: {e}")
            return None

def process_large_batches(limit=10000, max_tokens_per_batch=75000, max_docs_per_batch=50):
    """Processes documents in smaller batches to stay within token limits."""
    try:
        processor_instance = BatchDocumentProcessor(batch_size=max_docs_per_batch)  # Reduce batch size

        # Fetch documents from clean stage
        documents = processor.get_documents_for_stage(current_stage="clean", status="completed", limit=limit)

        if not documents:
            logger.warning("⚠ No documents found for batch processing.")
            return

        batch_id_list = []
        current_tokens = 0
        batch_docs = []

        for doc in documents:
            cleaned_doc = processor_instance.find_cleaned_document(doc["id"])
            if not cleaned_doc:
                continue

            doc_tokens = len(cleaned_doc["cleaned_content"].split())  # Approximate token count
            if current_tokens + doc_tokens > max_tokens_per_batch or len(batch_docs) >= max_docs_per_batch:
                # Process current batch and reset
                batch_filename = f"batch_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
                batch_file_path = processor_instance.create_jsonl_file(batch_docs, batch_filename)
                batch_id = processor_instance.upload_and_submit_batch(batch_file_path)
                batch_id_list.append(batch_id)

                # Reset for next batch
                batch_docs = []
                current_tokens = 0

            batch_docs.append(doc)
            current_tokens += doc_tokens

        # Process remaining batch
        if batch_docs:
            batch_filename = f"batch_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
            batch_file_path = processor_instance.create_jsonl_file(batch_docs, batch_filename)
            batch_id = processor_instance.upload_and_submit_batch(batch_file_path)
            batch_id_list.append(batch_id)

        logger.info(f"🚀 Successfully submitted {len(batch_id_list)} batches.")

    except Exception as e:
        logger.error(f"❌ Batch processing failed: {e}")
        
def main():
    """CLI interface for batch processing."""
    parser = argparse.ArgumentParser(description="Batch Document Processor using OpenAI API")
    parser.add_argument("--limit", "-l", type=int, default=10000, help="Max documents to process")
    
    args = parser.parse_args()
    process_large_batches(limit=args.limit)

if __name__ == "__main__":
    main()