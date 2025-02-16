"""Manage the Discord-side horrors"""

from discord import Bot
from discord.ext import commands

from zeusops_bot.settings import DiscordConfig


class ZeusopsBot(commands.Cog):
    """A Discord Client for general purposes"""

    def __init__(self, bot: Bot, config: DiscordConfig, *args, **kwargs):
        """Initialize the Client"""
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.config = config

    @commands.command(name="zeus-upload")
    async def zeus_upload(self, ctx, scenario_id: str):
        """Upload a mission as a Zeus"""
        await ctx.respond(f"Uploading {scenario_id=}")

    @commands.command(name="zeus-set-mission")
    async def zeus_set_mission(self, ctx, filename: str):
        """Activate the given a mission file as a Zeus"""
        await ctx.respond(f"Setting mission to {filename=}")


def setup(config: DiscordConfig):
    """Prepare a bot with the given config"""
    bot = Bot()
    bot.add_cog(ZeusopsBot(bot, config))
    return bot
