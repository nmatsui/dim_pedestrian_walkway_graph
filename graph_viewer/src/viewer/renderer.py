from PIL import Image, ImageDraw


class MapRenderer:
    BG_COLOR = (255, 255, 255)
    GRAPH_COLOR = (255, 51, 51)
    NODE_R = 2

    def __init__(self, size):
        self.size = size

    def render(self, nodes, links, map_path):
        img = Image.new("RGB", self.size, color=MapRenderer.BG_COLOR)
        draw = ImageDraw.Draw(img)

        for node in nodes.values():
            if not node.links:
                continue

            p = (
                node.x - MapRenderer.NODE_R,
                node.y - MapRenderer.NODE_R,
                node.x + MapRenderer.NODE_R,
                node.y + MapRenderer.NODE_R,
            )
            draw.ellipse(p, fill=MapRenderer.GRAPH_COLOR)

        for link in links:
            draw.line((link.start_node.as_tuple(), link.end_node.as_tuple()), fill=MapRenderer.GRAPH_COLOR)

        img.rotate(90, expand=True).save(map_path, format="PNG")
