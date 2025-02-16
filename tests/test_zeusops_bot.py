"""Basic tests of zeusops_bot CLI

Feature: Upload mission
  As a Zeus
  I need to upload new missions
  So that I can Zeus the next operation
"""

import json

from zeusops_bot.command import ReforgerConfigGenerator
from zeusops_bot.models import ConfigFile, ModDetail

BASE_CONFIG: ConfigFile = {"game": {"scenarioId": "old-value", "mods": []}}

MODLIST: list[ModDetail] = [
    {"modId": "595F2BF2F44836FB", "name": "RHS - Status Quo", "version": "0.10.4075"},
    {"modId": "5EB744C5F42E0800", "name": "ACE Chopping", "version": "1.2.0"},
    {"modId": "60EAEA0389DB3CC2", "name": "ACE Trenches", "version": "1.2.0"},
]


def test_upload_creates_files(tmp_path):
    """Scenario: Upload next mission creates file"""
    # Given a Zeusops mission locally ready
    # And Zeus specifies <modlist.json>, <scenarioId>, <filename>
    scenario_id = "cool-scenario-1"
    filename = "Jib_20250228"
    dest = tmp_path / "data"
    source_file = tmp_path / "source.json"
    source_file.write_text(json.dumps(BASE_CONFIG))
    gen = ReforgerConfigGenerator(base_config_file=source_file, target_folder=dest)
    # When Zeus calls "/zeus-upload"
    out_path = gen.zeus_upload(MODLIST, scenario_id, filename)
    # Then a new server config file is created
    assert out_path.is_file(), "Should have generated a file on disk"
    # And the config file is patched with <modlist.json> and <scenarioId>
    config = json.loads(out_path.read_text())
    assert config["game"]["scenarioId"] == scenario_id, "Should update scenarioId"
    assert config["game"]["mods"] == MODLIST, "Should update modlist"
