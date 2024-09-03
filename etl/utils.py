import yaml


def load_db_config(config_file="config.yaml"):
    """
    Load DB config.yaml
    """
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config


def get_db_uri(db_config):
    # 불러온 설정을 사용하여 DB URI 생성
    db_uri = (
        f"{db_config['database']['type']}+{db_config['database']['connector']}://"
        f"{db_config['database']['username']}:{db_config['database']['password']}@"
        f"{db_config['database']['host']}:{db_config['database']['port']}/"
        f"{db_config['database']['db_name']}"
    )

    return db_uri
