import json
from dataclasses import dataclass
from typing import List

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
class MapConfig:
    base_origin_latlng: List[float]
    map_bottom_left: List[float]
    map_top_right: List[float]
    resolution: float


@dataclass
class Config:
    fiware_config: FiwareConfig
    map_config: MapConfig


def parse_config(config_path):
    with open(config_path, mode="r") as f:
        d = json.load(f)
    return from_dict(data_class=Config, data=d)
