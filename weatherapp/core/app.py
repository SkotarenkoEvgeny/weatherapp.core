from argparse import ArgumentParser
import sys
import logging

from weatherapp.core import config

from weatherapp.core.providermanager import ProviderManager
<<<<<<< HEAD
=======
from weatherapp.core.commandmanager import CommandManager
>>>>>>> m05_ls14
from weatherapp.core.formatters import TableFormatter, CSV_Formatter


class App:
    """
    WeatherApp agregator
    """

    logger = logging.getLogger(__name__)
    LOG_LEVEL_MAP = {0: logging.WARNING,
                     1: logging.INFO,
                     2: logging.DEBUG}

    def __init__(self, stdin=None, stdout=None, stderr=None):
        self.stdin = stdin or sys.stdin
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr
        self.arg_parser = self._arg_parse()
        self.providermanager = ProviderManager()
        self.formatters = self._load_formatter()
<<<<<<< HEAD
=======
        self.commandmanager = CommandManager()
>>>>>>> m05_ls14

    def place_settings(self):
        """
        information about current settings
        :return: info about change settings
        """
        flag = False

        for site_name in config.sites:
            self.stdout.write(
                'The site {} have installed place {} \n'.format(site_name,
                                                             self.providermanager.get(
                                                                 site_name).read_settings()[
                                                                 1]))

        while True:
            self.stdout.write('If you will change place for site - input "sitename"')
            self.stdout.write('If you will exit? input "exit"')
            site_name = input('If not need - input "No"')
            if site_name.lower() == 'no':
                break
            elif site_name.lower() == 'exit':
                sys.exit(1)
            elif site_name in config.sites:
                self.providermanager.get(site_name).chose_place()
                flag = True
                break
            else:
                print('Not correct data')
        return flag

    def _arg_parse(self):
        """
        Initialize argument parser
        """
        arg_parser = ArgumentParser(add_help=False)
        arg_parser.add_argument('command',
                                help='Command',
                                nargs="?")
        arg_parser.add_argument('--refresh',
                                help='Bypass caches',
                                action='store_true')
        arg_parser.add_argument('--debug',
                                action='store_true')
        arg_parser.add_argument('-v', '--verbose',
                                action='count',
                                dest='verbose_level',
                                default=0,
                                help='Increase verbosity of output.')
        arg_parser.add_argument('-f', '--formatter',
                                action='store',
                                nargs='*',
                                default=['table'],
                                help="Output format, defaults to table")

        return arg_parser

    def configure_logging(self):
        """
        Create logging handlers for any log output
        """
        root_logger = logging.getLogger('')
        root_logger.setLevel(App.LOG_LEVEL_MAP[2])

        console_handler = logging.StreamHandler()
        console_handler.setLevel(
            App.LOG_LEVEL_MAP.get(self.options.verbose_level,
                                  App.LOG_LEVEL_MAP[0]))

        info_formater = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

        console_handler.setFormatter(info_formater)

        root_logger.addHandler(console_handler)


    @staticmethod
    def _load_formatter():
        return {'table': TableFormatter, 'csv': CSV_Formatter}

    def produce_output(self, data):
        """
        Print results.
        """
        formatter = self.formatters.get(self.options.formatter[0], 'table')()
        self.stdout.write(formatter.emit(data))
        self.stdout.write('\n')

    def run_provider(self, name):
        """
        Run specified provider
        """
        provider = self.providermanager.get(name)
        data = list()
        if provider:
            data.append(provider.data_for_table())
            self.produce_output(data)

    def run_providers(self):
        """
        Execute all available providers.
        data for table = list(site_name, temperature, place, cond)
        """
        data = list()
        for name, provider in self.providermanager._providers.items():
            provider = provider.data_for_table()
            data.append(provider)
        self.produce_output(data)


    def run(self, argv):

        self.options, remaining_args = self.arg_parser.parse_known_args(argv)
        print(self.options)
        command_name = self.options.command
        self.configure_logging()


        if not command_name:
            # run all weather providers by default
            self.run_providers()

        elif command_name in self.providermanager:
            # run specific provider
            self.run_provider(command_name)


    def __del__(self):
        pass


"""
    parser = argparse.ArgumentParser(description='returt weather information from chosen site')
    parser.add_argument('-rf', '--refresh', action='store_true', help='Refresh cach file')
    parser.add_argument('-rm', '--remove', action='store_true', help='Clear cach file')
    parser.add_argument('-sitename', help=str(site_functions.keys()), nargs=1, type=str)
    parser.add_argument('-temp_hour', help='Temprege per hour', nargs=1, type=str)
    parser.add_argument('-s', '--save', help='Save data from {sitename} to file', nargs=1, type=str)
    args = parser.parse_args()

    if args.sitename != None:
        display_data_weather(site_functions[args.sitename[0]]())
    if args.temp_hour != None:
        display_temperege_data_per_hour(temprege_per_hour[args.temp_hour[0]]())
    if args.save != None:
        save_data_to_file(site_functions[args.save[0]]())
    if args.refresh != False:
        refresh_cache()
    if args.remove != False:
        remove_cache()


"""


# import pdb; pdb.set_trace()

# python weatherapp.py -sitename rp5.ua
# python weatherapp.py -sitename sinoptik.ua    #
# python weatherapp.py -temp_hour accuweather.com
# python weatherapp.py -sitename accuweather.com

# python weatherapp.py -s accuweather.com
# python weatherapp.py --save rp5.ua
# python weatherapp.py -rm
# python weatherapp.py -rf

def main(argv=sys.argv[1:]):
    """
    Main entry point
    """
    try:
        site_chose = App()
        flag = site_chose.place_settings()
        if flag == True:
            print('Change settings. Restart search')
            del site_chose
            site_chose = App()

        return site_chose.run(argv)
    except Exception as exc:
        logging.exception(exc)
        if '--debug' in argv:
            print(exc)
        else:
            print("The programm can't work")
            print(exc)
            sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
