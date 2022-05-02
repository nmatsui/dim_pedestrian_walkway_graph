#!/usr/bin/env python

import argparse

from importer.config import parse_config
from importer.executors import get_executor


def parse_args():
    parser = argparse.ArgumentParser(description="preprocess command to import data into FIWARE")
    parser.add_argument("data_path", help="data file path")
    parser.add_argument("-c", "--config", default="fiware_config.json", help="fiware config json file path")
    parser.add_argument("-t", "--type", choices=["node", "link"], required=True, help="data type")
    parser.add_argument("-f", "--format", choices=["csv"], default="csv", help="format type")
    return parser.parse_args()


def main(args):
    config = parse_config(args.config)
    Executor = get_executor(args.type, args.format)
    Executor(config).execute(args.data_path)


if __name__ == "__main__":
    args = parse_args()
    main(args)
