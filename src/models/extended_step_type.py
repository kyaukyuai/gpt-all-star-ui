from enum import Enum

from gpt_all_star.core.steps.steps import StepType


class ExtendedStepType(Enum):
    NONE = StepType.NONE
    DEFAULT = StepType.DEFAULT
    BUILD = StepType.BUILD
    SPECIFICATION = StepType.SPECIFICATION
    SPECIFICATION_CHECK = "specification_check"
    SPECIFICATION_IMPROVE = "specification_improve"
    SYSTEM_DESIGN = StepType.SYSTEM_DESIGN
    SYSTEM_DESIGN_CHECK = "system_design_check"
    SYSTEM_DESIGN_IMPROVE = "system_design_improve"
    DEVELOPMENT = StepType.DEVELOPMENT
    ENTRYPOINT = StepType.ENTRYPOINT
    UI_DESIGN = StepType.UI_DESIGN
    HEALING = StepType.HEALING
    NOT_STARTED = "not_started"
    EXECUTION = "execution"
    FINISHED = "finished"


def get_steps(step_type: str):
    if step_type == ExtendedStepType.DEFAULT.name:
        return [
            ExtendedStepType.SPECIFICATION,
            ExtendedStepType.SPECIFICATION_CHECK,
            ExtendedStepType.SYSTEM_DESIGN,
            ExtendedStepType.SYSTEM_DESIGN_CHECK,
            ExtendedStepType.DEVELOPMENT,
            ExtendedStepType.UI_DESIGN,
            ExtendedStepType.ENTRYPOINT,
            ExtendedStepType.EXECUTION,
        ]
    elif step_type == ExtendedStepType.BUILD.name:
        return [
            ExtendedStepType.DEVELOPMENT,
            ExtendedStepType.UI_DESIGN,
            ExtendedStepType.ENTRYPOINT,
            ExtendedStepType.EXECUTION,
        ]
    else:
        return [ExtendedStepType.EXECUTION]
