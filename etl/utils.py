import yaml


def load_db_config(config_file="config.yaml"):
    """
    Load DB config.yaml
    """
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config
