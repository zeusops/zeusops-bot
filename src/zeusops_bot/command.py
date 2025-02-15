"""Commands that the bot can run"""

from pathlib import Path


def zeus_upload(
    modlist: list[str], scenario_id: str, filename: str, target_config_folder: Path
):
    """Convert a modlist+scenario into a file on server at given path"""
    # TODO: Jinja expand contents
    target_filepath = (target_config_folder / filename).with_suffix(".json")
    # Ensure parent folder exists
    target_filepath.parent.mkdir(parents=True, exist_ok=True)
    # Create the file itself
    target_filepath.touch()
