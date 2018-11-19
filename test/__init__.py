import readchar

import cutie


def print_call(msg="", state="selectable", delimiter_selectable="()", delimiter_active="{}"):
    """
    Convenience function to generate expected calls to `cutie.print`
    """
    delimiter_selectable = tuple(delimiter_selectable)
    delimiter_active = tuple(delimiter_active)
    states = {
                "selectable": 'K\x1b[1m%s %s\x1b[0m ' % delimiter_selectable,
                "selected": 'K\x1b[1m(\x1b[32mx\x1b[0;1m)\x1b[0m ',
                "caption": 'K',
                "active": 'K\x1b[32;1m%s %s\x1b[0m ' % delimiter_active,
                "active-selected": 'K\x1b[32;1m%sx%s\x1b[0m ' % delimiter_active,
                "confirm": '1m%s%s confirm %s%s\x1b[0m \x1b[K' \
                    % (
                        delimiter_selectable[0], delimiter_selectable[0],
                        delimiter_selectable[1], delimiter_selectable[1]
                    ),
                "confirm-active": '1;32m{{ confirm }}\x1b[0m \x1b[K',
    }
    base_call = '\x1b[{state}{message}'
    return ((base_call.format(state=states[state], message=msg),),)


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
