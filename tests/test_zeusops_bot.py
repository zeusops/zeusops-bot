"""Basic tests of zeusops_bot CLI

Feature: Upload mission
  As a Zeus
  I need to upload new missions
  So that I can Zeus the next operation
"""

from zeusops_bot.command import zeus_upload


def test_upload_creates_files(tmp_path):
    """Scenario: Upload next mission creates file"""
    # Given a Zeusops mission locally ready
    # And Zeus specifies <modlist.json>, <scenarioId>, <filename>
    modlist: list[str] = []
    scenario_id = "cool-scenario-1"
    filename = "Jib_20250228"
    dest = tmp_path / "data"
    # When Zeus calls "/zeus-upload"
    zeus_upload(modlist, scenario_id, filename, dest)
    # Then a new server config file is created
    target_path = (dest / filename).with_suffix(".json")
    assert target_path.is_file(), "Should have generated a file on disk"
