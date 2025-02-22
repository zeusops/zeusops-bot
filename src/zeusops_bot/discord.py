"""Manage the Discord-side horrors"""

from discord import Bot

from zeusops_bot.cogs import ZeusUpload
from zeusops_bot.settings import ZeusopsBotConfig


class ZeusopsBot(Bot):
    """A Discord Client for general purposes"""

    def __init__(self, config: ZeusopsBotConfig, logger, *args, **kwargs):
        """Initialize the Client"""
        super().__init__(*args, **kwargs)
        self.config = config
        self.logger = logger

        cog = ZeusUpload(self, config)
        self.add_cog(cog)

    def run(self):
        """Override to the main run, to tell it where to get the token"""
        super().run(self.config.discord.token.get_secret_value())

    async def on_ready(self):
        """Handle the 'ready' event"""
        self.logger.info("Logged in as %s#%s", self.user.name, self.user.discriminator)
