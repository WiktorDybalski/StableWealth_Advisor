import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_div[0].find_all('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    return texts

def real_time_price(stock_code):
    url = 'https://www.google.com/finance/quote/'+ stock_code + ':NASDAQ?hl=pl'
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, 'AHmHk')
    except ConnectionError:
        texts = []
    return texts[0]

print(real_time_price('TSLA'))

CD_project = 'https://www.google.com/finance/quote/CDR:WSE?hl=pl'
PKO = 'https://www.google.com/finance/quote/PKO:WSE?hl=pl'
