"""Validate the current-mission command

Feature: Show currently active mission
  As a Zeus
  I need to know the currently active mission config
  So that I can know which mission the server is running
"""

from pathlib import Path

import pytest

from zeusops_bot.errors import ConfigFileNotFound
from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator, as_config_file


def test_current_mission(mission_dir: Path, config_gen: ReforgerConfigGenerator):
    """Scenario: Show currently active mission"""
    # Given file "mission1.json" exists in the mission directory
    mission_name = "mission1"
    as_config_file(mission_dir, mission_name).touch()

    # And "mission1.json" is set as the active mission
    config_gen.zeus_set_mission(mission_name)
    # When Zeus calls "/current-mission"
    result: str = config_gen.current_mission()
    # Then "mission1" is displayed
    assert result == mission_name, "Should match previously set mission name"


def test_broken_link(mission_dir: Path, config_gen: ReforgerConfigGenerator):
    """Test that a broken link as active mission raises an error"""
    mission_name = "mission1"
    config_file = as_config_file(mission_dir, mission_name)
    config_file.touch()

    config_gen.zeus_set_mission(mission_name)
    config_file.unlink()
    with pytest.raises(ConfigFileNotFound):
        config_gen.current_mission()
