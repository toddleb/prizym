import logging
import asyncpg
from functools import wraps

logger = logging.getLogger(__name__)


def db_error_handler(func):
    """Decorator to handle database errors consistently."""

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except asyncpg.PostgresError as e:
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise

    return wrapper
