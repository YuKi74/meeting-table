from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent.parent


class Config:
    def __init__(self, **config):
        self.app_config = AppConfig(**config['app_config'])
        self.mysql_config = MysqlConfig(**config['mysql_config'])


class AppConfig:
    def __init__(self, **config):
        self.log_path = config['log_path']
        self.meeting_room_server = config['meeting_room_server']
        self.meeting_room_server_url = config['meeting_room_server_url']
        self.file_path = config['file_path']


class MysqlConfig:
    def __init__(self, **config):
        self.user = config['user']
        self.password = str(config['password'])
        self.host = config['host']
        self.name = config['name']


config: Config

with open(BASE_DIR/'config.yaml') as f:
    config_yaml = yaml.load(f.read(), Loader=yaml.SafeLoader)
    config = Config(**config_yaml)
