from __future__ import annotations

import argparse
from contextlib import suppress
from pathlib import Path

from ixia import choice, rand_int, rand_line, uniform


def _parse_args() -> tuple[argparse.Namespace, str]:
    parser = argparse.ArgumentParser(
        prog="ixia",
        description="Connecting secrets' security with random's versatility",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    mutex_group = parser.add_mutually_exclusive_group()
    mutex_group.add_argument(
        "-c", "--choice", nargs="+", metavar="ITEM", help="print a random choice"
    )
    mutex_group.add_argument(
        "-i",
        "--int",
        "--integer",
        type=int,
        metavar="N",
        help="print a random integer between 1 and N inclusive",
    )
    mutex_group.add_argument(
        "-l", "--line", type=argparse.FileType(), help="print a random line from a file"
    )
    mutex_group.add_argument(
        "-f",
        "--float",
        type=float,
        metavar="N",
        help="print a random floating-point number between 0 and N inclusive",
    )
    parser.add_argument(
        "input",
        nargs="*",
        help=(
            "if no options given, output depends on the input:"
            "\n  string or multiple: same as --choice"
            "\n  valid path:         same as --line"
            "\n  integer:            same as --int/--integer"
            "\n  float:              same as --float"
        ),
    )
    return parser.parse_args(), parser.format_help()


def _resolve_value(value: str) -> str | int | float:
    # Resolution order: path -> int -> float -> string
    if Path(value).resolve().exists():
        return rand_line(value)
    with suppress(ValueError):
        return rand_int(1, int(value))
    with suppress(ValueError):
        return uniform(0.0, float(value))
    # Splitting, likely a space-separated string
    return choice(value.split())


def main() -> None:
    args, help_text = _parse_args()

    if args.choice:
        print(choice(args.choice))
    elif args.int:
        print(rand_int(1, args.int))
    elif args.line:
        print(rand_line(args.line))
    elif args.float:
        print(uniform(0.0, args.float))
    elif args.input:
        print(
            choice(args.input)
            if len(args.input) >= 2
            else _resolve_value(args.input[0])
        )
    else:
        print(help_text)


if __name__ == "__main__":
    main()
