import os
from trains import Task
from dataclasses import dataclass


# hydra config
@dataclass
class AppConfig:
    task_name: str = os.path.basename(__file__)
    task_project: str = "hydra_project"
    a_parameter: int = 0


def main(config: AppConfig):
    Task.init(config.task_project,config.task_name)


if __name__ == "__main__":
    main(AppConfig())
