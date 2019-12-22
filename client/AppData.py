class AppData:
    _instance = None  # Singleton

    def __new__(cls, *args, **kwargs):
        if AppData._instance is None:
            AppData._instance = super(AppData, cls).__new__(cls, *args, **kwargs)
        return AppData._instance

    def __init__(self, state: dict):
        self._state = state

    def get_state(self):
        return self._state

    def set(self, key, value, is_main=False):
        """
        is_main
            if false
                can get by AppData.state.<key>
            elif true
                can get by AppData.<key>
        """
        self._state[key] = value
        if key not in self._state:
            self.__setattr__(("" if is_main else "state.") + key, lambda: self._state[key])

    def get(self, key):
        return self._state[key]

