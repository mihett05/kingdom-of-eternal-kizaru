from client.AppData import AppData
from client.Scenes import *


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
            self.dumps = {
                "MainMenu": MainMenuScene,
                "CharsScene": CharsScene,
                "Settings": SettingsScene,
                "CharMaker": CharMakerScene,
                "CharDelete": CharDeleteScene,
                "Game": GameScene,
                "Register": RegisterScene,
                "login": LoginScene,
                "Battle": BattleScene
            }
            self.ui = self.data["ui"]
            self.queue = []
            self.scene = None
            self.last = None
            self.game_scene = None

    def change(self, name, proto, make_dump=False):
        if make_dump:
            self.dumps[name] = proto
        self.name = name
        self.last = self.proto
        self.proto = proto
        self.ui.clear_and_reset()
        if self.scene is not None and not isinstance(self.scene, GameScene):
            self.scene.clear()
        if proto is GameScene and self.game_scene is not None:
            self.scene = self.game_scene
            self.scene.resume()
        else:
            self.scene = proto()
            if isinstance(self.scene, GameScene):
                self.game_scene = self.scene
        self.scene.name = name
