import requests
from bs4 import BeautifulSoup
import time

url = 'http://example.webscraping.com'
country_list = dict()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}


def find_all_countries(country_list, page_url=''):
    response = requests.get(url + page_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    pages_list = soup.find(id='pagination').find_all('a')
    temp = soup.find('section').find_all('a')
    for j in temp:
        if j.text.lstrip() not in country_list.keys() and j.text != 'Next >':
            country_list[j.text.lstrip()] = j['href']
    for i in pages_list:
        if i.text == 'Next >':
            page_url = i['href']
            print('We completed parse page ', i['href'][i['href'].rfind('/') + 1:])
            time.sleep(1)  # The strugle with Response 429
            find_all_countries(country_list, page_url)
    return country_list


country_list = find_all_countries(country_list, page_url='')

print('Zimbabwe' in country_list.keys())
print('Afghanistan' in country_list.keys())

# country_name = Aland Islands
question = input('Input the name of country ')


def country_information(question, country_list):
    print('The information abaut {} is:'.format(question))
    response = requests.get(url + country_list[question], headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find('table')
    temp_parametrs = body.find_all('label')
    for i in temp_parametrs:
        print(body.find(id=i['id']).text, body.find(id=i['id']).next.next.text)


print(country_information(question, country_list))
