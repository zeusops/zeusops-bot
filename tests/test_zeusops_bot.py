"""Basic tests of zeusops_bot CLI

Feature: Upload mission
  As a Zeus
  I need to upload new missions
  So that I can Zeus the next operation
"""

from zeusops_bot.command import ReforgerConfigGenerator


def test_upload_creates_files(tmp_path):
    """Scenario: Upload next mission creates file"""
    # Given a Zeusops mission locally ready
    # And Zeus specifies <modlist.json>, <scenarioId>, <filename>
    modlist: list[str] = []
    scenario_id = "cool-scenario-1"
    filename = "Jib_20250228"
    dest = tmp_path / "data"
    source_file = tmp_path / "source.json"
    source_file.write_text('{"key": "value"}')
    gen = ReforgerConfigGenerator(base_config_file=source_file, target_folder=dest)
    # When Zeus calls "/zeus-upload"
    gen.zeus_upload(modlist, scenario_id, filename)
    # Then a new server config file is created
    target_path = (dest / filename).with_suffix(".json")
    assert target_path.is_file(), "Should have generated a file on disk"
