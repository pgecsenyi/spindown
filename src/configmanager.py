"""
ConfigManager

Logic for managing application configuration.
"""

import configparser
import os

from config import Config

class ConfigManager(object):
    """
    Handles and persists application configuration.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, config_file_path):

        ### Validate parameters.
        if config_file_path is None:
            raise Exception('config_file_path cannot be')

        ### Attributes from the outside.
        self._config_file_path = config_file_path

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def load(self):
        """
        Loads settings from the file.
        """

        # Check if the given file exists.
        if not os.path.exists(self._config_file_path):
            raise Exception('The configuration file ({0}) does not exist.'.format(self._config_file_path))

        # Parse the configuration file.
        config_parser = configparser.RawConfigParser()
        config_parser.read(self._config_file_path)

        # Load settings.
        return self._load_config_from_parser(config_parser)

    def save(self, config):
        """
        Stores the given configuration in the file.

        Parameters
        ----------
        cofnig : Config
            The configuration settings to save.
        """

        # Instantiate configuration parser.
        config_parser = configparser.RawConfigParser()

        # Set values.
        self._save_config_to_parser(config_parser, config)

        # Store settings.
        with open(self._config_file_path, 'w') as config_file:
            config_parser.write(config_file)

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _load_config_from_parser(self, config_parser):
        """
        Creates a Config object and inflates it from the given ConfigParser.

        Parameters
        ----------
        config_parser : ConfigParser
            The configuration parser used to read the settings.

        Returns
        -------
        A Config object.
        """

        config = Config()

        # General.
        config.general.check_return_value = config_parser.getboolean('general', 'check_return_value')
        config.general.max_idle_time = config_parser.getint('general', 'max_idle_time')
        config.general.saved_stats_path = config_parser.get('general', 'saved_stats_path')
        config.general.time_format = config_parser.get('general', 'time_format')

        # Logging.
        if config_parser.has_section('logging'):

            config.logging.enable = config_parser.getboolean('logging', 'enable')
            config.logging.path = config_parser.get('logging', 'path')
            config.logging.time_format = config_parser.get('logging', 'time_format')

        # System.
        config.system.disk = config_parser.get('system', 'disk')
        config.system.hdparm_path = config_parser.get('system', 'hdparm_path')
        config.system.stats_path = config_parser.get('system', 'stats_path')

        return config

    def _save_config_to_parser(self, config_parser, config):
        """
        Saves configuration to the given ConfigParser.

        Parameters
        ----------
        config_parser : ConfigParser
            The configuration parser used to store the settings.
        config : Config
            The configuration to save.
        """

        # General.
        config_parser.add_section('general')
        config_parser.set('general', 'check_return_value', config.general.check_return_value)
        config_parser.set('general', 'saved_stats_path', config.general.saved_stats_path)
        config_parser.set('general', 'max_idle_time', config.general.max_idle_time)
        config_parser.set('general', 'time_format', config.general.time_format)

        # Logging.
        config_parser.add_section('logging')
        config_parser.set('logging', 'enable', config.logging.enable)
        config_parser.set('logging', 'path', config.logging.path)
        config_parser.set('logging', 'time_format', config.logging.time_format)

        # System.
        config_parser.add_section('system')
        config_parser.set('system', 'disk', config.system.disk)
        config_parser.set('system', 'stats_path', config.system.stats_path)
        config_parser.set('system', 'hdparm_path', config.system.hdparm_path)
