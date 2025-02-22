"""Base exception classes"""


class ZeusopsBotException(Exception):
    """The base for all Zeusops Bot's exceptions"""

    pass


class ZeusopsBotConfigException(ZeusopsBotException):
    """The bot's config itself is wrong somehow"""

    pass


class BadConfigFileException(ZeusopsBotException):
    """The config file given is incorrect somehow"""

    pass


class ConfigFileNotFound(BadConfigFileException):
    """The config file was not found at given path"""

    pass


class ConfigFileInvalidJson(BadConfigFileException):
    """The config file was found but isn't valid JSON"""

    pass


class ConfigPatchingError(BadConfigFileException):
    """The config file patching didn't work"""

    pass
