import pathlib

import platformdirs


def config_path(project_name):
    d = pathlib.Path(platformdirs.user_config_dir(project_name))
    return d / "config.json"
