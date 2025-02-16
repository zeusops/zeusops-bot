"""Commands that the bot can run"""

import json
from pathlib import Path

import jsonpatch

from zeusops_bot import errors
from zeusops_bot.models import ModDetail


class ReforgerConfigGenerator:
    """Manages Arma Reforger config.json for variations of modlist/scenario"""

    def __init__(self, base_config_file: Path, target_folder: Path):
        """Instantiate a config generator with the base config to use"""
        self.base_config = base_config_file
        self.target_dest = target_folder

    def zeus_upload(
        self,
        modlist: list[ModDetail],
        scenario_id: str,
        filename: str,
    ) -> Path:
        """Convert a modlist+scenario into a file on server at given path

        Args:
          modlist: The exhaustive list of mods to load
          scenario_id: The scenarioID to load within the modlist (selects mission)
          filename: The filename to store the resulting file under

        Returns:
          Path: Path to the file generated on filesystem, under :py:attr:`target_folder`

        Raises:
          ConfigFileNotFound: Base config file not found at all
          ConfigFileInvalidJson: Base config file doesn't decode as valid JSON
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
        target_filepath = (self.target_dest / filename).with_suffix(".json")
        # Create the file itself
        target_filepath.write_text(json.dumps(modded_config_dict))
        return target_filepath


def patch_file(source: dict, modlist: list[ModDetail], scenario_id: str) -> dict:
    """Edit the content of source with new modlist and scenarioID

    >>> modlist=[{"modId": "1", "name":"mod1"}]
    >>> patch_file({"game": {"scenarioId": "old", "mods": []}}, modlist,"new")
    {'game': {'scenarioId': 'new', 'mods': [{'modId': '1', 'name': 'mod1'}]}}

    Raises:
        ConfigPatchingError: Patching of the file failed, sending lib exception as arg
    """
    patch = jsonpatch.JsonPatch(
        [
            {"op": "replace", "path": "/game/scenarioId", "value": scenario_id},
            {"op": "replace", "path": "/game/mods", "value": modlist},
        ]
    )
    try:
        mod = patch.apply(source)
    except jsonpatch.JsonPatchException as e:
        raise errors.ConfigPatchingError(e)
    return mod
