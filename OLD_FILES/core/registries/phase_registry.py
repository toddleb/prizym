"""
Phase Registry for Workflow Management
"""

import logging
from typing import Any, Dict, Type

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class PhaseConfig(BaseModel):
    """Phase configuration"""

    phase_number: int
    phase_name: str
    description: str
    required_capabilities: list[str]
    prompt_template: str


class BasePhase:
    """Base class for workflow phases"""

    def __init__(self, config: PhaseConfig):
        """Initialize phase with configuration"""
        self.config = config

    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute phase"""
        raise NotImplementedError("Subclasses must implement execute method")


class PhaseRegistry:
    """Registry for workflow phases"""

    _phases: Dict[str, Type[BasePhase]] = {}

    @classmethod
    def register(cls, phase_name: str, phase_class: Type[BasePhase]):
        """Register a phase"""
        cls._phases[phase_name] = phase_class
        print(f"✅ Registered phase: {phase_name}")

    @classmethod
    def get_phase(cls, phase_name: str):
        """Retrieve a registered phase"""
        return cls._phases.get(phase_name)


def get_phase_sequence():
    """
    Retrieves the sequence of workflow phases from the database or default config.
    """
    return [
        "Code Generation",
        "Automated Testing",
        "Bug Fixing",
        "Career Pathing Engine",
        "Job Matching",
        "Scholarship Finder",
        "Lead Scoring & Prioritization",
        "Personalized Email Sequences",
        "AI Chatbots & Conversational Sales",
        "Sales Forecasting & Trend Analysis",
        "Quota & Compensation Optimization",
        "AI-Powered Sales Coaching",
        "Employee Retention Analysis",
        "Workforce Performance Benchmarking",
        "AI-Optimized Hiring Recommendations",
    ]


# ✅ Import `phase_loader.py` to register phases dynamically
import core.registries.phase_loader  # ✅ Loads phases dynamically at runtime
