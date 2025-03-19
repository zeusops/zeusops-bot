"""Manage the Discord-side horrors"""

from logging import Logger

from discord import Bot

from zeusops_bot.cogs import ZeusUpload
from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator
from zeusops_bot.settings import ZeusopsBotConfig


class ZeusopsBot(Bot):
    """A Discord Client for general purposes"""

    def __init__(self, config: ZeusopsBotConfig, logger: Logger, *args, **kwargs):
        """Initialize the Client"""
        super().__init__(*args, **kwargs)
        self.config = config
        self.logger = logger
        self.reforger_confgen = ReforgerConfigGenerator(
            base_config_file=config.reforger.reference_config,
            target_folder=config.reforger.config_folder,
        )

        cog = ZeusUpload(self, self.reforger_confgen)
        self.add_cog(cog)

    def run(self):
        """Override to the main run, to tell it where to get the token"""
        super().run(self.config.discord.token.get_secret_value())

    async def on_ready(self):
        """Handle the 'ready' event"""
        self.logger.info("Logged in as %s#%s", self.user.name, self.user.discriminator)
