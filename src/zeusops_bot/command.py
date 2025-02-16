"""Commands that the bot can run"""

from pathlib import Path


class ReforgerConfigGenerator:
    """Manages Arma Reforger config.json for variations of modlist/scenario"""

    def __init__(self, base_config_file: Path, target_folder: Path):
        """Instantiate a config generator with the base config to use"""
        self.base_config = base_config_file
        self.target_dest = target_folder

    def zeus_upload(
        self,
        modlist: list[str],
        scenario_id: str,
        filename: str,
    ):
        """Convert a modlist+scenario into a file on server at given path"""
        # TODO: Jinja expand contents
        target_filepath = (self.target_dest / filename).with_suffix(".json")
        # Ensure parent folder exists
        target_filepath.parent.mkdir(parents=True, exist_ok=True)
        # Create the file itself
        target_filepath.touch()
