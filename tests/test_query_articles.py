from news_madlibs import MadlibGame
import requests, json
from unittest import mock

url = (f'https://newsdata.io/api/1/news')

def test_connection_to_endpoint():
    response = requests.get(url)
    assert response.status_code == 401