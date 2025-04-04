from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel

from .phase_registry import PhaseConfig


class WorkflowType(BaseModel):
    """Workflow type configuration"""

    type_code: str
    name: str
    description: str
    phases: List[PhaseConfig]


class WorkflowRegistry:
    """Registry for workflow types"""

    def __init__(self):
        self._workflows: Dict[str, WorkflowType] = {}

    async def get_workflow(self, type_code: str) -> Optional[WorkflowType]:
        """Get workflow by type code"""
        return self._workflows.get(type_code)

    async def register_workflow(self, workflow: WorkflowType):
        """Register new workflow type"""
        self._workflows[workflow.type_code] = workflow

    async def identify_workflow_type(self, description: str) -> str:
        """Identify appropriate workflow type"""
        # TODO: Implement AI-based matching
        return list(self._workflows.keys())[0] if self._workflows else None
