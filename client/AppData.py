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
            self.__getattribute__("state")
        except AttributeError:
            self.state = state

    def get_state(self):
        return self.state

    def set(self, key, value):
        self.state[key] = value

    def get(self, key):
        return self.state[key]

    def __getitem__(self, item):
        return self.state[item]

    def __setitem__(self, key, value):
        self.state[key] = value

