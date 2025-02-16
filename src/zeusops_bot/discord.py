"""Manage the Discord-side horrors"""

import logging

from discord import Bot

from zeusops_bot.settings import DiscordConfig


class ZeusopsBot(Bot):
    """A Discord Client for general purposes"""

    def __init__(self, config: DiscordConfig, *args, **kwargs):
        """Initialize the Client"""
        super().__init__(*args, **kwargs)
        self.config = config

        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.gateway").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

        # TODO: load all cogs dynamically
        self.load_extension("zeusops_bot.cogs.zeus_upload")

    async def on_ready(self):
        """Handle the 'ready' event"""
        self.logger.info("Logged in as %s#%s", self.user.name, self.user.discriminator)
