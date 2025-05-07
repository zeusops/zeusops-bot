"""Data models we may need for mission upload"""

from typing import NotRequired, TypedDict

from pydantic import TypeAdapter


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


class TypedTypeAdapter[T]:
    """A wrapper around Pydantic's TypeAdapter to make mypy happy

    This class defines basically the same types as the actual TypeAdapter, but
    somehow mypy doesn't complain when using this one.
    """

    def __init__(self, type: type[T], **kwargs) -> None:
        """Typed init"""
        self.adapter = TypeAdapter(type, *kwargs)

    def validate_json(self, data: str | bytes | bytearray, /, **kwargs) -> T:
        """Typed method"""
        return self.adapter.validate_json(data, *kwargs)


modlist_typeadapter = TypedTypeAdapter(list[ModDetail])
configfile_typeadapter = TypedTypeAdapter(ConfigFile)
