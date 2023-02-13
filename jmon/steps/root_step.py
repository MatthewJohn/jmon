

from jmon.steps.base_step import BaseStep
import jmon.steps


class RootStep(BaseStep):

    SUPPORTED_CHILD_STEPS = [
        jmon.steps.GotoStep
    ]

