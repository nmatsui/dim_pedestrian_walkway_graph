#!/usr/bin/env python

import argparse

from importer.config import parse_config


def parse_args():
    parser = argparse.ArgumentParser(description="preprocess command to import data into FIWARE")
    parser.add_argument("data_path", help="path of config json file")
    parser.add_argument("-t", "--type", choices=["node", "link"], required=True, help="data type")
    parser.add_argument("-c", "--config", default="default_config.json", help="data type")
    parser.add_argument("-f", "--format", choices=["csv"], default="csv", help="data type")
    return parser.parse_args()


def main(args):
    config = parse_config(args.config)
    print(config)


if __name__ == "__main__":
    args = parse_args()
    main(args)
