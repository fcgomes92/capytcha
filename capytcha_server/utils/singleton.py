class Singleton:
    class __Singleton:
        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not Singleton.instance:
            Singleton.instance = Singleton.__Singleton()
        return Singleton.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)
