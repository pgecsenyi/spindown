"""
Config

Data structure to store configuration.
"""

class Config(object):
    """
    Stores application settings.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.general = GeneralConfig()
        self.logging = LoggingConfig()
        self.system = SystemConfig()

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def create_default(self):
        """
        Generates a sample configuration.
        """

        self.general.check_return_value = True
        self.general.max_idle_time = 720
        self.general.saved_stats_path = '/var/tmp/spindown/savedstats.txt'
        self.general.time_format = '%Y%m%d%H%M%S'
        self.logging.enable = False
        self.logging.path = '/var/tmp/spindown/log.txt'
        self.logging.time_format = '[%Y.%m.%d. %H:%M:%S]'
        self.system.disk = 'sda'
        self.system.hdparm_path = '/sbin/hdparm'
        self.system.stats_path = '/proc/diskstats'

class GeneralConfig(object):
    """
    Stores general application settings.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.check_return_value = False
        self.max_idle_time = 0 # seconds
        self.saved_stats_path = ''
        self.time_format = ''

class LoggingConfig(object):
    """
    Stores logging related application settings.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.enable = False
        self.path = ''
        self.time_format = ''

class SystemConfig(object):
    """
    Stores sytem parameters.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self):

        ### Public attributes.
        self.disk = ''
        self.hdparm_path = ''
        self.stats_path = ''
