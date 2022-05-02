import csv
from abc import ABCMeta, abstractmethod

from importer.models import Link, Node


class Executor(metaclass=ABCMeta):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def execute(self, data_path):
        raise NotImplementedError()


class CSVExecutor(Executor):
    def execute(self, data_path):
        with open(data_path, mode="r", newline="") as f:
            for row in csv.DictReader(f, skipinitialspace=True):
                self._process(row)

    @abstractmethod
    def _process(self, row):
        pass


class NodeCSVExecutor(CSVExecutor):
    def _process(self, row):
        node = Node(**{k: v for k, v in row.items() if k in Node.get_fields()})
        print(node)


class LinkCSVExecutor(CSVExecutor):
    def _process(self, row):
        link = Link(**{k: v for k, v in row.items() if k in Link.get_fields()})
        print(link)


def get_executor(executor_type, format_type):
    match (executor_type, format_type):
        case ("node", "csv"):
            return NodeCSVExecutor
        case ("link", "csv"):
            return LinkCSVExecutor
        case _:
            raise NotImplementedError()
