from enum import Enum

from gpt_all_star.core.steps.steps import StepType


class ExtendedStepType(Enum):
    NONE = StepType.NONE
    DEFAULT = StepType.DEFAULT
    BUILD = StepType.BUILD
    SPECIFICATION = StepType.SPECIFICATION
    SPECIFICATION_IMPROVE = "specification_improve"
    SYSTEM_DESIGN = StepType.SYSTEM_DESIGN
    SYSTEM_DESIGN_IMPROVE = "system_design_improve"
    UI_DESIGN = StepType.UI_DESIGN
    UI_DESIGN_IMPROVE = "ui_design_improve"
    DEVELOPMENT = StepType.DEVELOPMENT
    QUALITY_ASSURANCE = StepType.QUALITY_ASSURANCE
    ENTRYPOINT = StepType.ENTRYPOINT
    HEALING = StepType.HEALING
    NOT_STARTED = "not_started"
    EXECUTION = "execution"
    FINISHED = "finished"

    @property
    def display_name(self):
        return {
            ExtendedStepType.NONE: "Only Execution",
            ExtendedStepType.DEFAULT: "From Scratch",
            ExtendedStepType.BUILD: "Build",
            ExtendedStepType.SPECIFICATION: "Specification",
            ExtendedStepType.SPECIFICATION_IMPROVE: "Specification Refinement",
            ExtendedStepType.SYSTEM_DESIGN: "System Design",
            ExtendedStepType.SYSTEM_DESIGN_IMPROVE: "System Design Refinement",
            ExtendedStepType.UI_DESIGN: "UI Design",
            ExtendedStepType.UI_DESIGN_IMPROVE: "UI Design Refinement",
            ExtendedStepType.DEVELOPMENT: "Development",
            ExtendedStepType.QUALITY_ASSURANCE: "Quality Assurance",
            ExtendedStepType.ENTRYPOINT: "Development",
            ExtendedStepType.HEALING: "Healing",
            ExtendedStepType.NOT_STARTED: "Not Started",
            ExtendedStepType.EXECUTION: "Execution",
            ExtendedStepType.FINISHED: "Finished",
        }[self]


def get_steps(step_type: str):
    if step_type == ExtendedStepType.DEFAULT.display_name:
        return [
            ExtendedStepType.SPECIFICATION,
            ExtendedStepType.SPECIFICATION_IMPROVE,
            ExtendedStepType.SYSTEM_DESIGN,
            ExtendedStepType.SYSTEM_DESIGN_IMPROVE,
            ExtendedStepType.UI_DESIGN,
            ExtendedStepType.UI_DESIGN_IMPROVE,
            ExtendedStepType.DEVELOPMENT,
            ExtendedStepType.ENTRYPOINT,
            ExtendedStepType.QUALITY_ASSURANCE,
            ExtendedStepType.EXECUTION,
        ]
    elif step_type == ExtendedStepType.BUILD.display_name:
        return [
            ExtendedStepType.DEVELOPMENT,
            ExtendedStepType.ENTRYPOINT,
            ExtendedStepType.QUALITY_ASSURANCE,
            ExtendedStepType.EXECUTION,
        ]
    elif step_type == ExtendedStepType.NONE.display_name:
        return [
            ExtendedStepType.EXECUTION,
        ]
    else:
        raise ValueError(f"Invalid step type: {step_type}")
