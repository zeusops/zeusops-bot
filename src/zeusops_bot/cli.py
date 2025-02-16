"""Command line entrypoint for zeusops-bot"""

import argparse
import sys
from pathlib import Path

from zeusops_bot import command
from zeusops_bot.models import ModDetail


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
    parser.add_argument("base_config_path", help="The path to base config file")
    parser.add_argument("target_folder", help="The path where to store loaded configs")
    parser.add_argument("scenario_id", help="Scenario ID to load")
    parser.add_argument("config_file_name", help="Name under which to save new config")
    parser.add_argument("--mods", help="JSON string of modlist to load, or no change")
    return parser.parse_args(args)


def cli(arguments: list[str] | None = None):
    """Run the zeusops_bot cli"""
    if arguments is None:
        arguments = sys.argv[1:]
    args = parse_arguments(arguments)
    main(
        Path(args.base_config),
        Path(args.target_folder),
        args.mods,
        args.scenario_id,
        args.config_file_name,
    )


def main(
    base_config_file: Path,
    target_folder: Path,
    modlist: list[ModDetail] | None,
    scenario_id: str,
    filename: str,
):
    """Run the program's main command"""
    conf_generator = command.ReforgerConfigGenerator(base_config_file, target_folder)
    if modlist is not None:
        print(f"Loading {len(modlist)} mods, for {scenario_id=}...")
    else:
        print(f"Loading {scenario_id=}...")
    out_path = conf_generator.zeus_upload(scenario_id, filename, modlist)
    print(f"Saved under file {out_path.name}")
    return 0
