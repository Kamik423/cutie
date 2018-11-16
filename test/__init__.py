import readchar

import cutie


class InputContext:

    def __init__(self, *data, raise_on_empty=True):
        cutie.readchar.readkey = yield_input(*data, raise_on_empty=raise_on_empty)

    def __enter__(self):
        pass

    def __exit__(self, *a):
        cutie.readchar.readkey = readchar.readkey


class MockException(Exception):
    pass


def yield_input(*data, raise_on_empty=False):
    data = list(data)

    def func(*a, **kw):
        try:
            return data.pop(0)
        except IndexError:
            raise MockException()

    return func
