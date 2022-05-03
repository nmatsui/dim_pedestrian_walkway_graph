from viewer import models


def connect_all(link):
    link.start_node.links.append(link)
    link.end_node.links.append(link)
    return True


def connect_class1(link):
    if (
        link.rt_struct not in (models.RouteStructure.UNOFFICIAL_CROSSING, models.RouteStructure.PEDESTRIAN_BRIDGE)
        and link.route_type in (models.RouteType.GENERAL, models.RouteType.SLOPE)
        and link.width == models.Width.MORE_THAN_EAUAL_3m
        and link.vtcl_slope == models.Gradient.LESS_THAN_EQUAL_5pct
        and link.lev_diff == models.Step.LESS_THAN_EQUAL_2cm
    ):
        link.start_node.links.append(link)
        link.end_node.links.append(link)
        return True
    return False


def connect_class2(link):
    if (
        link.rt_struct not in (models.RouteStructure.UNOFFICIAL_CROSSING, models.RouteStructure.PEDESTRIAN_BRIDGE)
        and link.route_type in (models.RouteType.GENERAL, models.RouteType.SLOPE)
        and link.width == models.Width.MORE_THAN_EAUAL_2m_LESS_THAN_3m
        and link.vtcl_slope == models.Gradient.LESS_THAN_EQUAL_5pct
        and link.lev_diff == models.Step.LESS_THAN_EQUAL_2cm
    ):
        link.start_node.links.append(link)
        link.end_node.links.append(link)
        return True
    return False


def connect_class3(link):
    if (
        link.rt_struct not in (models.RouteStructure.UNOFFICIAL_CROSSING, models.RouteStructure.PEDESTRIAN_BRIDGE)
        and link.route_type in (models.RouteType.GENERAL, models.RouteType.SLOPE)
        and (
            (
                link.width in (models.Width.MORE_THAN_EAUAL_2m_LESS_THAN_3m, models.Width.MORE_THAN_EAUAL_3m)
                and link.vtcl_slope != models.Gradient.LESS_THAN_EQUAL_5pct
                and link.lev_diff != models.Step.LESS_THAN_EQUAL_2cm
            )
            or (link.width == models.Width.MORE_THAN_EAUAL_1m_LESS_THAN_2m)
        )
    ):
        link.start_node.links.append(link)
        link.end_node.links.append(link)
        return True
    return False
