import json
from dataclasses import dataclass


@dataclass
class Config:
    fiware_endpoint: str
    fiware_service: str
    fiware_servicepath: str


def parse_config(config_path):
    with open(config_path, mode="r") as f:
        d = json.load(f)
    return Config(**d)
