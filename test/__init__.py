import readchar

import cutie


def PrintCall(states):

    def func(msg=None, state="selectable"):
        if msg:
            return ((states[state] + msg,),)
        else:
            return ((states[state],),)

    return func


def yield_input(*data, raise_on_empty=False):
    """
    Closure that returns predefined data.

    If the data is exhausted raise a MockException or reraise the IndexError
    """
    data = list(data)

    def func(*a, **kw):
        try:
            return data.pop(0)
        except IndexError as e:
            if raise_on_empty:
                raise MockException()
            else:
                raise e

    return func


class InputContext:
    """
    Context manager to simulate keyboard input returned by `readchar.readkey`,
    by replacing it in `cutie` with `yield_input`

    When the supplied keystrokes are exhausted a `MockException` will be raised.
    This can be used to terminate the execution at any desired point, rather than
    relying on internal control mechanisms.

    Usage:
        with InputContext(" ", "\r"):
            cutie.select(["foo", "bar"])
    This will issue a space and enter keypress, selecting the first item and
    confirming.
    """

    def __init__(self, *data, raise_on_empty=True):
        cutie.readchar.readkey = yield_input(*data, raise_on_empty=raise_on_empty)

    def __enter__(self):
        pass

    def __exit__(self, *a):
        cutie.readchar.readkey = readchar.readkey


class MockException(Exception):
    pass
