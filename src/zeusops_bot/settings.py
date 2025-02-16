"""Base settings and config"""

from pydantic import DirectoryPath, FilePath, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ZeusopsBotConfig(BaseSettings):
    """All the config we may need"""

    reference_config_file: FilePath
    """The sample reforger config.json server we use as base"""
    config_folder: DirectoryPath
    """The place where all the bot-created derived config live + active symlink"""
    discord_token: SecretStr
    """The actual secret to run the bot with"""

    model_config = SettingsConfigDict(env_prefix="bot_")
