"""Validate the zeus-list command

Feature: List uploaded mission configs
  As a Zeus
  I need to see a list of uploaded mission configs
  So that I can choose which mission to load
"""

from pathlib import Path

from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator


def test_list_missions(tmp_path: Path):
    """Scenario: List uploaded missions"""
    # Given files "mission1.json" and "mission2.json" exist in the mission directory
    mission_name1 = "mission1"
    mission_name2 = "mission2"
    mission_dir = tmp_path / "missions"
    mission_dir.mkdir()
    (mission_dir / mission_name1).with_suffix(".json").touch()
    (mission_dir / mission_name2).with_suffix(".json").touch()
    source_file = tmp_path / "source.json"
    source_file.touch()
    gen = ReforgerConfigGenerator(
        base_config_file=source_file, target_folder=mission_dir
    )
    # When Zeus calls "/zeus-list"
    result: list[str] = gen.list_missions()
    # Then a list of mission names is returned
    assert [mission_name1, mission_name2] == result, "Should return mission names"
