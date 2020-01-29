class WindowManager:
    def __init__(self):
        self.active_window_proto = None
        self.active_window = None

    def create(self, window_proto):
        self.close()
        self.active_window_proto = window_proto
        self.active_window = window_proto()

    def close(self):
        if self.active_window is not None:
            self.active_window.kill()
            self.active_window = None
            self.active_window_proto = None

