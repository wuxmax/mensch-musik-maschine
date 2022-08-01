
import yaml


def load_config(yaml_file: str = 'config.yml'):
    with open(yaml_file, 'r') as stream:
        try:
            config=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    return config


def parse_arguments(args: list[str]) -> bool:
    if len(args) > 1 and args[1] == 'sleep':
        return True
    return False
