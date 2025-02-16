"""Validate the uploading of missions

Feature: Upload mission
  As a Zeus
  I need to upload new missions
  So that I can Zeus the next operation
"""

import json

from tests.fixtures import BASE_CONFIG, MODLIST
from zeusops_bot.command import ReforgerConfigGenerator


def test_upload_edits_files(tmp_path):
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
