#!/usr/bin/env python

import argparse

from viewer.config import parse_config
from viewer.parser import parse_data


def parse_args():
    parser = argparse.ArgumentParser(description="pedestrian walkway graph viewer")
    parser.add_argument("-c", "--config", default="viewer_config.json", help="viewer config json file path")
    return parser.parse_args()


def main(args):
    config = parse_config(args.config)
    parse_data(config)


if __name__ == "__main__":
    args = parse_args()
    main(args)
