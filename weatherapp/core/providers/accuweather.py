import logging

from bs4 import BeautifulSoup

from abstract import Cache_controller
from abstract import WeatherProvider as Weather_settings


class AccuWeatherProvider(Weather_settings):
    call = 0

    def __init__(self):
        # (search_url, place, current_location)
        AccuWeatherProvider.call += 1
        logging.debug('init Acu', AccuWeatherProvider.call)
        self.site_name = 'accuweather.com'
        self.site_data = Weather_settings.read_settings(self)

    def run(self):
        data_weather = self.parser()
        self.display_data_weather(data_weather)

    def parser(self):
        '''
        :return: site_name, temprege, place, cond from accuweather
        '''
        body = self.bs_body_processor()
        temprege = body.find('span', 'large-temp').text
        place = body.find('span', 'current-city').text
        cond = body.find('span', 'cond').text
        return (self.site_name, temprege, place, cond)

    def temperege_per_hour(self):
        '''
        Data from accuweather.com
        :return: list[site_name, mit temperage, max temperage, average temperage]
        '''
        body = body = self.bs_body_processor()
        temp = body.find(class_="hourly-table overview-hourly").table.tbody.tr
        raw_temprege_data = [int(i.text.replace('\n', '').replace('°', ''))
                             for i in temp.find_all('td')]
        return ['accuweather.com', min(raw_temprege_data),
                max(raw_temprege_data),
                sum(raw_temprege_data) / len(raw_temprege_data)]
