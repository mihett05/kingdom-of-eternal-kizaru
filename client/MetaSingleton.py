class MetaSingleton(type):
    _instances = dict()

    def __call__(cls, *args):
        if cls not in MetaSingleton._instances:
            MetaSingleton._instances[cls] = None
        if MetaSingleton._instances[cls] is None:
            obj = cls.__new__(cls)
            obj.__init__(*args)
            MetaSingleton._instances[cls] = obj
        return MetaSingleton._instances[cls]

    @staticmethod
    def remove(cls):
        MetaSingleton._instances[cls] = None
