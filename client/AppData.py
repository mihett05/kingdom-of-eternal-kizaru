class AppData:
    _instance = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if AppData._instance is None:
            AppData._instance = super(AppData, cls).__new__(cls, *args, **kwargs)
        return AppData._instance

    def __init__(self, state: dict = None):
        if state is None:
            state = dict()
        try:
            self.__getattribute__("_state")
        except AttributeError:
            self._state = state

    def get_state(self):
        return self._state

    def set(self, key, value):
        self._state[key] = value
        self.__setattr__(key, lambda: self.get(key))

    def get(self, key):
        return self._state[key]

