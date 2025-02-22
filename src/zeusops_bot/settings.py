"""Base settings and config"""

from pydantic import DirectoryPath, FilePath, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from zeusops_bot.errors import ZeusopsBotConfigException


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
    # zeusops_guild_id: str
    # """The Zeusops main GuildID"""
    # cmd_listen_channel_id: int
    """The Discord ChannelID to listen for commands onto"""
    # cmd_log_channel: str
    # """The Discord ChannelID to log result of commands onto"""
    model_config = SettingsConfigDict(env_prefix="bot_discord_")


class ZeusopsBotConfig(BaseSettings):
    """All the config we may need, in subsections"""

    reforger: ReforgerConfig
    discord: DiscordConfig
    model_config = SettingsConfigDict(env_prefix="bot_")


def load(class_tgt: type[BaseSettings]) -> BaseSettings:
    """Load a pydantic settings class

    Args:
      class_tgt: The Pydantic BaseSettings-derived class to instantiate

    Returns:
      An instance of class_tgt, once all sub-members were loaded (non-recursive).

    Raises:
      ZeusopsBotConfigException: If any of the member objects of class_tgt fail to load
        because of missing fields, this will be raised, with parameters being the array
        of strings that these missing fields represent, as envvars missing.
      pydantic.ValidationError: If any of the class_tgt members failed to instantiate
        with errors other than missing fields, the pydantic exception will be raised
        immediately, aborting from loading

    """
    missing_envvars = []
    subclasses_dict = class_tgt.model_fields
    subclasses_instances = {}
    for subclass_fieldname, subclass_annotation in subclasses_dict.items():
        subclass = subclass_annotation.annotation
        prefix = subclass.model_config["env_prefix"]
        try:
            subclass_instance = subclass()
            subclasses_instances[subclass_fieldname] = subclass_instance
        except ValidationError as e:
            errors = e.errors()
            if not all([err["type"] == "missing" for err in errors]):
                raise  # Not just missing envvar errors = raise it as-is, aborting
            envvars = [(prefix + err["loc"][0]).upper() for err in errors]
            missing_envvars += envvars
            continue
    if missing_envvars:
        raise ZeusopsBotConfigException(missing_envvars)
    return class_tgt(**subclasses_instances)
