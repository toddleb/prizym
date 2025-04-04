from datetime import datetime
from enum import Enum
from typing import Any, Dict


class PhaseStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ProjectTimeline:
    """Tracks project execution timeline"""

    def __init__(self):
        self.phases: Dict[str, Dict[str, Any]] = {}
        self.start_time = datetime.now()

    async def start_phase(self, phase_name: str):
        """Start a phase"""
        self.phases[phase_name] = {
            "status": PhaseStatus.IN_PROGRESS,
            "start_time": datetime.now(),
        }

    async def complete_phase(self, phase_name: str, result: Dict[str, Any] = None):
        """Complete a phase"""
        if phase_name in self.phases:
            self.phases[phase_name].update(
                {
                    "status": PhaseStatus.COMPLETED,
                    "end_time": datetime.now(),
                    "result": result,
                }
            )

    async def fail_phase(self, phase_name: str, error: str):
        """Mark phase as failed"""
        if phase_name in self.phases:
            self.phases[phase_name].update(
                {
                    "status": PhaseStatus.FAILED,
                    "end_time": datetime.now(),
                    "error": error,
                }
            )
