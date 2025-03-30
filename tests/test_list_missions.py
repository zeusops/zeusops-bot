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
    ("filenames", "mission_names"),
    [
        (["mission1.json", "mission2.json"], ["mission1", "mission2"]),
        ([], []),
        pytest.param(
            ["mission1.json", "mission2.json", ".gitignore"],
            ["mission1", "mission2"],
            marks=pytest.mark.xfail(reason="GH#11"),
        ),
    ],
    ids=["two missions", "empty", "non-json extra"],
)
def test_list_missions(
    mission_dir: Path,
    config_gen: ReforgerConfigGenerator,
    filenames: list[str],
    mission_names: list[str],
):
    """Scenario: List uploaded missions"""
    # Given files "mission1.json" and "mission2.json" exist in the mission directory
    for filename in filenames:
        (mission_dir / filename).with_suffix(".json").touch()
    # When Zeus calls "/zeus-list"
    result: list[str] = config_gen.list_missions()
    # Then a list of mission names is returned
    assert set(result) == set(mission_names), "Should return mission names"
