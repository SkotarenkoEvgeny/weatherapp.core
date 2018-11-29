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
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, "html.parser")


def display_data_weather(data_weather):
    '''
    :param data_weather:
    :return: printing processed data
    '''
    site_name, temprege, place, cond = data_weather[0], data_weather[1], data_weather[2], data_weather[3]
    print('The temprege in {} is {}'.format(place, temprege), 'from ', site_name)
    print('The weather is {}'.format(cond), 'from ', site_name)


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

site_data = {'accuweather': accuweather_parser(), 'rp5': rp5_parser(), 'sinoptik': sinoptik_parser()}



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='returt weather information from chosen site')
    parser.add_argument('-sitename', help=str(site_data.keys()), nargs=1, type=str)
    args = parser.parse_args()
    display_data_weather(site_data[args.sitename[0]])
    #python weatherapp.py -sitename rp5
    #python weatherapp.py -sitename sinoptik
    # site = sinoptik_parser(args.sitename[0])
    # display_data_weather(site)