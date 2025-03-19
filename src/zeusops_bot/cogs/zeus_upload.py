"""zeus_upload extension"""

import json
from typing import Annotated

import discord

# from discord.commands import option
from discord.ext import commands
from discord.utils import basic_autocomplete
from pydantic import TypeAdapter, ValidationError

from zeusops_bot.errors import (
    ConfigFileInvalidJson,
    ConfigFileNotFound,
    ConfigPatchingError,
)
from zeusops_bot.models import ModDetail, extract_mods
from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator
from zeusops_bot.settings import ZeusopsBotConfig

OptionalDiscordAttachment = Annotated[
    discord.Attachment,
    discord.Option(discord.SlashCommandOptionType.attachment, required=False),
]

modlist_typeadapter = TypeAdapter(list[ModDetail])


async def _autocomplete_missions(ctx: discord.AutocompleteContext) -> list[str]:
    return [
        mission
        for mission in ReforgerConfigGenerator.get_config().list_missions()
        if ctx.value.lower() in mission.lower()
    ]


# NOTE: this isn't needed when using the autocomplete decorator
AutocompletedMission = Annotated[
    str,
    discord.Option(
        str, "mission", autocomplete=basic_autocomplete(_autocomplete_missions)
    ),
]


class ZeusUpload(commands.Cog):
    """ZeusUpload cog for handling mission uploads"""

    def __init__(self, bot: discord.Bot, config: ZeusopsBotConfig):
        """Initialise the cog"""
        self.bot = bot
        self.config = config
        self.reforger_confgen = ReforgerConfigGenerator(
            base_config_file=config.reforger.reference_config,
            target_folder=config.reforger.config_folder,
        )

    @commands.slash_command(name="zeus-upload")
    async def zeus_upload(
        self,
        ctx: discord.ApplicationContext,
        scenario_id: str,
        filename: str,
        modlist: OptionalDiscordAttachment,
    ):
        """Upload a mission as a Zeus"""
        try:
            if modlist is None:
                extracted_mods = None
            else:
                data = await modlist.read()
                extracted_mods = extract_mods(data.decode())
            path = self.reforger_confgen.zeus_upload(
                scenario_id, filename, modlist=extracted_mods
            )
        except json.JSONDecodeError as e:
            await ctx.respond(
                "Failed to understand the attached modlist as JSON. "
                "Check the file was exported from the workshop, "
                "try confirming with an online validator like "
                "<https://jsonlint.com/>. "
                f"Parse error was: {e}"
            )
            return
        except ValidationError as e:
            await ctx.respond(
                "Failed to understand the modlist given: valid JSON, "
                "but not a list of mod objects (name/ID/optional-version). "
                "Check the file was exported from the workshop? "
                f"Validation error was: {e}"
            )
            return
        except ConfigFileNotFound:
            await ctx.respond(
                "Bot config error: the base config file could not be found"
                f" Tell the Techmins! Path was: {self.reforger_confgen.base_config}"
            )
            return
        except ConfigFileInvalidJson as e:
            await ctx.respond(
                "Bot config error: the base config file is invalid JSON "
                "Tell the Techmins! Error was: " + str(e)
            )
            return
        except ConfigPatchingError as e:
            await ctx.respond(
                "Failed to patch your requested change over base config.\n"
                f"Error was: {str(e)}"
            )
            return
        await ctx.respond(f"Mission uploaded successfully under {path=}")

    @commands.slash_command(name="zeus-set-mission")
    # NOTE: there are two ways of creating auto-completions, this decorator and
    #       the `AutocompletedMission` type hint
    # @option(
    #     "filename", description="Mission filename", autocomplete=autocomplete_missions
    # )
    async def zeus_set_mission(
        self,
        ctx: discord.ApplicationContext,
        filename: AutocompletedMission,
    ):
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
