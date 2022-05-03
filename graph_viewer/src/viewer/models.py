from dataclasses import dataclass, field
from enum import Enum
from typing import List


class InOut(Enum):
    OUTSIDE = 1
    BORDER = 2
    INSIDE = 3
    UNKNOWN = 99


class RouteStructure(Enum):
    SEPARATED_SIDEWALK = 1
    UNSEPARATED_ROAD = 2
    CROSSWALK = 3
    UNOFFICIAL_CROSSING = 4
    UNDERGROUND_PASSAGE = 5
    PEDESTRIAN_BRIDGE = 6
    IN_FACILITY_PASSAGE = 7
    OTHER = 8
    UNKNOWN = 99


class RouteType(Enum):
    GENERAL = 1
    MOVING_WALKWAY = 2
    RAILROAD_CROSSING = 3
    ELEVATOR = 4
    ESCALATOR = 5
    STAIRS = 6
    SLOPE = 7
    UNKNOWN = 99


class Direction(Enum):
    BOTH = 1
    FORWARD = 2
    BACKWARD = 3
    UNKNOWN = 99


class Width(Enum):
    LESS_THAN_1m = 1
    MORE_THAN_EAUAL_1m_LESS_THAN_2m = 2
    MORE_THAN_EAUAL_2m_LESS_THAN_3m = 3
    MORE_THAN_EAUAL_3m = 4
    UNKNOWN = 99


class Gradient(Enum):
    LESS_THAN_EQUAL_5pct = 1
    UPHILL_MORE_THAN_5pct = 2
    DOWNHILL_MORe_THAN_5pct = 3
    UNKNOWN = 99


class Step(Enum):
    LESS_THAN_EQUAL_2cm = 1
    MORE_THAN_2cm = 2
    UNKNOWN = 99


class PedestriansSignals(Enum):
    WITHOUT = 1
    WITH_VEHICLE_SEPARATED = 2
    WITH_CONTROLLABLE = 3
    OTHER = 4
    UNKNOWN = 99


class PedestriansSignalsType(Enum):
    WITHOUT_SOUND = 1
    WITH_SOUND_WITHOUT_BUTTON = 2
    WITH_SOUND_WITH_BUTTON = 3
    UNKNOWN = 99


class TactileTile(Enum):
    WITHOUT_TILE = 1
    WITH_TILE = 2
    UNKNOWN = 99


class ElevatorType(Enum):
    WITHOUT_ELEVATOR = 1
    WITH_ELEVATOR_NOT_ACCESSIBLE = 2
    WITH_ELEVATOR_ACCESSIBLE_WHEELCHAIR = 3
    WITH_ELEVATOR_ACCESSIBLE_VISUALLY_IMPAIRED = 4
    WITH_ELEVATOR_ACCESSIBLE_WHEELCHAIR_VISUALLY_IMPAIRED = 5
    UNKNOWN = 99


class Roof(Enum):
    NONE = 1
    YES = 2
    UNKNOWN = 99


@dataclass
class Node:
    node_id: str
    lat: float
    lon: float
    floor: float
    in_out: InOut
    x: int = 0
    y: int = 0
    c_x: float = 0.0
    c_y: float = 0.0
    links: List["Link"] = field(default_factory=list, repr=False)

    def transform(self, transformer):
        if self.lat != 0.0 and self.lon != 0.0:
            self.c_x, self.c_y = transformer.latlng2xy(self.lat, self.lon)
            self.x, self.y = transformer.xy2imagexy(self.c_x, self.c_y)

    def as_tuple(self):
        return (self.x, self.y)


@dataclass
class Link:
    link_id: str
    start_node: Node
    end_node: Node
    distance: float
    rt_struct: RouteStructure
    route_type: RouteType
    direction: Direction
    width: Width
    vtcl_slope: Gradient
    lev_diff: Step
    tfc_signal: PedestriansSignals
    tfc_s_type: PedestriansSignalsType
    brail_tile: TactileTile
    elevator: ElevatorType
    roof: Roof
