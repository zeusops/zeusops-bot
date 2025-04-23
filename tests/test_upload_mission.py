"""Validate the uploading of missions

Feature: Upload mission
  As a Zeus
  I need to upload new missions
  So that I can Zeus the next operation
"""

import json
from pathlib import Path

import pytest

from tests.fixtures import (
    BASE_CONFIG,
    MODLIST_DICTS,
    MODLIST_DICTS_VERSIONLESS,
    MODLIST_JSON,
)
from zeusops_bot.errors import ConfigFileNotFound
from zeusops_bot.models import ModDetail
from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator, extract_mods


@pytest.mark.parametrize(
    "keep_versions,mods",
    [(False, MODLIST_DICTS_VERSIONLESS), (True, MODLIST_DICTS)],
    ids=["strip versions", "keep versions"],
)
@pytest.mark.parametrize("activate", (False, True), ids=["no activate", "activate"])
def test_upload_edits_files(
    base_config: Path,
    mission_dir: Path,
    activate: bool,
    keep_versions: bool,
    mods: list[ModDetail],
):
    """Scenario: Upload next mission creates file"""
    # Given a Zeusops mission locally ready
    # And Zeus specifies <modlist.json>, <scenarioId>, <filename>
    scenario_id = "cool-scenario-1"
    filename = "Jib_20250228"
    config_gen = ReforgerConfigGenerator(
        base_config_file=base_config, target_folder=mission_dir
    )
    # When Zeus calls "/zeus-upload"
    modlist = extract_mods(MODLIST_JSON, keep_versions)
    out_path = config_gen.zeus_upload(filename, scenario_id, modlist, activate)
    # Then a new server config file is created
    assert out_path.is_file(), "Should have generated a file on disk"
    # And the config file is patched with <modlist.json> and <scenarioId>
    config = json.loads(out_path.read_text())
    assert config["game"]["scenarioId"] == scenario_id, "Should update scenarioId"
    assert isinstance(config["game"]["mods"], list)
    assert config["game"]["mods"][0] == mods[0]


def test_upload_activate_mission(base_config: Path, mission_dir: Path):
    """Scenario: Upload next mission and activate"""
    # Given a Zeusops mission locally ready
    # When Zeus calls "/zeus-upload" with the activate flag
    config_gen = ReforgerConfigGenerator(
        base_config_file=base_config, target_folder=mission_dir
    )
    modlist = extract_mods(MODLIST_JSON)
    out_path = config_gen.zeus_upload(
        "Jib_20250228", "cool-scenario-1", modlist, activate=True
    )
    # Then the server config file is set as the active mission
    target = mission_dir / "current-config.json"
    assert target.readlink() == out_path.relative_to(
        mission_dir
    ), "Target should point to uploaded file"


def test_upload_edits_files_without_modlist(base_config: Path, mission_dir: Path):
    """Scenario: Upload next mission without modlist"""
    # Given a Zeusops mission locally ready
    # And Zeus specifies <scenarioId>, <filename>
    scenario_id = "cool-scenario-1"
    filename = "Jib_20250228"
    config_gen = ReforgerConfigGenerator(
        base_config_file=base_config, target_folder=mission_dir
    )
    # When Zeus calls "/zeus-upload"
    out_path = config_gen.zeus_upload(filename, scenario_id, modlist=None)
    # Then a new server config file is created
    assert out_path.is_file(), "Should have generated a file on disk"
    # And the config file is patched with just <scenarioId>
    config = json.loads(out_path.read_text())
    assert config["game"]["scenarioId"] == scenario_id, "Should update scenarioId"
    assert isinstance(config["game"]["mods"], list)
    assert config["game"]["mods"] == BASE_CONFIG["game"]["mods"], "Should keep modlist"


@pytest.mark.xfail(raises=NotImplementedError)
def test_upload_existing_filename_without_scenarioid(
    base_config: Path, mission_dir: Path
):
    """Scenario: Update modlist of an existing mission"""
    # Given a Zeusops mission uploaded previously
    scenario_id = "cool-scenario-1"
    filename = "Jib_20250228"
    config_gen = ReforgerConfigGenerator(
        base_config_file=base_config, target_folder=mission_dir
    )
    # When Zeus calls "/zeus-upload"
    modlist = MODLIST_DICTS[0:-1]
    out_path = config_gen.zeus_upload(filename, scenario_id, modlist)
    # When Zeus calls "/zeus-upload" with an existing filename
    # And Zeus specifies <modlist.json>
    out_path = config_gen.zeus_upload(filename, scenario_id=None, modlist=MODLIST_DICTS)
    # Then the scenario ID is deduced automatically from the existing config
    config = json.loads(out_path.read_text())
    assert config["game"]["scenarioId"] == scenario_id, "Should use existing scenarioId"
    # And the existing config is updated with the new mods.
    assert isinstance(config["game"]["mods"], list)
    assert config["game"]["mods"] == MODLIST_DICTS, "Should update modlist"


@pytest.mark.xfail(raises=NotImplementedError)
def test_upload_no_scenarioid_without_file_fails(base_config: Path, mission_dir: Path):
    """Scenario: Not providing a scenario ID for a new mission produces an error"""
    # When Zeus calls "/zeus-upload" with a new filename
    # And Zeus does not specify <scenarioId>
    filename = "Jib_20250228"
    config_gen = ReforgerConfigGenerator(
        base_config_file=base_config, target_folder=mission_dir
    )
    # Then an error about a missing mission is raised.
    with pytest.raises(ConfigFileNotFound):
        config_gen.zeus_upload(filename, scenario_id=None, modlist=MODLIST_DICTS)
