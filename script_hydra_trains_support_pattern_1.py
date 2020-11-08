import os
from trains import Task
import hydra
from hydra.core.config_store import ConfigStore
from dataclasses import dataclass


# hydra config
@dataclass
class AppConfig:
    task_name: str = os.path.basename(__file__)
    task_project: str = "hydra_project"
    a_parameter: int = 0


# register config
cs = ConfigStore.instance()
cs.store(name="config", node=AppConfig)


@hydra.main(config_name="config")
def main(config: AppConfig):
    Task.init(config.task_project, config.task_name)
    print("config is:")
    print(config)


# see https://github.com/allegroai/trains/issues/219#issuecomment-723503923
if __name__ == "__main__":
    main()
