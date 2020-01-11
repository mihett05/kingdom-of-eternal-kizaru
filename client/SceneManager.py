from client.AppData import AppData


class SceneManager:
    _instance = None  # Singleton

    def __new__(cls):
        if SceneManager._instance is None:
            SceneManager._instance = super(SceneManager, cls).__new__(cls)
        return SceneManager._instance

    def __init__(self):
        try:
            self.__getattribute__("ui")
        except AttributeError:
            self.name = None
            self.proto = None
            self.data = AppData()
            self.ui = self.data["ui"]
            self.queue = []
            self.scene = None
            self.last = None

    def change(self, name, proto):
        self.name = name
        self.last = self.proto
        self.proto = proto
        self.ui.clear_and_reset()
        if self.scene is not None:
            self.scene.clear()
        self.scene = proto()


