import abc
import sys, os
import requests
import time
import hashlib
import logging

from configparser import ConfigParser
from bs4 import BeautifulSoup

from weatherapp.core import config
from weatherapp.core.abstract.command import Command


class Configure(Command):
    """
    read and change settings from settings file
    """
    call = 0

    def __init__(self, site_name):
        super().__init__(site_name)
        Configure.call += 1
        logging.debug('init Weather_settings %s' % site_name)
        self.site_data = self.read_settings()

    def change_settings(self, current_location_url, curent_location,
                        site_search=''):
        """
        :param site_name:,
        :param current_location_url:
        :param current_location:
        :param site_url:
        :param site_search:
        :return:  save change site settings to settings.ini
        """
        config = ConfigParser()
        config.read('settings.ini', encoding='utf8')
        if self.site_name in config.sections():
            config.set(self.site_name, 'current_location_url',
                       current_location_url)
            config.set(self.site_name, 'current_location', curent_location)
            with open('settings.ini', 'w', encoding='utf8') as config_file:
                config.write(config_file)
        else:
            config.add_section(self.site_name)
            config.set(self.site_name, 'current_location_url',
                       current_location_url)
            config.set(self.site_name, 'current_location', curent_location)
            config.set(self.site_name, 'search', site_search)
            with open('settings.ini', 'w', encoding='utf8') as config_file:
                config.write(config_file)

    def read_settings(self):
        """
        :param site_name:
        :return: (search_url, place, current_location)
        """
        try:
            response = list()
            config = ConfigParser()
            config.read('settings.ini', encoding='utf8')
            for j in config.items(self.site_name):
                response.append(j[1])
            return response
        except:
            logging.exception('The settings file is broken')
            sys.stderr.write('The settings file is broken. Settings is will be rewrite.')
            with open('default_settings.ini', 'r') as default_file:
                with open('settings.ini', 'w') as file:
                    for line in default_file:
                        file.write(line)
            return self.read_settings()

    def search_place(self):
        """
        :param links_search:
        :param url:
        :return:
        """
        request_place = None
        url = self.site_data[2]
        while True:
            list_links = self.links_search(url)
            for k in sorted(list_links.keys()):
                print(k, end=', ')
            print('\n')
            try:
                print('If you wont stop search place - input "stop"')
                if len(list_links.keys()) == 0:
                    print('You chose place')
                    return (url, request_place)
                request_place = input('Input search place ')
                if request_place.lower() == 'stop':
                    return False
                else:
                    url = list_links[request_place]
            except KeyError:
                logging.exception('Bad input the search place')
                print('Not correct place')
                continue

    def chose_place(self):
        while True:
            print('Current place for weather view is {}'.format(
                self.site_data[1]))
            chose = input(
                'if you wont change place - input "yes", else - "no"').lower()
            if chose == 'yes':
                search_data = self.search_place()
                self.change_settings(search_data[0], search_data[1])
                return self.read_settings()
            elif chose == 'no':
                return self.site_data

    @staticmethod
    def display_data_weather(data_weather):
        """
        :param data_weather:
        :return: printing processed data
        """
        site_name, temperature, place, cond = data_weather[0], data_weather[1], \
                                              data_weather[2], data_weather[3]
        sys.stdout.write('The temperature in {} is {}\n'.format(place, temperature), 'from ',
              site_name)
        sys.stdout.write('The weather is {}\n'.format(cond), 'from ', site_name)

    @staticmethod
    def display_temperature_data_per_hour(temperature_data):
        """
        :param temperege_data:
        :return: min max average temperature to display
        """
        sys.stdout.write('From {} min temperature = {}, max temperature = {}, '
              'average temperature = {}'.format(temperature_data[0],
                                                temperature_data[1],
                                                temperature_data[2],
                                                temperature_data[3]))

    def bs_body_processor(self):
        """
        create data for BS
        :return:
        """
        raw_data = Cache_controller(self.site_data[0]).cache_chose()
        return BeautifulSoup(raw_data, "html.parser")

    def run(self):
        data_weather = self.parser()
        self.display_data_weather(data_weather)


class Cache_controller(Configure):
    """
    response content and create cache file
    the main function is cache_chose. He return data from site or cache.
    refresh cache - refresh data in cache
    remove cache - delete cahe data
    """

    def __init__(self, url):
        self.url = url
        self.cache_file_name = os.path.join('Cache_folder/',
                                            hashlib.md5(url.encode(
                                                'utf-8')).hexdigest() + '.txt')

    def site_request(self):
        """
        :param url:
        :return: data from site
        """
        headers = config.headers
        response = requests.get(self.url, headers=headers)
        try:
            if response.status_code != 200:
                return None
            return response.content
        except requests.exceptions.RequestException:
            logging.exception('Site response ', response.status_code)
            return None

    def cache_chose(self):
        """
        chose create or reed cache
        :return: cache_data
        """
        if 'Cache_folder' not in os.listdir():
            os.mkdir('Cache_folder')
        # file_name = self.cache_file_name
        web_data = self.site_request()
        if web_data == None:
            raw_data = self.read_cache()
            logging.debug('Old Data from file')
        elif os.path.exists(self.cache_file_name) and time.time() \
                - os.stat(self.cache_file_name).st_mtime < 60:
            raw_data = self.read_cache()
            logging.debug('Data from file')
        else:
            self.write_cache(web_data)
            raw_data = self.read_cache()
            logging.debug('Data from site')
        site_data = raw_data
        # site_data = BS_converter(raw_data)
        return site_data

    def read_cache(self):
        """
        read_cache
        :param url:
        :return:
        """
        with open(self.cache_file_name, 'r', encoding='utf-8') as f:
            site_data = f.read()
        return site_data

    @staticmethod
    def refresh_cache(self):
        """
        remove and refresh cache
        :return:
        """
        # remove_cache()
        for key in config.sites:  # переделать
            url = self.read_settings(key)
            self.cache_chose(url)

    @staticmethod
    def remove_cache():
        """
        remove and refresh cache
        :return:
        """
        for file in os.listdir('Cache_folder'):
            os.remove(os.path.join('Cache_folder', file))

    def write_cache(self, web_data):
        """
        save data in cache_file
        :param url:
        :param site_data:
        :return:
        """
        try:
            with open(self.cache_file_name, 'w+', encoding='utf-8') as f:
                f.write(web_data.decode('utf-8'))
        except IOError:
            logging.exception('Write cache exception, ')
            sys.stderr.write("An IOError has occurred!")


class WeatherProvider(Configure):

    @abc.abstractmethod
    def parser(self):
        """
        :return: site_name, temperature, place, cond from site_name
        """

    @abc.abstractmethod
    def links_search(self):
        """
        :return:
        """

    @abc.abstractmethod
    def temperature_per_hour(self):
        """
        Data from site_name
        :return: list[site_name, mit temperature, max temperature, average temperature]
        """
