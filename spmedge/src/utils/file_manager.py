from pathlib import Path  # Add this import
import shutil
from config.config import config

def move_file(file_path: str, destination_dir: str) -> str:
    """Move a file to the specified directory."""
    source = Path(file_path).expanduser()  # Expand tilde (~)
    destination = Path(destination_dir).expanduser() / source.name

    if source.exists():
        shutil.move(str(source), str(destination))
        return str(destination)
    else:
        raise FileNotFoundError(f"File not found: {source}")

def archive_file(file_path: str) -> str:
    """Move file to archive after processing."""
    return move_file(file_path, config.ARCHIVE_DIR)

def finalize_processed_file(file_path: str) -> str:
    """Move file to processed directory after AI processing."""
    return move_file(file_path, config.PROCESSED_DOCS_DIR)

# Example Usage
if __name__ == "__main__":
    test_file = Path(config.NEW_DOCS_DIR).expanduser() / "test_document.pdf"
    print(f"Moving {test_file} to processed docs...")
    print(finalize_processed_file(str(test_file)))