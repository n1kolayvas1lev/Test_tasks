from __future__ import annotations


def is_even(value: int | float) -> bool:
    """
    Value parity check.
    :param value: int | float
    :return: bool
    """
    result = False
    if (value % 10) % 2 == 0:
        result = True
    return result
