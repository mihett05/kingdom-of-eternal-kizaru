from client.Map import Map


class MapManager:
    def __init__(self):
        self.map = None

    def set_map(self, map_path):
        if self.map is not None:
            self.clear_map()
        self.map = Map(map_path)

    def draw(self):
        self.map.draw()

    def clear_map(self):
        self.map.clear()
