from __future__ import annotations

import datetime as dt
from typing import Union

from .integers import rand_below, rand_int

Datelike = Union[str, int, tuple[int, int, int], dt.date, dt.datetime]
Timelike = Union[
    str,
    int,
    tuple[int, int],
    tuple[int, int, int],
    tuple[int, int, int, int],
    dt.time,
    dt.datetime,
]


def _convert_date(date: Datelike) -> dt.date:
    if isinstance(date, str):
        return dt.date.fromisoformat(date)
    if isinstance(date, int):
        return dt.date(date, 1, 1)
    if isinstance(date, tuple):
        return dt.date(*date)
    if isinstance(date, dt.datetime):
        return date.date()
    return date


def _convert_time(time: Timelike) -> dt.time:
    if isinstance(time, str):
        return dt.time.fromisoformat(time)
    if isinstance(time, int):
        return dt.time(time)
    if isinstance(time, tuple):
        return dt.time(*time)
    if isinstance(time, dt.datetime):
        return time.time()
    return time


def _microseconds(time: dt.time) -> int:
    return (
        time.microsecond
        + time.second * 10**6
        + time.minute * 6 * 10**7
        + time.hour * 36 * 10**8
    )


def rand_date(start: Datelike, end: Datelike | None = None) -> dt.date:
    """
    Return a random date between start and end. If end is None, defaults to Dec 31.
    """
    start = _convert_date(start)
    if end is None:
        end = dt.date(start.year, 12, 31)
    elif isinstance(end, int):
        end = dt.date(end, 12, 31)
    else:
        end = _convert_date(end)
    return start + dt.timedelta(days=rand_below((end - start).days + 1))


def rand_time(start: Timelike | None = None, end: Timelike | None = None) -> dt.time:
    """
    Return a random time between start and end.
    If start is None, defaults to 00:00:00.
    If end is None, defaults to 23:59:59.999999.
    """
    start = dt.time.min if start is None else _convert_time(start)
    end = dt.time.max if end is None else _convert_time(end)
    out = rand_int(_microseconds(start), _microseconds(end))
    out, us = divmod(out, 1_000_000)
    out, s = divmod(out, 60)
    h, m = divmod(out, 60)
    return dt.time(h, m, s, us)
