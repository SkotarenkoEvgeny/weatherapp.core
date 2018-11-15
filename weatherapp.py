import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# the task 3
temprege = soup.find('span', 'large-temp')
place = soup.find('span', 'current-city')
print('The temprege in {} is {}'.format(place.text[:place.text.find(',')], temprege.text))

# the task # 4
cond = soup.find('span', 'cond')
print('The weather is {}'.format(cond.text))

# the task # 5
url = 'http://example.webscraping.com/'
response = requests.get(url)
soup1 = BeautifulSoup(response.content, "html.parser")

countries = soup1.find('table').find_all('img')
print('The contries on the first page is:')
for i in countries:
    print(i.next)
