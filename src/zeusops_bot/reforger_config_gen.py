"""Reforger config generation"""

import json
from pathlib import Path

import jsonpatch

from zeusops_bot import errors
from zeusops_bot.models import ModDetail

SYMLINK_FILENAME = "current-config.json"


def as_config_file(target_dest: Path, filename: str) -> Path:
    """Expands the config file path to absolute"""
    return (target_dest / filename).with_suffix(".json")


class ReforgerConfigGenerator:
    """Manages Arma Reforger config.json for variations of modlist/scenario"""

    def __init__(self, base_config_file: Path, target_folder: Path):
        """Instantiate a config generator with the base config to use"""
        self.base_config = base_config_file
        self.target_dest = target_folder

    def zeus_upload(
        self,
        scenario_id: str,
        filename: str,
        modlist: list[ModDetail] | None,
    ) -> Path:
        """Convert a modlist+scenario into a file on server at given path

        Args:
          scenario_id: The scenarioID to load within the modlist (selects mission)
          filename: The filename to store the resulting file under
          modlist: The exhaustive list of mods to load, or None to mean no change needed

        Returns:
          Path: Path to the file generated on filesystem, under {py:attr}`target_folder`

        Raises:
          ConfigFileNotFound: Base config file not found at all
          ConfigFileInvalidJson: Base config file doesn't decode as valid JSON
          ConfigPatchingError: Patching of the file failed, sending lib exception as arg

        """
        # Ensure parent folder exists
        self.target_dest.mkdir(parents=True, exist_ok=True)
        # Read the original config file
        if not self.base_config.is_file():
            raise errors.ConfigFileNotFound(self.base_config)
        try:
            base_config_content = json.loads(self.base_config.read_text())
        except json.JSONDecodeError as e:
            raise errors.ConfigFileInvalidJson(e)
        modded_config_dict = patch_file(base_config_content, modlist, scenario_id)
        target_filepath = as_config_file(self.target_dest, filename)
        # Create the file itself
        target_filepath.write_text(json.dumps(modded_config_dict))
        return target_filepath

    def zeus_set_mission(self, filename):
        """Load a mission that was previously uploaded via zeus_upload

        Args:
          filename: The partial file name that was uploaded before (eg. "Jib_20250215")

        Raises:
          ConfigFileNotFound: Loaded config file not found at all, did you zeus-upload?
        """
        self.target_dest.mkdir(parents=True, exist_ok=True)
        target_filepath = as_config_file(self.target_dest, filename)
        # Confirm the target file exists
        if not target_filepath.is_file():
            raise errors.ConfigFileNotFound(target_filepath)
        symlink_path = self.target_dest / SYMLINK_FILENAME
        symlink_path.symlink_to(target_filepath.relative_to(self.target_dest))


def patch_file(source: dict, modlist: list[ModDetail] | None, scenario_id: str) -> dict:
    """Edit the content of source with new modlist and scenarioID

    >>> modlist=[{"modId": "1", "name":"mod1"}]
    >>> patch_file({"game": {"scenarioId": "old", "mods": []}}, modlist,"new")
    {'game': {'scenarioId': 'new', 'mods': [{'modId': '1', 'name': 'mod1'}]}}
    >>> patch_file({"game": {"scenarioId": "old", "mods": []}}, None,"new")
    {'game': {'scenarioId': 'new', 'mods': []}}

    Raises:
        ConfigPatchingError: Patching of the file failed, sending lib exception as arg
    """
    patch_dict: list[dict] = [
        {"op": "replace", "path": "/game/scenarioId", "value": scenario_id},
    ]
    if modlist is not None:
        patch_dict.append({"op": "replace", "path": "/game/mods", "value": modlist})
    patch = jsonpatch.JsonPatch(patch_dict)
    try:
        mod = patch.apply(source)
    except jsonpatch.JsonPatchException as e:
        raise errors.ConfigPatchingError(e)
    return mod
