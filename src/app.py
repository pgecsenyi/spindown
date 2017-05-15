"""
App

Core application logic.
"""

from datetime import datetime
from os.path import exists
import re
import subprocess

class App(object):
    """
    Implements core application logic.
    """

    ####################################################################################################################
    # Constructor.
    ####################################################################################################################

    def __init__(self, config):

        ### Validate parameters.
        if config is None:
            raise Exception('config cannot be')

        ### Attributes from the outside.
        self._config = config

    ####################################################################################################################
    # Public methods.
    ####################################################################################################################

    def execute(self):
        """
        Acquire disk info from the system and compare it with the saved state. Then act accordingly.
        """

        try:

            self._log('Checking disk state for /dev/{}'.format(self._config.system.disk))

            # Get disk statistics.
            new_stats_line = self._read_sys_stats()

            # In case there is no saved information yet, save the current state and exit.
            if not exists(self._config.general.saved_stats_path):
                self._save_stats(new_stats_line, 0)
                exit(0)

            # Analyze new statistics.
            self._analyze_new_stats(new_stats_line)

        except Exception as exception:

            print('Unexpected error.', exception)
            self._log('Unexpected error. ' + str(exception))
            exit(1)

    ####################################################################################################################
    # Private methods.
    ####################################################################################################################

    def _analyze_new_stats(self, new_stats):
        """
        Compares saved and new state and acts accordingly.
        """

        with open(self._config.general.saved_stats_path, 'r') as saved_stats_file:

            # Get and check statistics. Exit if the disk was used in the meantime.
            saved_stats = saved_stats_file.readline()[:-1]
            self._compare_stats_and_exit(saved_stats, new_stats)

            # Check if the disk is already in standby mode.
            is_in_standby = saved_stats_file.readline()[:-1]
            self._check_standby_and_exit(is_in_standby)

            # Get and check timestamp.
            last_change_time = saved_stats_file.readline()[:-1]
            self._check_idle_time_and_shutdown(last_change_time, new_stats)

    def _check_idle_time_and_shutdown(self, last_change_time_str, new_stats):
        """
        Checks if enough time has been passed in idle mode.

        Parameters
        ----------
        last_change_time_str : str
            The time of the last check as string.
        new_stats : str
            The new statistics info to be saved.
        """

        last_change_time = datetime.strptime(last_change_time_str, self._config.general.time_format)
        time_difference = datetime.now() - last_change_time
        idle_time = time_difference.total_seconds()
        if idle_time > self._config.general.max_idle_time:
            self._shutdown_disk(new_stats)

    def _check_standby_and_exit(self, saved_state):
        """
        Checks if the disk is already in standby mode based on the saved statistics and if so, exits the program.

        Parameters
        ----------
        saved_state : str
            0 or 1 as a string. '0' indicates that the disk is operational, '1' indicates that it is already in standby
            mode.
        """

        if saved_state == str(1):
            self._log('Disk /dev/{} is in standby mode'.format(self._config.system.disk))
            exit(0)

    def _compare_stats_and_exit(self, saved_stats, new_stats):
        """
        Compares the saved state with the fresh one and exits if there has been any change.

        Parameters
        ----------
        saved_stats : str
            The saved statistics.
        new_stats : str
            The new statistics.
        """

        if saved_stats != new_stats:
            self._log('State of /dev/{} has been changed'.format(self._config.system.disk))
            self._save_stats(new_stats, 0)
            exit(0)

    def _log(self, message):
        """
        Logs the given message.

        Parameters
        ----------
        message : str
            The message to log.
        """

        if self._config.logging.enable is True:
            with open(self._config.logging.path, 'a') as log_file:
                formatted_time = datetime.now().strftime(self._config.logging.time_format)
                log_file.write('{} {}\n'.format(formatted_time, message))

    def _read_sys_stats(self):
        """
        Reads information the system knows about that specific disk.
        """

        with open(self._config.system.stats_path, 'r') as stats_file:
            for line in stats_file.readlines():
                disk_pattern = re.compile(r'\s+\d+\s+\d+\s+' + self._config.system.disk + r'\s')
                disk_pattern_match = disk_pattern.search(line)
                if disk_pattern_match != None and disk_pattern_match != '':
                    return line[:-2]

        return ''

    def _save_stats(self, stats, flag):
        """
        Saves current state.

        Parameters
        ----------
        stats : stats
            The copied line of the 'diskstats' file.
        flag : int
            Indicates whether the disk is in standby mode.
        """

        with open(self._config.general.saved_stats_path, 'w') as output_file:
            output_file.write(stats + '\n')
            output_file.write(str(flag) + '\n')
            output_file.write(datetime.now().strftime(self._config.general.time_format) + '\n')

    def _shutdown_disk(self, new_stats):
        """
        Puts the disk in standby mode using the 'hdparm' utility.

        Parameters
        ----------
        new_stats : str
            The new statistics data to be saved.
        """

        self._log('Setting standby mode for /dev/{}'.format(self._config.system.disk))

        program = [self._config.system.hdparm_path, '-y', '/dev/' + self._config.system.disk]
        ret = subprocess.call(program)

        if (not self._config.general.check_return_value) or (ret == 0):
            self._save_stats(new_stats, 1)
        else:
            self._save_stats(new_stats, 0)
