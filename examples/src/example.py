import requests


def get_data(url):
    result = requests.get(url)

    return result.json().get('message')
