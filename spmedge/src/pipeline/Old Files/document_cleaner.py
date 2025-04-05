#!/usr/bin/env python3
"""
Document Cleaner - Third stage of the document processing pipeline.
- Applies dynamic cleaning based on database rules
- Moves documents from stage_load to stage_clean
- Ensures pipeline consistency with batch processing
"""

import os
import sys
import json
import logging
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Fix the import path issue - use absolute imports
sys.path.insert(0, '/Users/toddlebaron/prizym/spmedge')

# Import pipeline components
from config.config import config
from src.pipeline.db_integration import DBManager
from src.pipeline.pipeline_processor import PipelineProcessor, PipelineStage

# Logging setup
LOG_FILE = os.path.join(config.LOG_DIR, "document_cleaner.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE, encoding="utf-8")],
)
logger = logging.getLogger("document_cleaner")

# Initialize pipeline components
processor = PipelineProcessor(PipelineStage.CLEAN)
db_manager = DBManager()


def fetch_cleaning_patterns() -> List[Dict[str, Any]]:
    """Fetch active cleaning patterns from the database."""
    try:
        db_manager.cursor.execute("""
            SELECT pattern, replacement, pattern_type 
            FROM cleaning_patterns 
            WHERE active = true 
            ORDER BY sort_order ASC;
        """)
        patterns = db_manager.cursor.fetchall()

        return [{"pattern": row[0], "replacement": row[1], "type": row[2]} for row in patterns]
    
    except Exception as e:
        logger.error(f"❌ Error fetching cleaning patterns: {e}")
        return []


def apply_minimal_cleaning(text: str) -> str:
    """Applies dynamic cleaning rules from the database."""
    
    # Ensure UTF-8 encoding
    text = text.encode("utf-8", "ignore").decode("utf-8", "ignore")

    # Fetch cleaning rules from DB
    cleaning_rules = fetch_cleaning_patterns()

    for rule in cleaning_rules:
        pattern = rule["pattern"]
        replacement = rule["replacement"]
        pattern_type = rule["type"]

        if pattern_type == "regex":
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
        elif pattern_type == "exact":
            text = text.replace(pattern, replacement)

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def get_document_content(document_id: str, doc: Dict, content_dir: Path) -> str:
    """Finds and extracts document content using the correct naming pattern."""

    # Match based on loader's naming pattern
    doc_id_short = document_id.replace("-", "")[:12]  # Get first 12 characters without dashes
    matching_files = list(content_dir.glob(f"pipeline_load_doc{doc_id_short}*.json"))

    if not matching_files:
        logger.error(f"❌ No content file found for document {document_id} in {content_dir}")
        logger.info(f"📂 Available files: {list(content_dir.glob('*'))}")  # Debugging
        return ""

    content_file = matching_files[0]  # Take the first match
    logger.info(f"🔎 Found content file: {content_file}")

    try:
        with open(content_file, "r", encoding="utf-8") as f:
            data = json.load(f)  # Assuming JSON structure
            return data.get("content", "").strip()  # Extract text content

    except Exception as e:
        logger.error(f"⚠️ Error reading {content_file}: {e}")
        return ""


def clean_documents(limit: int = 500):
    """Process documents and apply minimal cleaning."""
    documents = processor.get_documents_for_stage(current_stage="load", status="completed", limit=limit)

    if not documents:
        logger.warning("⚠️ No documents ready for cleaning")
        return

    batch_name = f"clean_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    batch_id = processor.record_batch_processing(batch_name=batch_name, document_count=len(documents), status="processing")

    # Get directory paths
    dirs = processor.get_base_dirs()
    content_dir = dirs["stage_load"]  # Source files come from the "load" stage
    clean_dir = dirs["stage_clean"]   # Save cleaned files in "clean"

    cleaned_documents = []
    failures = 0

    for doc in documents:
        document_id = doc["id"]
        logger.info(f"🔍 Cleaning document {document_id}")

        content = get_document_content(document_id, doc, content_dir)

        if not content:
            failures += 1
            processor.update_document_stage(document_id=document_id, status="failed", error_message="No content found", batch_id=batch_id)
            continue

        cleaned_text = apply_minimal_cleaning(content)

        # Generate a cleaned filename following the pipeline convention
        new_filename = processor.generate_stage_filename(
            original_filename=doc.get("name", f"doc_{document_id}.txt"),
            document_id=document_id,
            batch_id=batch_id
        )

        # Save cleaned content
        clean_file_path = clean_dir / new_filename
        with open(clean_file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        cleaned_documents.append({
            "id": document_id,
            "original_filename": doc.get("original_filename"),
            "pipeline_filename": new_filename,
            "cleaned_content_length": len(cleaned_text),
            "pipeline_stage": "clean",
            "batch_id": batch_id,
            "status": "completed",
        })

        logger.info(f"✅ Document {document_id} cleaned ({len(cleaned_text)} chars)")

    # Batch update
    if cleaned_documents:
        processor.save_document_batch(cleaned_documents, batch_name=batch_name)
        processor.finalize_batch(batch_id, "completed")
        logger.info(f"✅ Cleaning complete: {len(cleaned_documents)} success, {failures} failed")
    else:
        processor.finalize_batch(batch_id, "failed")
        logger.warning("⚠️ No documents were successfully cleaned")


def main():
    """CLI Entry point."""
    parser = argparse.ArgumentParser(description="Minimal Document Cleaner")
    parser.add_argument("--limit", "-l", type=int, default=500, help="Max documents to process")

    args = parser.parse_args()
    clean_documents(limit=args.limit)


if __name__ == "__main__":
    main()