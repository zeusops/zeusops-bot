"""Logging-related utilities"""

import logging


def setup_logging(debug):
    """Set up basic logger"""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

        # By default the Discord library is very verbose, so we're limiting it
        # a bit
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.gateway").setLevel(logging.WARNING)
