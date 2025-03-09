"""Validate the set-mission command"""

import json

from tests.fixtures import BASE_CONFIG
from zeusops_bot.reforger_config_gen import ReforgerConfigGenerator, as_config_file


def test_load_mission(tmp_path):
    """Scenario: Load mission from previous upload"""
    # Given a Zeusops mission was uploaded already under <filename>
    config_base = tmp_path / "reforger_configs"
    filename = "Jib_20250228"
    uploaded_conf_path = as_config_file(config_base, filename)
    uploaded_conf_path.parent.mkdir(parents=True, exist_ok=True)
    gen = ReforgerConfigGenerator(
        base_config_file=uploaded_conf_path, target_folder=config_base
    )
    uploaded_conf_path.write_text(json.dumps(BASE_CONFIG))
    # When Zeus calls "/zeus-set-mission" with <filename>
    base_conf = tmp_path / "base.json"
    base_conf.write_text(json.dumps(BASE_CONFIG))
    gen.zeus_set_mission(filename)
    # Then a symbolic link is created from "current-config.json" to <filename>
    target = config_base / "current-config.json"
    assert target.exists(), "Should have created latest config symlink"
    assert target.is_symlink(), "Target config should be a symlink"
    assert target.readlink() == uploaded_conf_path.relative_to(
        config_base
    ), "Target should point to uploaded file"


def test_load_mission_twice(tmp_path):
    """Scenario: Load two missions back to back"""
    # Given a Zeusops mission was uploaded already under <filename>
    config_base = tmp_path / "reforger_configs"
    filename = "Jib_20250228"
    uploaded_conf_path = as_config_file(config_base, filename)
    uploaded_conf_path.parent.mkdir(parents=True, exist_ok=True)
    gen = ReforgerConfigGenerator(
        base_config_file=uploaded_conf_path, target_folder=config_base
    )
    uploaded_conf_path.write_text(json.dumps(BASE_CONFIG))
    # And another Zeusops mission was uploaded already under <filename2>
    filename2 = "Jib_20250229"
    uploaded_conf_path2 = as_config_file(config_base, filename2)
    uploaded_conf_path2.write_text(json.dumps(BASE_CONFIG))
    # And Zeus has already called "/zeus-set-mission" with <filename>
    gen.zeus_set_mission(filename)
    # When Zeus calls "/zeus-set-mission" with <filename2>
    gen.zeus_set_mission(filename2)
    # Then a symbolic link is created from "current-config.json" to <filename2>
    target = config_base / "current-config.json"
    assert target.exists(), "Should have created latest config symlink"
    assert target.is_symlink(), "Target config should be a symlink"
    assert target.readlink() == uploaded_conf_path2.relative_to(
        config_base
    ), "Target should point to latest mission set"
