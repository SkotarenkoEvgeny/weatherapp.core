import sys, os
import requests
import argparse
import datetime

from bs4 import BeautifulSoup
from configparser import ConfigParser


def site_request(url):
    '''
    :param url:
    :return: page data from url
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/70.0.3538.102 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(1)


def display_data_weather(data_weather):
    '''
    :param data_weather:
    :return: printing processed data
    '''
    site_name, temprege, place, cond = data_weather[0], data_weather[1], data_weather[2], data_weather[3]
    print('The temprege in {} is {}'.format(place, temprege), 'from ', site_name)
    print('The weather is {}'.format(cond), 'from ', site_name)


def display_temperege_data_per_hour(temperege_data):
    '''
    :param temperege_data:
    :return: min max average temperage to display
    '''
    print('From {} min temperege = {}, max temperege = {}, average temperege = {}'.format(temperege_data[0],
                                                                                          temperege_data[1],
                                                                                          temperege_data[2],
                                                                                          temperege_data[3]))


def save_data_to_file(data_weather):
    '''
    you cann use argument -s(or --save) {name site}
    :param data_weather:
    :return: save weather data to file
    '''
    if 'Data_weather' not in os.listdir():
        os.mkdir('Data_weather')
    site_name, temprege, place, cond = data_weather[0], data_weather[1], data_weather[2], data_weather[3]
    file_name = os.path.join('Data_weather/', site_name + str(datetime.date.today()) + '.txt')
    try:
        with open(file_name, 'w+', encoding='utf-8') as f:
            f.write(str(datetime.date.today()) + '\n')
            for i in range(1, len(data_weather)):
                f.write(str(data_weather[i]) + '\n')
    except IOError:
        print("An IOError has occurred!")


def search_place(links_search, url):
    '''
    :param links_search:
    :param url:
    :return:
    '''
    while True:
        list_links = links_search(url)
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


def change_settings(site_name, current_location_url, curent_location, site_search=''):
    '''
    :param site_name:
    :param current_location_url:
    :param current_location:
    :param site_url:
    :param site_search:
    :return:  save change site settings to settings.ini
    '''
    config = ConfigParser()
    config.read('settings.ini')
    if site_name in config.sections():
        config.set(site_name, 'current_location_url', current_location_url)
        config.set(site_name, 'current_location', curent_location)
        with open('settings.ini', 'w') as config_file:
            config.write(config_file)
    else:
        config.add_section(site_name)
        config.set(site_name, 'current_location_url', current_location_url)
        config.set(site_name, 'current_location', curent_location)
        config.set(site_name, 'search', site_search)
        with open('settings.ini', 'w') as config_file:
            config.write(config_file)


def read_settings(site_name):
    '''
    :param site_name:
    :return: (search_url, place, current_location)
    '''
    response = list()
    config = ConfigParser()
    config.read('settings.ini')
    for j in config.items(site_name):
        response.append(j[1])
    return response


def chose_place(site_name):
    site_data = read_settings(site_name) # recive place url and search url from settings.ini
    while True:
        print('Current plase for weather view is {}'.format(site_data[1]))
        chose = input('if you wont change plase - input "yes", else - "no"').lower()
        if chose == 'yes':
            search_data = search_place(site_change_place[site_name], site_data[2])
            change_settings(site_name, search_data[0], search_data[1], site_search='')
            return read_settings(site_name)
        elif chose == 'no':
            return site_data


def place_settings():
    '''
    :return: information adaut current settings
    '''
    for site_name in site_functions.keys():
        print('The site {} have installed place {}'.format(site_name, read_settings(site_name)[1]))

def accuweather_parser():
    '''
    :return: site_name, temprege, place, cond from accuweather
    '''
    site_name = 'accuweather.com'
    url = read_settings(site_name)[0]
    body = site_request(url)
    temprege = body.find('span', 'large-temp').text
    place = body.find('span', 'current-city').text
    cond = body.find('span', 'cond').text
    return (site_name, temprege, place, cond)


def accuweather_temperege_per_hour():
    '''
    Data from accuweather.com
    :return: list[site_name, mit temperage, max temperage, average temperage]
    '''
    url = 'https://www.accuweather.com/uk/ua/kyiv/324505/hourly-weather-forecast/324505'
    body = site_request(url)
    temp = body.find(class_="hourly-table overview-hourly").table.tbody.tr
    raw_temprege_data = [int(i.text.replace('\n', '').replace('°', '')) for i in temp.find_all('td')]
    return ['accuweather.com', min(raw_temprege_data), max(raw_temprege_data),
            sum(raw_temprege_data) / len(raw_temprege_data)]


def accuweather_links_search(url):
    '''
    :param url: accuweather url
    :return: dictionary with data for chose place
    '''
    body = site_request(url).find(id='panel-main')
    data_links = body.find_all(class_="drilldown cl")
    list_links = {}
    for info in data_links:
        list_links[str(info.find('a').em.text)] = info.find('a')['href']
    return list_links


def rp5_parser():
    '''
    :return: site_name, temprege, place, cond from rp5
    '''
    site_name = 'rp5.ua'
    url = 'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B8%D1%94%D0%B2%D1%96'
    body = site_request(url)
    temprege = body.find('span', 't_0').text
    place = body.find('div', {'id': 'pointNavi'}).text
    cond = body.find(id='forecastShort-content').find(class_='second-part').previous.lstrip(' ')[:-2]
    return (site_name, temprege, place, cond)


def rp5_links_search(url):
    body = site_request(url).find(class_='countryMap')
    if body != None:
        raw_data = body.findAll(class_='country_map_links')
        data ={}
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


def sinoptik_parser():
    '''
    :return: site_name, temprege, place, cond from sinoptik
    '''
    site_name = 'sinoptik.ua/'
    url = 'https://sinoptik.ua/'
    body = site_request(url)
    temprege = body.find(class_='main loaded', id='bd1').find(class_='temperature').find(class_='min').span.text
    place = body.find(class_='isMain').next.next.next.next
    place = place[3:len(place) - 2]
    cond = body.find(class_='main loaded', id='bd1').find(class_='weatherIco')['title'].lower()
    return (site_name, temprege, place, cond)



site_functions = {'accuweather.com': accuweather_parser,
                    'rp5.ua': rp5_parser,
                  'sinoptik.ua': sinoptik_parser}
site_change_place = {'accuweather.com': accuweather_links_search,
                    'rp5.ua': rp5_links_search,
                  'sinoptik.ua': ''}

'''
site_functions = {'accuweather.com': (accuweather_parser, accuweather_links_search,
                             accuweather_temperege_per_hour),
                    'rp5.ua': (rp5_parser),
                  'sinoptik.ua': (sinoptik_parser)}
'''


if __name__ == '__main__':

    while True:
        place_settings()
        print('If you will change place for site - input "sitename"')
        print('If you will exit? input "exit"')
        site_name = input('If not need - input "No"')
        if site_name.lower() == 'no':
            break
        elif site_name.lower() == 'exit':
            sys.exit(1)
        elif site_name in site_functions:
            chose_place(site_name)
        else:
            print('Not correct data')

    parser = argparse.ArgumentParser(description='returt weather information from chosen site')
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
    # python weatherapp.py -sitename rp5.ua
    # python weatherapp.py -sitename sinoptik.ua
    # python weatherapp.py -temp_hour accuweather.com
    # python weatherapp.py -sitename accuweather.com

    # python weatherapp.py -s accuweather.com
    # python weatherapp.py --save rp5.ua
