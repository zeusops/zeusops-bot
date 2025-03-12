"""zeus_upload extension"""

import discord
from discord.ext import commands

from zeusops_bot.errors import (
    ConfigFileInvalidJson,
    ConfigFileNotFound,
    ConfigPatchingError,
)
from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator


class ZeusUpload(commands.Cog):
    """ZeusUpload cog for handling mission uploads"""

    def __init__(self, bot, config):
        """Initialise the cog"""
        self.bot = bot
        self.config = config
        self.reforger_confgen = ReforgerConfigGenerator(
            base_config_file=config.reforger.reference_config,
            target_folder=config.reforger.config_folder,
        )

    @commands.slash_command(name="zeus-upload")
    async def zeus_upload(
        self, ctx: discord.ApplicationContext, scenario_id: str, filename: str
    ):
        """Upload a mission as a Zeus"""
        try:  # TODO: How do we pass modlist != None
            path = self.reforger_confgen.zeus_upload(
                scenario_id, filename, modlist=None
            )
            await ctx.respond(f"Mission uploaded successfully under {path=}")
        except ConfigFileNotFound:
            await ctx.respond(
                "Bot config error: the base config file could not be found"
                " Tell the Techmins! Path was: "
                + str(self.reforger_confgen.base_config)
            )
        except ConfigFileInvalidJson as e:
            await ctx.respond(
                "Bot config error: the base config file is invalid JSON "
                "Tell the Techmins! Error was: " + str(e)
            )
        except ConfigPatchingError as e:
            await ctx.respond(
                "Failed to patch your requested change over base config.\n"
                f"Error was: {str(e)}"
            )

    @commands.slash_command(name="zeus-set-mission")
    async def zeus_set_mission(self, ctx: discord.ApplicationContext, filename: str):
        """Activate the given a mission file as a Zeus"""
        await ctx.respond(f"Setting mission to {filename=}")
        self.reforger_confgen.zeus_set_mission(filename)

    @commands.slash_command(name="zeus-list")
    async def zeus_list(self, ctx: discord.ApplicationContext):
        """List available missions created via `/zeus-upload`"""
        missions = self.reforger_confgen.list_missions()
        if not missions:
            await ctx.respond("No missions configured")
            return
        missions_str = "\n- ".join(missions)
        await ctx.respond(f"Missions: \n- {missions_str}")

    @commands.slash_command(name="current-mission")
    async def current_mission(self, ctx: discord.ApplicationContext):
        """List currently configured mission"""
        try:
            await ctx.respond(
                f"Current mission: `{self.reforger_confgen.current_mission()}`"
            )
        except ConfigFileNotFound as e:
            await ctx.respond(f"Could not find configured mission: {str(e)}")
