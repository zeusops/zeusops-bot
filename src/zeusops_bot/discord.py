"""Manage the Discord-side horrors"""

from discord import Bot, Message

# from discord.ext import commands
from zeusops_bot.settings import DiscordConfig


class ZeusopsBot(Bot):
    """A Discord Client for general purposes"""

    def __init__(self, config: DiscordConfig, *args, **kwargs):
        """Initialize the Client"""
        super().__init__(*args, **kwargs)
        self.config = config

    # FIXME: Convert from prefix commands into slash commands
    # @commands.command(name="zeus-upload")
    # async def zeus_upload(self, ctx, scenario_id: str):
    #     """Upload a mission as a Zeus"""
    #     await ctx.respond(f"Uploading {scenario_id=}")

    # @commands.command(name="zeus-set-mission")
    # async def zeus_set_mission(self, ctx, filename: str):
    #     """Activate the given a mission file as a Zeus"""
    #     await ctx.respond(f"Setting mission to {filename=}")

    async def on_ready(self):
        """Handle the 'ready' event"""
        print("ready!")
        print("Logged in as %s#%s" % (self.user.name, self.user.discriminator))

    # TODO: deprecate
    async def on_message(self, message: Message):
        """Handle incoming messages"""
        print(type(message.channel.id), type(self.config.cmd_listen_channel_id))
        if message.channel.id != self.config.cmd_listen_channel_id:
            return
        print(f'received a message! {message.author} "{message.content}"')
