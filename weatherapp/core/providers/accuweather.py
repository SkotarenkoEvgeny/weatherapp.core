import logging

from bs4 import BeautifulSoup

from weatherapp.core.abstract import Cache_controller
from weatherapp.core.abstract import WeatherProvider as Weather_settings


class AccuWeatherProvider(Weather_settings):
    call = 0

    def __init__(self):
        # (search_url, place, current_location)
        AccuWeatherProvider.call += 1
        logging.debug('init Acu', AccuWeatherProvider.call)
        self.site_name = 'accuweather.com'
        super().__init__(self.site_name)
        self.site_data = Weather_settings.read_settings(self)


    def parser(self):
        '''
        :return: site_name, temperature, place, cond from accuweather
        '''
        body = self.bs_body_processor()
        temprege = body.find('span', 'large-temp').text
        place = body.find('span', 'current-city').text
        cond = body.find('span', 'cond').text
        return (self.site_name, temprege, place, cond)

    def temperature_per_hour(self):
        '''
        Data from accuweather.com
        :return: list[site_name, mit temperature, max temperature, average
        temperature]
        '''
        body = self.bs_body_processor()
        temp = body.find(class_="hourly-table overview-hourly").table.tbody.tr
        raw_temprege_data = [int(i.text.replace('\n', '').replace('°', ''))
                             for i in temp.find_all('td')]
        return ['accuweather.com', min(raw_temprege_data),
                max(raw_temprege_data),
                sum(raw_temprege_data) / len(raw_temprege_data)]

    def links_search(url):
        '''
        :param url: accuweather url
        :return: dictionary with data for chose place
        '''
        raw_data = Cache_controller(url).cache_chose()
        body = BeautifulSoup(raw_data, "html.parser").find(id='panel-main')
        data_links = body.find_all(class_="drilldown cl")
        list_links = {}
        for info in data_links:
            list_links[str(info.find('a').em.text)] = info.find('a')['href']
        return list_links

