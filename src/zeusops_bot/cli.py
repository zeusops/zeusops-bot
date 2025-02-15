"""Command line entrypoint for zeusops-bot"""

import argparse
import sys


def parse_arguments(args: list[str]) -> argparse.Namespace:
    """Parse generic arguments, given as parameters

    This function can be used programatically to emulate CLI calls, either
    during tests or via other interfaces like API calls.


    Arguments:
      args: The arguments to parse, usually from `sys.argv` array.

    """
    parser = argparse.ArgumentParser(
        "zeusops-bot",
        description="Multipurpose discord bot for the Zeusops community",
    )
    parser.add_argument("foo", help="Some parameter")
    return parser.parse_args(args)


def cli(arguments: list[str] | None = None):
    """Run the zeusops_bot cli"""
    if arguments is None:
        arguments = sys.argv[1:]
    args = parse_arguments(arguments)
    main(args.foo)


def main(foo):
    """Run the program's main command"""
    print(f"Foo is: {foo}")
