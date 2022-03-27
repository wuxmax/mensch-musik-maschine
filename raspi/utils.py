
import yaml


def load_config(yaml_file: str):
    with open(yaml_file, 'r') as stream:
        try:
            config=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    return config