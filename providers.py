'''
The specific infirmation processing for each Provider
'''
from bs4 import BeautifulSoup

from abstract import Cache_controller
from abstract import WeatherProvider as Weather_settings


class AccuWeatherProvider(Weather_settings):
    call = 0

    def __init__(self):
        # (search_url, place, current_location)
        AccuWeatherProvider.call += 1
        print('init Acu', AccuWeatherProvider.call)
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

    def links_search(self, url):
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


class RP5Provider(Weather_settings):
    call = 0

    def __init__(self):
        # (search_url, place, current_location)
        RP5Provider.call += 1
        print('init rp5', RP5Provider.call)
        self.site_name = 'rp5.ua'
        self.site_data = Weather_settings.read_settings(self)

    def run(self):
        data_weather = self.parser()
        self.display_data_weather(data_weather)

    def parser(self):
        '''
        :return: site_name, temprege, place, cond from rp5
        '''
        body = body = self.bs_body_processor()
        temprege = body.find('span', 't_0').text
        place = body.find('div', {'id': 'pointNavi'}).text
        cond = body.find(id='forecastShort-content').find(class_='second-part')\
                   .previous.lstrip(' ')[:-2]
        return (self.site_name, temprege, place, cond)

    def links_search(self):

        raw_data = Cache_controller(self).cache_chose()
        body = BeautifulSoup(raw_data, "html.parser").find(class_='countryMap')
        if body != None:
            raw_data = body.findAll(class_='country_map_links')
            data = {}
            if raw_data != []:
                for i in raw_data:
                    data[i.b.text[:-1]] = 'http://rp5.ua' + i.b.a['href']
            else:
                raw_data = body.findAll(class_='href20')
                for i in raw_data:
                    data[i.text] = 'http://rp5.ua/' + i['href']
            return data
        else:
            return {}

    def temperege_per_hour(self):
        '''
        Data from accuweather.com
        :return: list[site_name, mit temperage, max temperage, average temperage]
        '''
        pass

# Aqu = AccuWeatherProvider()
# Aqu.run()
# print(Aqu)
