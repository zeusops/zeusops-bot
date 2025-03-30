"""Reforger config generation"""

import json
from pathlib import Path

import jsonpatch
from pydantic import TypeAdapter, ValidationError

from zeusops_bot import errors
from zeusops_bot.errors import ConfigFileInvalidJson
from zeusops_bot.models import ModDetail

modlist_typeadapter = TypeAdapter(list["ModDetail"])

SYMLINK_FILENAME = "current-config.json"


def as_config_file(target_dest: Path, filename: str) -> Path:
    """Expands the config file path to absolute"""
    return (target_dest / filename).with_suffix(".json")


class ReforgerConfigGenerator:
    """Manages Arma Reforger config.json for variations of modlist/scenario"""

    def __init__(self, base_config_file: Path, target_folder: Path):
        """Instantiate a config generator with the base config to use

        Args:
          base_config_file: The filename of a reference Reforger config
          target_folder: The folder to place generated config files in
        """
        self.base_config = base_config_file
        self.target_dest = target_folder

    def zeus_upload(
        self,
        scenario_id: str,
        filename: str,
        modlist: list[ModDetail] | None,
        activate: bool = False,
    ) -> Path:
        """Convert a modlist+scenario into a file on server at given path

        Args:
          scenario_id: The scenarioID to load within the modlist (selects mission)
          filename: The filename to store the resulting file under
          modlist: The exhaustive list of mods to load, or None to mean no change needed
          activate: If set to true, the added config is immediately set as the
                    currently active config

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
        target_filepath.write_text(json.dumps(modded_config_dict, indent=4))
        if activate:
            self.zeus_set_mission(target_filepath)
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
        link_dest = target_filepath.relative_to(self.target_dest)
        # Python throws FileExistsError on existing link, doesn't allow
        # 'ln --force': use a temp file and rename atomically instead
        temp_symlink_path = symlink_path.with_suffix(".tmp")
        temp_symlink_path.symlink_to(link_dest)
        # NOTE: Will not work as expected on Windows, raises a
        # FileExistsError instead of replacing the target
        temp_symlink_path.rename(symlink_path)

    def list_missions(self) -> list[str]:
        """List all missions available in the config folder

        Returns:
          List of mission names available in the folder
        """
        entries = self.target_dest.iterdir()
        ignored_names = [SYMLINK_FILENAME, "config.json"]
        mission_names = [
            entry.stem
            for entry in entries
            if entry.is_file() and entry.name not in ignored_names
        ]
        return mission_names

    def current_mission(self) -> str:
        """Show currently active mission

        Returns:
          Currently active mission name

        Raises:
          ConfigFileNotFound: Mission symlink was found but points to a
                              non-existent mission.
        """
        symlink_path = self.target_dest / SYMLINK_FILENAME
        target = symlink_path.readlink()
        if not (symlink_path.parent / target).exists():
            raise errors.ConfigFileNotFound(
                f"Current mission points to a missing config {target}"
            )
        return target.stem


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


def extract_mods(modlist: str | None, keep_versions=False) -> list[ModDetail] | None:
    """Extracts a list of ModDetail entries from a mod list exported from Reforger

    Args:
      modlist: A partial JSON string of mods to extract. Can be None if the
               user did not provide any mods, in which case the operation is a
               no-op.
      keep_versions: Preserve mod versions in the extracted list of mods.

    Raises:
      pydantic.ValidationError: Generic error in validating the mod list
      ConfigFileInvalidJson: The input was not valid JSON

    Returns:
      A list of ModDetail, or None if the input was None.
    """
    if modlist is None:
        return None
    modlist = f"[{modlist}]"
    try:
        return modlist_typeadapter.validate_json(modlist)
    except ValidationError as e:
        errors = e.errors()
        if len(errors) > 1:
            # Got more than 1 error, not our problem
            raise e
        error = errors[0]
        match error["type"]:
            case "json_invalid":
                raise ConfigFileInvalidJson(e)
            case _:
                # Unknown error
                raise e
