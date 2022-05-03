import json
from dataclasses import dataclass

from dacite import from_dict


@dataclass
class FiwareConfig:
    endpoint: str
    service: str
    servicepath: str
    node_type: str
    link_type: str
    limit: int


@dataclass
class Config:
    fiware_config: FiwareConfig


def parse_config(config_path):
    with open(config_path, mode="r") as f:
        d = json.load(f)
    return from_dict(data_class=Config, data=d)
