from requests import get
from bs4 import BeautifulSoup


class Data:
    def __init__(self, ticker):
        self._ticker = ticker
        self._url = f'https://statusinvest.com.br/acoes/{self._ticker}'
    def get_indicators(self):
        html = get(self._url).text
        soup = BeautifulSoup(html, 'html.parser')
        html_table = soup.select("div.width-auto:nth-child(2)")
        return

if __name__ == "__main__":
    '''request = get('https://statusinvest.com.br/acoes/cvcb3').text

    soup = BeautifulSoup(request, 'html.parser')
    print(soup.select("div.width-auto:nth-child(2)"))'''
    cvc = Data(ticker='cvcb3')
    print(cvc.get_indicators())

