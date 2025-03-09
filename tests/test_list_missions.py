"""Validate the zeus-list command

Feature: List uploaded mission configs
  As a Zeus
  I need to see a list of uploaded mission configs
  So that I can choose which mission to load
"""

from pathlib import Path

import pytest

from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator


@pytest.mark.parametrize(
    "mission_names", [["mission1", "mission2"], []], ids=["two missions", "empty"]
)
def test_list_missions(tmp_path: Path, mission_names: list[str]):
    """Scenario: List uploaded missions"""
    # Given files "mission1.json" and "mission2.json" exist in the mission directory
    mission_dir = tmp_path / "missions"
    mission_dir.mkdir()
    for mission_name in mission_names:
        (mission_dir / mission_name).with_suffix(".json").touch()
    source_file = tmp_path / "source.json"
    source_file.touch()
    gen = ReforgerConfigGenerator(
        base_config_file=source_file, target_folder=mission_dir
    )
    # When Zeus calls "/zeus-list"
    result: list[str] = gen.list_missions()
    # Then a list of mission names is returned
    assert result == mission_names, "Should return mission names"
