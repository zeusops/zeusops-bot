"""Reusable test fixtures, that we may need between multiple tests"""

import json
from pathlib import Path

import pytest

from zeusops_bot.models import ConfigFile, ModDetail
from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator

BASE_CONFIG: ConfigFile = {"game": {"scenarioId": "old-value", "mods": []}}

MODLIST: list[ModDetail] = [
    {"modId": "595F2BF2F44836FB", "name": "RHS - Status Quo", "version": "0.10.4075"},
    {"modId": "5EB744C5F42E0800", "name": "ACE Chopping", "version": "1.2.0"},
    {"modId": "60EAEA0389DB3CC2", "name": "ACE Trenches", "version": "1.2.0"},
]


@pytest.fixture
def mission_dir(tmp_path: Path) -> Path:
    """Temporary directory for mission files"""
    mission_dir = tmp_path / "missions"
    mission_dir.mkdir()
    return mission_dir


@pytest.fixture
def config_gen(tmp_path: Path, mission_dir: Path) -> ReforgerConfigGenerator:
    """Reforger config generator"""
    source_file = tmp_path / "source.json"
    source_file.write_text(json.dumps(BASE_CONFIG))
    gen = ReforgerConfigGenerator(
        base_config_file=source_file, target_folder=mission_dir
    )
    return gen
