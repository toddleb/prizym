import json
import logging
from datetime import datetime
import asyncpg
from core.security.credential_manager import SecureCredentialManager

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Handles database connections and queries."""

    def __init__(self):
        self._pool = None  # ✅ Use a connection pool

    async def setup_pool(self):
        """Initialize a database connection pool."""
        if self._pool is None:
            db_name = SecureCredentialManager.get_credential("postgres", "db_name")
            db_user = SecureCredentialManager.get_credential("postgres", "db_user")
            db_password = SecureCredentialManager.get_credential(
                "postgres", "db_password"
            )
            db_host = SecureCredentialManager.get_credential("postgres", "db_host")
            db_port = SecureCredentialManager.get_credential("postgres", "db_port")

            if not all([db_name, db_user, db_password, db_host, db_port]):
                logging.error("❌ Missing database credentials in macOS Keychain.")
                raise ValueError(
                    "Database credentials are missing! Run `setup_credentials()`."
                )

            self._pool = await asyncpg.create_pool(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
                min_size=5,
                max_size=20,
            )
            logger.info("✅ Database connection pool initialized.")

    async def get_db_connection(self):
        """Get a connection from the pool."""
        if self._pool is None:
            await self.setup_pool()  # ✅ Ensure the pool is ready
        return self._pool

    async def close_pool(self):
        """Close the database connection pool when done."""
        if self._pool:
            await self._pool.close()
            self._pool = None
            logger.info("🚪 Database connection pool closed.")


# ✅ Create a global database manager instance
db_manager = DatabaseManager()
