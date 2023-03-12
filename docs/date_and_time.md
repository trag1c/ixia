# Date & Time

## `ixia.rand_date`

```py
Datelike = str | int | tuple[int, int, int] | datetime.date | datetime.datetime

def rand_date(start: Datelike, end: Datelike | None = None) -> datetime.date
```
Returns a random date between `start` and `end` (both inclusive).

The inputs can be of the following types:
- ISO format string (e.g. "2023-03-12")
- year integer (`rand_date(2020, 2022)` ⇔ `rand_date("2020-01-01", "2022-12-31")`)
- (year, month, day) tuple
- `datetime.date` object
- `datetime.datetime` object

If `end` is not specified, it's gonna be set to the end of the start date's year,  
(e.g. `rand_date("2023-09-01")` → `rand_date("2023-09-01", "2023-12-31")`).


## `ixia.rand_time`

```py
Timelike = (
    str
    | int
    | tuple[int, int]
    | tuple[int, int, int]
    | tuple[int, int, int, int]
    | datetime.time
    | datetime.datetime
)

def rand_time(
    start: Timelike | None = None, end: Timelike | None = None
) -> datetime.time
```

Returns a random date between `start` and `end` (both inclusive).

The inputs can be of the following types:
- ISO format string (e.g. `"12:34:56.789012"`)
- hour integer
- 2–4 integer (hour, minute, second, microsecond) tuple (only the first two are required)
- `datetime.time` object
- `datetime.datetime` object
