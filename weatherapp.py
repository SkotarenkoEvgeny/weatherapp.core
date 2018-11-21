import requests
from bs4 import BeautifulSoup
import re

# the task 1
# Змерджити гілку m04_ls1 в develop та видалити
# complete

# the task 2
# Створити гілку m04_ls2
# complete

# the task 3
url = 'https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

temprege = soup.find('span', 'large-temp')
place = soup.find('span', 'current-city')
print('The temprege in {} is {}'.format(place.text[:place.text.find(',')], temprege.text), 'from accuweather.com')

# the task # 4
cond = soup.find('span', 'cond')
print('The weather is {}'.format(cond.text), 'from accuweather.com')

# weather from , 'rp5.ua'
url = 'http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B8%D1%94%D0%B2%D1%96'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
body = soup.find(id='FheaderContent')

temprege = body.find(id='ArchTemp').find(class_='t_0')
place = body.find(id='pointNavi')
print('The temprege in {} is {}'.format(place.text[place.text.rfind(' ') - 1:], temprege.text), 'from rp5.ua')

cond = soup.find(id='forecastShort-content').find(class_='second-part').previous

print('The weather is {}'.format(cond.lstrip(' ')), 'from accuweather.com')

# weather from , 'https://sinoptik.ua/'

url = 'https://sinoptik.ua/'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
body = soup.find('body')

temprege = body.find(class_='main loaded', id='bd1').find(class_='temperature').find(class_='min').span.text
place = body.find(class_='isMain').next.next.next.next

print('The temprege in {} is {}'.format(place[3:len(place)-2], temprege), 'from sinoptik.ua')

cond = body.find(class_='main loaded', id='bd1').find(class_='weatherIco')

print('The weather is {}'.format(cond['title'].lower()), 'from sinoptik.ua')