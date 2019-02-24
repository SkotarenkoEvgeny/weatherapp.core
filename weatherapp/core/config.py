import os

"""
headers - the user agent for requests sites-data

"""
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/70.0.3538.102 Safari/537.36'}


sites = ['accuweather.com', 'rp5.ua']

DEFAULT_VERBOSE_LEVEL = 0

base_path = os.path.dirname(__file__)
