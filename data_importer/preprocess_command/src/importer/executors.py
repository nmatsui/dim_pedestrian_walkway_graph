import csv
from abc import ABCMeta, abstractmethod


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
        print(row)


class LinkCSVExecutor(CSVExecutor):
    def _process(self, row):
        print(row)


def get_executor(executor_type, format_type):
    match (executor_type, format_type):
        case ("node", "csv"):
            return NodeCSVExecutor
        case ("link", "csv"):
            return LinkCSVExecutor
        case _:
            raise NotImplementedError()
