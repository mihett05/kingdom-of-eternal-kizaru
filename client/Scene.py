from AppData import AppData


class Scene:
    _instance = None  # Singleton

    def __new__(cls):
        if Scene._instance is None:
            Scene._instance = super(Scene, cls).__new__(cls)
        return Scene._instance

    def __init__(self):
        try:
            self.__getattribute__("name")
        except AttributeError:
            self.name = None
            self.proto = None
            self.data = AppData()
            self.ui = self.data.ui()
            self.queue = []
            self.scene = None

    def change(self, name, proto):
        self.name = name
        self.proto = proto
        self.ui.clear_and_reset()
        self.scene = proto()


