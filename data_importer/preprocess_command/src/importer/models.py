from dataclasses import dataclass, fields


@dataclass
class Node:
    node_id: str
    lat: float
    lon: float
    floor: float
    in_out: int

    def __post_init__(self):
        self.lat = float(self.lat)
        self.lon = float(self.lon)
        self.floor = float(self.floor)
        self.in_out = int(self.in_out or "99")  # Temporary implementaton for missing value

    @classmethod
    def get_fields(cls):
        return [f.name for f in fields(cls)]


@dataclass
class Link:
    link_id: str
    start_id: str
    end_id: str
    distance: float
    rt_struct: int
    route_type: int
    direction: int
    width: int
    vtcl_slope: int
    lev_diff: int
    tfc_signal: int
    tfc_s_type: int
    brail_tile: int
    elevator: int
    roof: int

    def __post_init__(self):
        self.distance = float(self.distance)
        self.rt_struct = int(self.rt_struct or "99")
        self.route_type = int(self.route_type or "99")
        self.direction = int(self.direction or "99")
        self.width = int(self.width or "99")
        self.vtcl_slope = int(self.vtcl_slope or "99")
        self.lev_diff = int(self.lev_diff or "99")
        self.tfc_signal = int(self.tfc_signal or "99")
        self.tfc_s_type = int(self.tfc_s_type or "99")
        self.brail_tile = int(self.brail_tile or "99")
        self.elevator = int(self.elevator or "99")
        self.roof = int(self.roof or "99")

    @classmethod
    def get_fields(cls):
        return [f.name for f in fields(cls)]
