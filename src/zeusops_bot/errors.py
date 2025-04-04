"""Base exception classes"""


class ZeusopsBotException(Exception):
    """The base for all Zeusops Bot's exceptions"""

    pass


class ZeusopsBotConfigException(ZeusopsBotException):
    """The Discord bot config itself is wrong somehow"""

    pass


class BadConfigFileException(ZeusopsBotException):
    """The Reforger config file given is incorrect somehow"""

    pass


class ConfigFileNotFound(BadConfigFileException):
    """The Reforger config file was not found at given path"""

    pass


class ConfigFileInvalidJson(BadConfigFileException):
    """The Reforger config file was found but isn't valid JSON"""

    pass


class ConfigPatchingError(BadConfigFileException):
    """The Reforger config file patching didn't work"""

    pass
