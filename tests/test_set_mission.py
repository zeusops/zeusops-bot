"""Validate the set-mission command"""

import json
from pathlib import Path

from tests.fixtures import BASE_CONFIG
from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator, as_config_file


def test_load_mission(base_config: Path, mission_dir: Path):
    """Scenario: Load mission from previous upload"""
    # Given a Zeusops mission was uploaded already under <filename>
    filename = "Jib_20250228"
    uploaded_conf_path = as_config_file(mission_dir, filename)
    uploaded_conf_path.write_text(json.dumps(BASE_CONFIG))
    config_gen = ReforgerConfigGenerator(
        base_config_file=base_config, target_folder=mission_dir
    )
    # When Zeus calls "/zeus-set-mission" with <filename>
    config_gen.zeus_set_mission(filename)
    # Then a symbolic link is created from "current-config.json" to <filename>
    target = mission_dir / "current-config.json"
    assert target.exists(), "Should have created latest config symlink"
    assert target.is_symlink(), "Target config should be a symlink"
    assert target.readlink() == uploaded_conf_path.relative_to(
        mission_dir
    ), "Target should point to uploaded file"


def test_load_mission_twice(base_config: Path, mission_dir: Path):
    """Scenario: Load two missions back to back"""
    # Given a Zeusops mission was uploaded already under <filename>
    filename = "Jib_20250228"
    uploaded_conf_path = as_config_file(mission_dir, filename)
    uploaded_conf_path.write_text(json.dumps(BASE_CONFIG))
    config_gen = ReforgerConfigGenerator(
        base_config_file=base_config, target_folder=mission_dir
    )
    # And another Zeusops mission was uploaded already under <filename2>
    filename2 = "Jib_20250229"
    uploaded_conf_path2 = as_config_file(mission_dir, filename2)
    uploaded_conf_path2.write_text(json.dumps(BASE_CONFIG))
    # And Zeus has already called "/zeus-set-mission" with <filename>
    config_gen.zeus_set_mission(filename)
    # When Zeus calls "/zeus-set-mission" with <filename2>
    config_gen.zeus_set_mission(filename2)
    # Then a symbolic link is created from "current-config.json" to <filename2>
    target = mission_dir / "current-config.json"
    assert target.exists(), "Should have created latest config symlink"
    assert target.is_symlink(), "Target config should be a symlink"
    assert target.readlink() == uploaded_conf_path2.relative_to(
        mission_dir
    ), "Target should point to latest mission set"
