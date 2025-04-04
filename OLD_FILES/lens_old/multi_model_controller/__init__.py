# multi_model_controller/__init__.py
"""
Multi-Model Controller (MMC) - Handles AI model routing, queries, and integration.
"""

# Import AI Query Service (formerly ai_query_service)
from .ai_query_service.main import process_ai_query

# Import Model Router (if exists)
try:
    from .model_router import route_query
except ImportError:
    route_query = None  # Handle gracefully if missing

# Import Utility Functions (if needed)
try:
    from .utils import log_request, log_response
except ImportError:
    log_request = log_response = lambda x: None  # No-op if missing

# Expose key MMC functions for easy access
__all__ = ["process_ai_query", "route_query", "log_request", "log_response"]
