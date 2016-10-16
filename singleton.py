# encoding: utf-8


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        cls.dispatch = cls.__dispatch
        return cls._instances[cls]

    @classmethod
    def __dispatch(cls):
        cls._instances = {}  # pragma: no cover
