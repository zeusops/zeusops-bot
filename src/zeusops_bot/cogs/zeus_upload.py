"""zeus_upload extension"""

import discord
from discord.ext import commands


class ZeusUpload(commands.Cog):
    """ZeusUpload cog for handling mission uploads"""

    def __init__(self, bot, config):
        """Initialise the cog"""
        self.bot = bot
        self.config = config

    @commands.slash_command(name="zeus-upload")
    async def zeus_upload(self, ctx: discord.ApplicationContext, scenario_id: str):
        """Upload a mission as a Zeus"""
        await ctx.respond(f"Uploading {scenario_id=}")

    @commands.slash_command(name="zeus-set-mission")
    async def zeus_set_mission(self, ctx: discord.ApplicationContext, filename: str):
        """Activate the given a mission file as a Zeus"""
        await ctx.respond(f"Setting mission to {filename=}")
