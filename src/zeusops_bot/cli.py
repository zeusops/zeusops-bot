"""Command line entrypoint for zeusops-bot"""

import argparse
import logging
import sys
from enum import IntEnum
from pathlib import Path

from zeusops_bot import reforger_config_gen as cmd
from zeusops_bot.discord import ZeusopsBot
from zeusops_bot.errors import ZeusopsBotConfigException
from zeusops_bot.logging import setup_logging
from zeusops_bot.models import ModDetail
from zeusops_bot.settings import ZeusopsBotConfig, load


class Exit(IntEnum):
    """Exit codes for the CLI"""

    SUCCESS = 0
    FAILURE = 1


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
    parser.add_argument(
        "--debug",
        help="Enable debug logging",
        action="store_true",
    )
    return parser.parse_args(args)


def cli(arguments: list[str] | None = None):
    """Run the zeusops_bot cli"""
    if arguments is None:
        arguments = sys.argv[1:]
    _args = parse_arguments(arguments)
    return main(_args.debug)


def main(debug: bool = False):
    """Run the main bot"""
    try:
        config = load(ZeusopsBotConfig)
    except ZeusopsBotConfigException as e:
        envvars = e.args[0]
        print(f"Missing {len(envvars)} envvars:", file=sys.stderr)
        for envvar in envvars:
            print(f"- {envvar.upper()}", file=sys.stderr)
        return Exit.FAILURE
    except Exception:
        print("Error while loading the bot's config from envvars", file=sys.stderr)
        raise

    setup_logging(debug)

    bot = ZeusopsBot(config, logging.getLogger("zeusops.discord"))
    bot.run()  # Token is already in config


def reforger_upload(
    base_config_file: Path,
    target_folder: Path,
    modlist: list[ModDetail] | None,
    scenario_id: str,
    filename: str,
):
    """Run the program's /zeus-upload command"""
    conf_generator = cmd.ReforgerConfigGenerator(base_config_file, target_folder)
    if modlist is not None:
        print(f"Loading {len(modlist)} mods, for {scenario_id=}...")
    else:
        print(f"Loading {scenario_id=}...")
    out_path = conf_generator.zeus_upload(scenario_id, filename, modlist)
    print(f"Saved under file {out_path.name}")
    return Exit.SUCCESS
