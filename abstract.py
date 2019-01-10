'''
Abstract clases for project
'''
import abc
import argparse
import sys, os
import requests
import time
import hashlib

from configparser import ConfigParser
from bs4 import BeautifulSoup

import config


class Command(abc.ABC):
    '''Base class for commands'''

    def __init__(self, site_name):
        self.site_name = site_name

    @staticmethod
    def get_parser():
        parser = argparse.ArgumentParser()
        return parser

    @abc.abstractmethod
    def run(self, argv):
        '''
        Invoced by application when the command is run
        '''


class Configure(Command):
    '''
    read and change settings from settings file
    '''
    call = 0

    def __init__(self, site_name):
        super().__init__(site_name)
        Configure.call += 1
        print('init Weather_settings', Configure.call)
        self.site_data = self.read_settings()

    def change_settings(self, current_location_url, curent_location,
                        site_search=''):
        '''
        :param site_name:,
        :param current_location_url:
        :param current_location:
        :param site_url:
        :param site_search:
        :return:  save change site settings to settings.ini
        '''
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
        '''
        :param site_name:
        :return: (search_url, place, current_location)
        '''
        try:
            response = list()
            config = ConfigParser()
            config.read('settings.ini', encoding='utf8')
            for j in config.items(self.site_name):
                response.append(j[1])
            return response
        except:
            print('The settings file is broken. Settings is will be rewrite.')
            with open('default_settings.ini', 'r') as defoult_file:
                with open('settings.ini', 'w') as file:
                    for line in defoult_file:
                        file.write(line)
            return self.read_settings()

    def search_place(self):
        '''
        :param links_search:
        :param url:
        :return:
        '''
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
                print('Not correct place')
                continue

    def chose_place(self):
        while True:
            print('Current plase for weather view is {}'.format(
                self.site_data[1]))
            chose = input(
                'if you wont change plase - input "yes", else - "no"').lower()
            if chose == 'yes':
                search_data = self.search_place()
                self.change_settings(search_data[0], search_data[1])
                return self.read_settings()
            elif chose == 'no':
                return self.site_data

    @staticmethod
    def display_data_weather(data_weather):
        '''
        :param data_weather:
        :return: printing processed data
        '''
        site_name, temprege, place, cond = data_weather[0], data_weather[1], \
                                           data_weather[2], data_weather[3]
        print('The temprege in {} is {}'.format(place, temprege), 'from ',
              site_name)
        print('The weather is {}'.format(cond), 'from ', site_name)

    @staticmethod
    def display_temperege_data_per_hour(temperege_data):
        '''
        :param temperege_data:
        :return: min max average temperage to display
        '''
        print('From {} min temperege = {}, max temperege = {}, '
              'average temperege = {}'.format(temperege_data[0],
                                              temperege_data[1],
                                              temperege_data[2],
                                              temperege_data[3]))

    def bs_body_processor(self):
        '''
        create data for BS
        :return:
        '''
        raw_data = Cache_controller(self.site_data[0]).cache_chose()
        return BeautifulSoup(raw_data, "html.parser")

    def run(self):
        data_weather = self.parser()
        self.display_data_weather(data_weather)


class Cache_controller:
    '''
    response content and create cache file
    the main function is cache_chose. He return data from site or cache.
    refresh cache - refresh data in cache
    remove cache - delete cahe data
    '''

    def __init__(self, url):
        self.url = url
        self.cache_file_name = os.path.join('Cache_folder/',
                                            hashlib.md5(url.encode(
                                                'utf-8')).hexdigest() + '.txt')

    def site_request(self):
        '''
        :param url:
        :return: data from site
        '''
        headers = config.headers
        try:
            response = requests.get(self.url, headers=headers)
            if response.status_code != 200:
                return None
            return response.content
        except requests.exceptions.RequestException as err:
            return None

    def cache_chose(self):
        '''
        chose create or reed cache
        :return: cache_data
        '''
        if 'Cache_folder' not in os.listdir():
            os.mkdir('Cache_folder')
        file_name = self.cache_file_name
        web_data = self.site_request()
        if web_data == None:
            raw_data = self.read_cache()
            print('Old Data from file')
        elif os.path.exists(self.cache_file_name) and time.time() \
                - os.stat(self.cache_file_name).st_mtime < 60:
            raw_data = self.read_cache()
            print('Data from file')
        else:
            self.write_cache(web_data)
            raw_data = self.read_cache()
            print('Data from site')
        site_data = raw_data
        # site_data = BS_converter(raw_data)
        return site_data

    def read_cache(self):
        '''
        read_cache
        :param url:
        :return:
        '''
        with open(self.cache_file_name, 'r', encoding='utf-8') as f:
            site_data = f.read()
        return site_data

    @staticmethod
    def refresh_cache():
        '''
        remove and refresh cache
        :return:
        '''
        # remove_cache()
        for key in config.sites:  # переделать
            url = self.read_settings(key)
            cache_chose(url)

    @staticmethod
    def remove_cache():
        '''
        remove and refresh cache
        :return:
        '''
        for file in os.listdir('Cache_folder'):
            os.remove(os.path.join('Cache_folder', file))

    def write_cache(self, web_data):

        '''
        save data in cache_file
        :param url:
        :param site_data:
        :return:
        '''
        try:
            with open(self.cache_file_name, 'w+', encoding='utf-8') as f:
                f.write(web_data.decode('utf-8'))
        except IOError:
            print("An IOError has occurred!")

class Prowiders(Command):

    sites = config.sites

    @staticmethod
    def providers():
        return sites


class WeatherProvider(Configure):




    @abc.abstractmethod
    def parser(self):
        '''
        :return: site_name, temprege, place, cond from site_name
        '''

    @abc.abstractmethod
    def links_search(self):
        '''
        :return:
        '''

    @abc.abstractmethod
    def temperege_per_hour(self):
        '''
        Data from site_name
        :return: list[site_name, mit temperage, max temperage, average temperage]
        '''