import datetime as dt

from ixia.date_time import (
    _convert_date,
    _convert_time,
    _microseconds,
    rand_date,
    rand_time,
)


def test_convert_date() -> None:
    # with input as str
    assert dt.date(2022, 1, 1) == _convert_date("2022-01-01")

    # with input as int
    assert dt.date(2022, 1, 1) == _convert_date(2022)

    # with input as tuple
    assert dt.date(2022, 1, 1) == _convert_date((2022, 1, 1))

    # with input as datetime
    assert dt.date(2022, 1, 1) == _convert_date(dt.datetime(2022, 1, 1, 12, 00, 00))


def test_convert_time() -> None:
    # with input as str
    assert dt.time(12) == _convert_time("12:00:00")

    # with input as int
    assert dt.time(12) == _convert_time(12)

    # with input as tuple
    assert dt.time(12) == _convert_time((12, 0))
    assert dt.time(12) == _convert_time((12, 0, 0))
    assert dt.time(12) == _convert_time((12, 0, 0, 0))

    # with input as datetime
    assert dt.time(12) == _convert_time(dt.datetime(2022, 1, 1, 12, 00, 00))


def test_microseconds() -> None:
    time = dt.time(hour=6, minute=45, second=0)
    microseconds = (
        (time.hour * 3600) + (time.minute * 60) + time.second
    ) * 1000000 + time.microsecond
    assert microseconds == _microseconds(time)


def test_rand_date() -> None:
    start = dt.date(2022, 1, 1)
    end = dt.date(2022, 12, 31)

    # with both start and end
    assert start <= rand_date(start, end) <= end
    assert start <= rand_date(2022, 2022) <= end

    # without end
    assert start <= rand_date(start) <= end


def test_rand_time() -> None:
    start = dt.time(6, 45, 00)
    end = dt.time(20, 45, 00)

    # with both start and end as input
    assert start <= rand_time(start, end) <= end

    # with only start as input
    assert start <= rand_time(start) <= dt.time.max

    # with only end as input
    assert dt.time.min <= rand_time(end=end) <= end

    # with none as input
    assert dt.time.min <= rand_time() <= dt.time.max
