

from enum import Enum


class StepStatus(Enum):
    """Status of a step"""

    NOT_RUN = "NOT_RUN"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
