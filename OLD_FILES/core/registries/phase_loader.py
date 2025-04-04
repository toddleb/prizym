import asyncio
import logging

from core.database import get_db_connection

logger = logging.getLogger(__name__)


async def register_phases_from_db():
    """Fetch and register workflow phases dynamically from the database."""
    conn = await get_db_connection()
    async with conn.transaction():
        rows = await conn.fetch("SELECT phase_name FROM workflow_phases")
        phase_names = [row["phase_name"] for row in rows]

    logger.info(f"📌 Found Phases in Database: {phase_names}")


async def init():
    """Initialize phase loading dynamically."""
    await register_phases_from_db()


# ✅ Fix async loop handling
def run_phase_loader():
    """Ensure correct async execution within an existing event loop"""
    loop = None
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        pass

    if loop and loop.is_running():
        loop.create_task(init())  # ✅ Run inside an existing event loop
    else:
        asyncio.run(init())  # ✅ Start a new event loop if none exists


def load_phase(phase_name):
    """
    Dynamically loads a workflow phase by name.
    """
    module_name = f"core.phases.{phase_name.lower().replace(' ', '_')}"
    try:
        module = __import__(module_name, fromlist=[phase_name])
        return getattr(module, phase_name)
    except (ModuleNotFoundError, AttributeError):
        raise ImportError(f"Phase '{phase_name}' not found in {module_name}")


# ✅ Execute phase loader
run_phase_loader()
