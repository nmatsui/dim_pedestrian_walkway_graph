import csv
import sys
from abc import ABCMeta, abstractmethod
from os import path

import requests
from jinja2 import Environment, FileSystemLoader

from importer.models import Link, Node


class Executor(metaclass=ABCMeta):
    def __init__(self, config):
        self.config = config
        templates_path = path.join(path.dirname(__file__), "../templates")
        self.env = Environment(loader=FileSystemLoader(templates_path, encoding="utf8"))

    @abstractmethod
    def execute(self, data_path):
        raise NotImplementedError()

    def post(self, body, id, type):
        headers = {
            "fiware-service": self.config.fiware_service,
            "fiware-servicepath": self.config.fiware_servicepath,
            "content-type": "application/json",
        }
        res = requests.post(self.config.fiware_endpoint, headers=headers, data=body)
        if res.status_code != 201:
            print(f"An error raised, id={id}, type={type}, status_code={res.status_code}, msg={res.text}", file=sys.stderr)


class CSVExecutor(Executor):
    def execute(self, data_path):
        with open(data_path, mode="r", newline="") as f:
            for row in csv.DictReader(f, skipinitialspace=True):
                self._process(row)

    @abstractmethod
    def _process(self, row):
        pass


class NodeCSVExecutor(CSVExecutor):
    def __init__(self, config):
        super().__init__(config)
        self.template = self.env.get_template("node_entity.j2")

    def _process(self, row):
        node = Node(**{k: v for k, v in row.items() if k in Node.get_fields()})
        body = self.template.render(node=node)
        self.post(body, id=node.node_id, type="Node")


class LinkCSVExecutor(CSVExecutor):
    def __init__(self, config):
        super().__init__(config)
        self.template = self.env.get_template("link_entity.j2")

    def _process(self, row):
        link = Link(**{k: v for k, v in row.items() if k in Link.get_fields()})
        body = self.template.render(link=link)
        self.post(body, id=link.link_id, type="Link")


def get_executor(executor_type, format_type):
    match (executor_type, format_type):
        case ("node", "csv"):
            return NodeCSVExecutor
        case ("link", "csv"):
            return LinkCSVExecutor
        case _:
            raise NotImplementedError()
