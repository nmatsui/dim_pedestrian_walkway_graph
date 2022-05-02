#!/usr/bin/env python

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="preprocess command to import data into FIWARE")
    parser.add_argument("data_path", help="path of config json file")
    parser.add_argument("-t", "--type", choices=["node", "link"], required=True, help="data type")
    parser.add_argument("-c", "--config", default="default_config.json", help="data type")
    return parser.parse_args()


def main(args):
    print(args)


if __name__ == "__main__":
    args = parse_args()
    main(args)
