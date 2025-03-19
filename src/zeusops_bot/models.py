"""Data models we may need for mission upload"""

from typing import NotRequired, TypedDict

from pydantic import TypeAdapter

modlist_typeadapter = TypeAdapter(list["ModDetail"])


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


def extract_mods(modlist: str | None) -> list[ModDetail] | None:
    """Extracts a list of ModDetail entries from a mod list exported from Reforger."""
    if modlist is None:
        return None
    modlist = f"[{modlist}]"
    return modlist_typeadapter.validate_json(modlist)
