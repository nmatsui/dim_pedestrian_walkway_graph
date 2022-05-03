import sys

import requests

from viewer import models
from viewer.utils import CoordTransformer


class NGSIIterator:
    def __init__(self, config, type):
        self.config = config
        self.type = type
        self._offset = 0
        self._buf = []

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._buf) > 0:
            return self._buf.pop(0)

        headers = {
            "fiware-service": self.config.fiware_config.service,
            "fiware-servicepath": self.config.fiware_config.servicepath,
        }
        q = {
            "type": self.type,
            "limit": self.config.fiware_config.limit,
            "offset": self._offset,
        }
        result = requests.get(self.config.fiware_config.endpoint, headers=headers, params=q).json()
        if len(result) == 0:
            raise StopIteration()
        self._offset += self.config.fiware_config.limit
        self._buf = result
        return self._buf.pop(0)


def parse_data(config, strategy):
    transformer = CoordTransformer(config)

    nodes = dict()
    for ngsi_node in NGSIIterator(config, config.fiware_config.node_type):
        node = models.Node(
            ngsi_node["id"],
            float(ngsi_node["lat"]["value"]),
            float(ngsi_node["lon"]["value"]),
            float(ngsi_node["floor"]["value"]),
            models.InOut(int(ngsi_node["in_out"]["value"])),
        )
        node.transform(transformer)
        nodes[node.node_id] = node

    links = list()
    for ngsi_link in NGSIIterator(config, config.fiware_config.link_type):
        if ngsi_link["start_id"]["value"] not in nodes or ngsi_link["end_id"]["value"] not in nodes:
            print(f"skipped link, {ngsi_link['id']}", file=sys.stderr)
            continue

        link = models.Link(
            ngsi_link["id"],
            nodes[ngsi_link["start_id"]["value"]],
            nodes[ngsi_link["end_id"]["value"]],
            float(ngsi_link["distance"]["value"]),
            models.RouteStructure(int(ngsi_link["rt_struct"]["value"])),
            models.RouteType(int(ngsi_link["route_type"]["value"])),
            models.Direction(int(ngsi_link["direction"]["value"])),
            models.Width(int(ngsi_link["width"]["value"])),
            models.Gradient(int(ngsi_link["vtcl_slope"]["value"])),
            models.Step(int(ngsi_link["lev_diff"]["value"])),
            models.PedestriansSignals(int(ngsi_link["tfc_signal"]["value"])),
            models.PedestriansSignalsType(int(ngsi_link["tfc_s_type"]["value"])),
            models.TactileTile(int(ngsi_link["brail_tile"]["value"])),
            models.ElevatorType(int(ngsi_link["elevator"]["value"])),
            models.Roof(int(ngsi_link["roof"]["value"])),
        )
        if strategy(link):
            links.append(link)

    size = transformer.get_mapsize()

    return size, nodes, links
