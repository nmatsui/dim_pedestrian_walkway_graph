import requests


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


def parse_data(config):
    i = 1
    node_itr = NGSIIterator(config, config.fiware_config.node_type)
    for ngsi_node in node_itr:
        print(f"{i:5}: Node [{ngsi_node['id']}]")
        i += 1

    j = 1
    link_itr = NGSIIterator(config, config.fiware_config.link_type)
    for ngsi_link in link_itr:
        print(f"{j:5}: Link [{ngsi_link['id']}]")
        j += 1
