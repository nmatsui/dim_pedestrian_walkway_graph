import math

import staticmaps
from PIL import Image, ImageChops, ImageDraw, ImageFont

from viewer.utils import CoordTransformer


class MapRenderer:
    GET_ZOOM = 15
    BG_IMAGE_ROTATE = 90.0
    SCALE_START_POS_X_MARGIN = 10
    SCALE_START_POS_Y_MARGIN = -20
    SCALE_MAIN_WIDTH = 20
    SCALE_SUB_WIDTH = 4
    TEXT_MARGIN = 4
    SCALE_TEXT = "1km"

    def __init__(self, config, size):
        self.config = config
        self.size = size
        self.provider = self._get_provider(self.config.map_config.provider)

    def render(self, nodes, links, map_path):
        rastermap = self._generate_rastermap()
        self._attach_scale(rastermap)
        img = rastermap.rotate(-MapRenderer.BG_IMAGE_ROTATE, expand=True)

        draw = ImageDraw.Draw(img)

        for node in nodes.values():
            if not node.links:
                continue

            p = (
                node.x - self.config.map_config.node_radius,
                node.y - self.config.map_config.node_radius,
                node.x + self.config.map_config.node_radius,
                node.y + self.config.map_config.node_radius,
            )
            draw.ellipse(p, fill=tuple(self.config.map_config.line_color))

        for link in links:
            draw.line(
                (link.start_node.as_tuple(), link.end_node.as_tuple()),
                fill=tuple(self.config.map_config.line_color),
                width=self.config.map_config.line_width,
            )

        img.rotate(MapRenderer.BG_IMAGE_ROTATE, expand=True).save(map_path, format="PNG")

    def _get_provider(self, provider):
        match (provider):
            case "StamenToner":
                return staticmaps.tile_provider_StamenToner
            case "OSM":
                return staticmaps.tile_provider_OSM
            case "Chiriin":
                return staticmaps.TileProvider(
                    name="chiriin",
                    url_pattern="https://cyberjapandata.gsi.go.jp/xyz/std/$z/$x/$y.png",
                    attribution="Source: Geospatial Information Authority of Japan",
                    max_zoom=18,
                )
            case _:
                return staticmaps.tile_provider_CartoNoLabels

    def _generate_rastermap(self):
        _size = (self.size[1], self.size[0])

        center = staticmaps.create_latlng(
            (self.config.map_config.map_bottom_left[0] + self.config.map_config.map_top_right[0]) / 2.0,
            (self.config.map_config.map_bottom_left[1] + self.config.map_config.map_top_right[1]) / 2.0,
        )

        area = [
            staticmaps.create_latlng(lat, lng)
            for lat, lng in (
                self.config.map_config.map_bottom_left,
                (self.config.map_config.map_bottom_left[0], self.config.map_config.map_top_right[1]),
                self.config.map_config.map_top_right,
                (self.config.map_config.map_top_right[0], self.config.map_config.map_bottom_left[1]),
                self.config.map_config.map_bottom_left,
            )
        ]

        context = staticmaps.Context()
        context.set_tile_provider(self.provider)
        context.set_zoom(MapRenderer.GET_ZOOM)
        context.set_center(center)

        image_all = context.render_pillow(*_size)

        context.add_object(
            staticmaps.Area(
                area,
                fill_color=staticmaps.BLACK,
                width=0,
                color=staticmaps.BLACK,
            )
        )

        image_filled = context.render_pillow(*_size)

        rect = ImageChops.difference(image_all.convert("RGB"), image_filled.convert("RGB")).getbbox()
        cropped = image_all.crop(rect)
        resized = cropped.resize(_size, Image.LANCZOS)

        return resized

    def _attach_scale(self, rastermap):
        transformer = CoordTransformer(self.config)
        _size = (self.size[1], self.size[0])

        draw = ImageDraw.Draw(rastermap)
        x, y = transformer.latlng2xy(*self.config.map_config.map_bottom_left)
        one_km_px = transformer.xy2imagexy(x + 1000.0, y)[0] - transformer.xy2imagexy(x, y)[0]

        draw.line(
            (
                (0 + MapRenderer.SCALE_START_POS_X_MARGIN, _size[1] + MapRenderer.SCALE_START_POS_Y_MARGIN),
                (0 + MapRenderer.SCALE_START_POS_X_MARGIN + one_km_px, _size[1] + MapRenderer.SCALE_START_POS_Y_MARGIN),
            ),
            tuple(self.config.map_config.scale_color),
            MapRenderer.SCALE_MAIN_WIDTH,
        )
        draw.line(
            (
                (
                    0 + MapRenderer.SCALE_START_POS_X_MARGIN + math.floor(MapRenderer.SCALE_SUB_WIDTH / 2),
                    _size[1] + MapRenderer.SCALE_START_POS_Y_MARGIN,
                ),
                (
                    0 + MapRenderer.SCALE_START_POS_X_MARGIN + math.floor(MapRenderer.SCALE_SUB_WIDTH / 2),
                    _size[1] + MapRenderer.SCALE_START_POS_Y_MARGIN * 2,
                ),
            ),
            tuple(self.config.map_config.scale_color),
            MapRenderer.SCALE_SUB_WIDTH,
        )
        draw.line(
            (
                (
                    0 + MapRenderer.SCALE_START_POS_X_MARGIN + one_km_px - math.ceil(MapRenderer.SCALE_SUB_WIDTH / 2) + 1,
                    _size[1] + MapRenderer.SCALE_START_POS_Y_MARGIN,
                ),
                (
                    0 + MapRenderer.SCALE_START_POS_X_MARGIN + one_km_px - math.ceil(MapRenderer.SCALE_SUB_WIDTH / 2) + 1,
                    _size[1] + MapRenderer.SCALE_START_POS_Y_MARGIN * 2,
                ),
            ),
            tuple(self.config.map_config.scale_color),
            MapRenderer.SCALE_SUB_WIDTH,
        )

        font = ImageFont.truetype(self.config.map_config.scale_font_path, self.config.map_config.scale_font_size)
        text_size = font.getsize(MapRenderer.SCALE_TEXT)
        text_point = (
            0 + MapRenderer.SCALE_START_POS_X_MARGIN + one_km_px - math.ceil(text_size[0] / 2),
            _size[1] + MapRenderer.SCALE_START_POS_Y_MARGIN * 2 - math.ceil(text_size[1]) - MapRenderer.TEXT_MARGIN,
        )
        draw.text(text_point, MapRenderer.SCALE_TEXT, font=font, fill=tuple(self.config.map_config.scale_color))
