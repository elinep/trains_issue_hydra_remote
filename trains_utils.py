import sys
import tempfile
from trains import Task
from omegaconf import OmegaConf
from omegaconf.dictconfig import DictConfig
from omegaconf.listconfig import ListConfig
from omegaconf import MISSING


def generate_trains_hyperparameter_dict(config: OmegaConf):
    res_dict = {
        "!WARNING!": """Cloning and editing these hyperparameters will have no effect.
The true hyperparameters are stored in Artifact->Model Configuration
These view has been generated to ease the comparison with other experiments.""",
        "CLI": " ".join(sys.argv),
    }
    return flatten_config(config, prefix="yaml", res_dict=res_dict)


def flatten_config(config: OmegaConf, prefix="", res_dict={}):
    for key in config:
        if key not in config:
            value = MISSING
        else:
            value = config[key]
        if prefix:
            next_prefix = prefix + "." + key
        else:
            next_prefix = key
        if isinstance(value, DictConfig):
            flatten_config(value, next_prefix, res_dict)
        elif isinstance(value, ListConfig):
            # TODO: if this is a list of complex object, this might not be a good representation
            res_dict[next_prefix] = str(value)
        else:
            res_dict[next_prefix] = str(value)
    return res_dict


def update_config(config: OmegaConf):
    """
    Serialize and sync config with trains
    :param config: the config to sync
    :return:
    """
    # expected config_global format
    schema = OmegaConf.structured(config._metadata.object_type)

    # serialize config
    # For config logging we use yaml format (Trains: Artifacts ->  Model configuration)
    # save config in a temp yaml file
    config_global_file = tempfile.NamedTemporaryFile("w+t")
    config_global_file.write(OmegaConf.to_yaml(config))
    config_global_file.flush()
    config_global_file_name = config_global_file.name

    # sync with server if a task has been created
    current_task = Task.current_task()
    if current_task:
        # send yaml to trains server
        config_global_file_name = Task.current_task().connect_configuration(config_global_file_name)

        # for visualization (Trains: Hyperparameters)
        Task.current_task().connect(generate_trains_hyperparameter_dict(config))

    config_back_ = OmegaConf.load(config_global_file_name)
    config_back = OmegaConf.merge(schema, config_back_)

    return config_back
