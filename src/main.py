"""
Main module.
"""

import getopt
import sys

from app import App
from config import Config
from configmanager import ConfigManager

DEFAULT_CONFIG_PATH = 'config.cfg'

def main(application_name, arguments):
    """
    Main procedure.

    Parameters
    ----------
    application_name : str
        The name of the application (used in console messages).
    arguments : list of str
        The command line arguments passed to the interpreter (beside the name of the script).
    """

    # Parse command line arguments.
    is_config_generation_requested = False
    config_file_path = DEFAULT_CONFIG_PATH

    try:
        opts, _ = getopt.getopt(arguments, 'c:ih', ['config=', 'install'])
    except getopt.GetoptError:
        print_usage_and_exit(application_name, 2)

    for opt, arg in opts:
        if opt in ('-c', '--config'):
            config_file_path = arg
        elif opt in ('-h', '--help'):
            print_usage_and_exit(application_name)
        elif opt in ('-i', '--install'):
            is_config_generation_requested = True

    config_manager = ConfigManager(config_file_path)

    # Create configuration file and exit.
    if is_config_generation_requested:
        config = Config()
        config.create_default()
        config_manager.save(config)
    # Load configuration, then go ahead.
    else:
        config = config_manager.load()
        app = App(config)
        app.execute()

def print_usage_and_exit(application_name, error_code=0):
    """
    Prints a short manual and exists the application.

    Parameters
    ----------
    application_name : str
        The name of the application (used in console messages).
    error_code : int
        The error code to exit with.
    """

    print('python {0} <options>'.format(application_name))
    print('')
    print('  -c, --config    Use the specified configuration file instead')
    print('                  of the default ({0}) one.'.format(DEFAULT_CONFIG_PATH))
    print('  -i, --install   Generate a sample configuration file and exit.')
    print('  -h, --help      Print this help and exit.')
    print('')

    sys.exit(error_code)

if __name__ == '__main__':

    try:
        main(sys.argv[0], sys.argv[1:])
    except Exception as exception:
        print(exception)
        exit(1)
