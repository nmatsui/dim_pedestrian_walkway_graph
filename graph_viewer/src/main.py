#!/usr/bin/env python

import argparse

from viewer.config import parse_config
from viewer.parser import parse_data
from viewer.renderer import MapRenderer


def parse_args():
    parser = argparse.ArgumentParser(description="pedestrian walkway graph viewer")
    parser.add_argument("map_path", help="map file path")
    parser.add_argument("-c", "--config", default="viewer_config.json", help="viewer config json file path")
    return parser.parse_args()


def main(args):
    config = parse_config(args.config)
    size, nodes, links = parse_data(config)
    MapRenderer(config, size).render(nodes, links, args.map_path)


if __name__ == "__main__":
    args = parse_args()
    main(args)
