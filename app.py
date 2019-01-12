from argparse import ArgumentParser
import sys
import logging

import providers, config, abstract
from providermanager import ProviderManager


class App:
    '''
    WeatherApp agregator
    '''

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.arg_parser = self._arg_parse()
        self.providermanager = ProviderManager()

    def place_settings(self):
        '''
        information adaut current settings
        :return: info abaut change settings
        '''
        flag = False

        for site_name in config.sites:
            print(
                'The site {} have installed place {}'.format(site_name, \
                                                self.providermanager.get(
                                                site_name).read_settings()[1]))

        while True:
            print('If you will change place for site - input "sitename"')
            print('If you will exit? input "exit"')
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
        '''
        Initialize argument parser
        '''
        arg_parser = ArgumentParser(add_help=False)
        arg_parser.add_argument('command', help='Command', nargs="?")
        arg_parser.add_argument('--refresh', help='Bypass caches',
                                action='store_true')
        arg_parser.add_argument('--debug', action='store_true')

        return arg_parser

    def run(self, argv):

        self.options, remaining_args = self.arg_parser.parse_known_args(argv)
        command_name = self.options.command

        if not command_name:
            # run all weather providers by default
            for name, provider in self.providermanager._providers.items():
                provider.run()

        elif command_name in self.providermanager:
            # run specific provider
            provider = self.providermanager[command_name]
            provider.run()

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


# python weatherapp.py -sitename rp5.ua
# python weatherapp.py -sitename sinoptik.ua    #
# python weatherapp.py -temp_hour accuweather.com
# python weatherapp.py -sitename accuweather.com

# python weatherapp.py -s accuweather.com
# python weatherapp.py --save rp5.ua
# python weatherapp.py -rm
# python weatherapp.py -rf

def main(argv=sys.argv[1:]):
    '''
    Main entry point
    '''
    try:
        site_chose = App()
        flag = site_chose.place_settings()
        if flag == True:
            print('Change settings. Restart search')
            del site_chose
            site_chose = App()

        return site_chose.run(argv)
    except Exception as exc:
        if '--debug' in argv:
            print(exc)
        else:
            print("The programm can't work")
            print(exc)
            sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
    main(sys.argv[1:])
