#!/usr/bin/env python

import argparse

from viewer import strategies
from viewer.config import parse_config
from viewer.parser import parse_data
from viewer.renderer import MapRenderer


def parse_args():
    parser = argparse.ArgumentParser(description="pedestrian walkway graph viewer")
    parser.add_argument("map_path", help="map file path")
    parser.add_argument("-c", "--config", default="viewer_config.json", help="viewer config json file path")
    parser.add_argument(
        "-s", "--strategy", choices=["all", "class1", "class2", "class3"], default="all", help="strategy to connect a link"
    )
    return parser.parse_args()


def get_strategy(strategy):
    match (strategy):
        case "class1":
            return strategies.connect_class1
        case "class2":
            return strategies.connect_class2
        case "class3":
            return strategies.connect_class3
        case _:
            return strategies.connect_all


def main(args):
    config = parse_config(args.config)
    strategy = get_strategy(args.strategy)
    size, nodes, links = parse_data(config, strategy)
    MapRenderer(config, size).render(nodes, links, args.map_path)


if __name__ == "__main__":
    args = parse_args()
    main(args)
