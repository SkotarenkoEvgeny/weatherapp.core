import sys
import requests
import argparse
from bs4 import BeautifulSoup


def site_request(url):
    '''
    :param url:
    :return: page data from url
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
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


def accuweather_parser():
    '''
    :return: site_name, temprege, place, cond from accuweather
    '''
    site_name = 'accuweather.com'
    url = 'https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505'
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
            sum(raw_temprege_data)/len(raw_temprege_data)]


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


site_data = {'accuweather': accuweather_parser, 'rp5': rp5_parser, 'sinoptik': sinoptik_parser}
temprege_per_hour = {'accuweather': accuweather_temperege_per_hour}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='returt weather information from chosen site')
    parser.add_argument('-sitename', help=str(site_data.keys()), nargs=1, type=str)
    parser.add_argument('-temp_hour', help='Temprege per hour', nargs=1, type=str)
    args = parser.parse_args()
    if args.sitename != None:
        display_data_weather(site_data[args.sitename[0]]())
    if args.temp_hour != None:
        display_temperege_data_per_hour(temprege_per_hour[args.temp_hour[0]]())

    # python weatherapp.py -sitename rp5
    # python weatherapp.py -sitename sinoptik
    # python weatherapp.py -temp_hour accuweather
