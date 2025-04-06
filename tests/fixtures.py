"""Reusable test fixtures, that we may need between multiple tests"""

import json
from pathlib import Path

import pytest

from zeusops_bot.models import ConfigFile, ModDetail

BASE_CONFIG: ConfigFile = {
    "game": {
        "scenarioId": "old-value",
        "mods": [
            {"modId": "5EB744C5F42E0800", "name": "ACE Chopping", "version": "1.2.0"}
        ],
    }
}

MODLIST_DICT: list[ModDetail] = [
    {"modId": "595F2BF2F44836FB", "name": "RHS - Status Quo", "version": "0.10.4075"},
    {"modId": "5EB744C5F42E0800", "name": "ACE Chopping", "version": "1.2.0"},
    {"modId": "60EAEA0389DB3CC2", "name": "ACE Trenches", "version": "1.2.0"},
]

MODLIST_DICT_VERSIONLESS: list[ModDetail] = [
    {"modId": "595F2BF2F44836FB", "name": "RHS - Status Quo"},
    {"modId": "5EB744C5F42E0800", "name": "ACE Chopping"},
    {"modId": "60EAEA0389DB3CC2", "name": "ACE Trenches"},
]

# NOTE: These two formats are not 100% equivalent: Reforger exports the mods in
# a JSON list, but doesn't actually include the outer [] in the exported
# string, because the data is meant to be pasted directly inside the
# `"mods": [ ]` entry of the config file.
MODLIST_JSON: str = """
    {
        "modId": "595F2BF2F44836FB",
        "name": "RHS - Status Quo",
        "version": "0.10.4075"
    },
    {
        "modId": "5EB744C5F42E0800",
        "name": "ACE Chopping",
        "version": "1.2.0"
    },
    {
        "modId": "60EAEA0389DB3CC2",
        "name": "ACE Trenches",
        "version": "1.2.0"
    }
"""


@pytest.fixture
def mission_dir(tmp_path: Path) -> Path:
    """Temporary directory for mission files"""
    mission_dir = tmp_path / "missions"
    mission_dir.mkdir()
    return mission_dir


@pytest.fixture
def base_config(tmp_path: Path) -> Path:
    """Reforger config generator"""
    source_file = tmp_path / "source.json"
    source_file.write_text(json.dumps(BASE_CONFIG))
    return source_file
