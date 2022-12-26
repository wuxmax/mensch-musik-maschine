from pathlib import Path

import yaml
from typing import List


def load_config(yaml_file: str = 'config.yml'):
    with open(Path(__file__).parent / 'configs'/ yaml_file, 'r') as stream:
        try:
            config=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    return config


def parse_arguments(args: List[str]) -> bool:
    if len(args) > 1 and args[1] == 'sleep':
        return True
    return False
