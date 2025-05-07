"""zeus_upload extension"""

import typing

import discord
from discord.ext import commands
from pydantic import TypeAdapter, ValidationError

if typing.TYPE_CHECKING:
    from zeusops_bot.discord import ZeusopsBot
from zeusops_bot.errors import (
    ConfigFileInvalidJson,
    ConfigFileNotFound,
    ConfigPatchingError,
)
from zeusops_bot.models import ModDetail
from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator, extract_mods

modlist_typeadapter = TypeAdapter(list[ModDetail])


def _autocomplete_missions(ctx: discord.AutocompleteContext) -> list[str]:
    """List known missions

    Used to populate the autocomplete list in /zeus-set-mission.

    TODO: Return list[discord.OptionChoice] instead?
    """
    return [
        mission
        for mission in ctx.bot.reforger_confgen.list_missions()
        if ctx.value.lower() in mission.lower()
    ]


class ZeusUpload(commands.Cog):
    """ZeusUpload cog for handling mission uploads"""

    def __init__(self, bot: "ZeusopsBot", reforger_confgen: ReforgerConfigGenerator):
        """Initialise the cog"""
        self.bot = bot
        self.reforger_confgen = reforger_confgen

    @commands.slash_command(name="zeus-upload")
    @discord.option(
        "modlist",
        description="Modlist JSON exported from Reforger",
        input_type=discord.SlashCommandOptionType.attachment,
        required=False,
    )
    @discord.option(
        "activate",
        description="Immediately use this uploaded mission as the active mission",
        required=False,
    )
    @discord.option(
        "keep_versions",
        description=(
            "Prevent version numbers from being removed from the uploaded modlist"
        ),
        required=False,
    )
    async def zeus_upload(
        self,
        ctx: discord.ApplicationContext,
        scenario_id: str,
        filename: str,
        modlist: discord.Attachment | None = None,
        activate: bool = False,
        keep_versions: bool = True,
    ):
        """Upload a mission as a Zeus"""
        extracted_mods = None
        try:
            if modlist is not None:
                data = await modlist.read()
                extracted_mods = extract_mods(
                    data.decode(), keep_versions=keep_versions
                )
        except ConfigFileInvalidJson as e:
            await ctx.respond(
                "Failed to understand the attached modlist as JSON. "
                "Check the file was exported from the workshop, "
                "try confirming with an online validator like "
                "<https://jsonlint.com/>.\n\n"
                f"Parse error was:\n```\n{e}\n```"
            )
            return
        except ValidationError as e:
            await ctx.respond(
                "Failed to understand the modlist given: valid JSON, "
                "but not a list of mod objects (name/ID/optional-version). "
                "Check the file was exported from the workshop.\n\n"
                f"Error was:\n```\n{e}\n```"
            )
            return
        try:
            path = self.reforger_confgen.zeus_upload(
                scenario_id, filename, modlist=extracted_mods, activate=activate
            )
        except ConfigFileNotFound:
            await ctx.respond(
                "Bot config error: the base config file could not be found"
                f" Tell the Techmins! Path was: {self.reforger_confgen.base_config}"
            )
            return
        except ConfigFileInvalidJson as e:
            await ctx.respond(
                "Bot config error: the base config file is invalid JSON "
                "Tell the Techmins!\n\n"
                f"Error was:\n```\n{e}\n```"
            )
            return
        except ConfigPatchingError as e:
            await ctx.respond(
                "Failed to patch your requested change over base config.\n\n"
                f"Error was:\n```\n{e}\n```"
            )
            return
        await ctx.respond(f"Mission uploaded successfully under {path=}")

    @commands.slash_command(name="zeus-set-mission")
    @discord.option(
        "filename",
        description="Mission filename",
        autocomplete=_autocomplete_missions,
    )
    async def zeus_set_mission(
        self,
        ctx: discord.ApplicationContext,
        filename: str,
    ):
        """Activate the given a mission file as a Zeus"""
        try:
            self.reforger_confgen.zeus_set_mission(filename)
            await ctx.respond(f"Setting mission to {filename=}")
        except ConfigFileNotFound:
            await ctx.respond(f"Error: could not find mission '{filename}'")

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
            await ctx.respond(f"Could not find configured mission: {e}")

    @commands.Cog.listener()
    async def on_application_command_error(
        self, ctx: discord.ApplicationContext, error: discord.DiscordException
    ):
        """Handles application command errors that are not caught elsewhere"""
        await ctx.respond(f"Unhandled exception: \n\nError was: {error}")
