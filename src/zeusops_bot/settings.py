"""Base settings and config"""

from pydantic import DirectoryPath, FilePath, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ReforgerConfig(BaseSettings):
    """Manages the config of the reforger subsection"""

    reference_config: FilePath
    """The sample reforger config.json server we use as base"""
    config_folder: DirectoryPath
    """The place where all the bot-created derived config live + active symlink"""
    model_config = SettingsConfigDict(env_prefix="bot_reforger_")


class DiscordConfig(BaseSettings):
    """Manages the config of the discord bot"""

    token: SecretStr
    """The actual secret to run the bot with"""
    zeusops_guild_id: str
    """The Zeusops main GuildID"""
    cmd_listen_channel_id: str
    """The Discord ChannelID to listen for commands onto"""
    cmd_log_channel: str
    """The Discord ChannelID to log result of commands onto"""
    model_config = SettingsConfigDict(env_prefix="bot_discord_")


class ZeusopsBotConfig(BaseSettings):
    """All the config we may need, in subsections"""

    reforger: ReforgerConfig
    discord: DiscordConfig
    model_config = SettingsConfigDict(env_prefix="bot_")
