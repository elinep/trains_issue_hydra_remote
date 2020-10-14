import os
from trains import Task
import hydra
from hydra.core.config_store import ConfigStore
from dataclasses import dataclass
import os


# hydra config
@dataclass
class AppConfig:
    task_name: str = os.path.basename(__file__)
    task_project: str = "hydra_project"
    a_parameter: int = 0


# register config
cs = ConfigStore.instance()
cs.store(name="config", node=AppConfig)


def fix_hydra(task):
    # TODO: seems there might be synchronization issue as script informations are filled by a thread
    print("trains working dir after sleep {}".format(task.data.script.working_dir))
    print("trains entry point after sleep {}".format(task.data.script.entry_point))

    # trains conf
    current_working_dir = task.data.script.working_dir
    current_entry_point = task.data.script.entry_point
    # current path
    current_cwd = os.getcwd()
    # original current path before hydra kicked in
    original_cwd = hydra.utils.get_original_cwd()

    # get base dir according to trains
    trains_base_dir = current_cwd.split(current_working_dir)[0]
    script_abs_path = os.path.normpath(os.path.join(current_cwd, current_entry_point))
    real_working_dir = os.path.relpath(original_cwd, trains_base_dir)
    real_entry_point = os.path.relpath(
        script_abs_path, os.path.join(trains_base_dir, real_working_dir)
    )
    print("trains patch working dir {}".format(real_working_dir))
    print("trains patch entry point {}".format(real_entry_point))

    # update task
    update_task_data = {
        "script": {"entry_point": real_entry_point, "working_dir": real_working_dir}
    }
    task.update_task(update_task_data)


@hydra.main(config_name="config")
def main(config: AppConfig):
    task = Task.init(config.task_project,config.task_name)
    fix_hydra(task)


if __name__ == "__main__":
    main()
