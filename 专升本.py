import sys

import requests
from lxml import etree
import pandas as pd
import time

def get_data():
    url =  ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

    response = requests.get(url,headers=headers,timeout=2)
    html =etree.HTML(response.text)
    name = html.xpath('//*[@id="app"]//div[@class="account-settings-info-right white"]//div[@class="ant-descriptions-title"]/div/div/span[1]/text()')
    # '//*[@id="app"]/div/div/div/div/div[2]/div/div[1]/div/div[1]/div/div/span[1]'
    print(name)
    return 0

def work():
    get_data()


if __name__ == '__main__':
    work()