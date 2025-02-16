"""Data models we may need for mission upload"""

from typing import NotRequired, TypedDict


class ModDetail(TypedDict):
    """A single mod's details

    Ref: https://community.bistudio.com/wiki/Arma_Reforger:Server_Config#mods
    """

    modId: str
    name: str
    version: NotRequired[str]
    required: NotRequired[bool]


class ConfigFileGameSection(TypedDict):
    """The 'game' section of the config file"""

    scenarioId: str
    mods: list[ModDetail]


class ConfigFile(TypedDict):
    """The reforger config file"""

    game: ConfigFileGameSection
