from requests import get
from bs4 import BeautifulSoup


class Data:
    def __init__(self, ticker):
        self._ticker = ticker
        self._url = f'https://statusinvest.com.br/acoes/{self._ticker}'
    def get_indicators(self):
        html = get(self._url).text
        soup = BeautifulSoup(html, 'html.parser')
        html_table = soup.select("div.width-auto:nth-child(2)")[0]
        indicators = html_table.find_all('h3')
        valuations = html_table.find_all('strong')
        keys, values  = [], []
        for index in range(len(valuations)):
            keys.append(indicators[index].text)
            value = valuations[index].text
            if '%' in value:
                value = value[:-1]
            try:
                value = value.replace(',', '.')
                value = float(value)
            except ValueError:
                value = valuations[index].text
            values.append(value)
        fundamental_indicators = dict(zip(keys, values))
        return fundamental_indicators
if __name__ == "__main__":
    '''request = get('https://statusinvest.com.br/acoes/cvcb3').text

    soup = BeautifulSoup(request, 'html.parser')
    print(soup.select("div.width-auto:nth-child(2)"))'''
    cvc = Data(ticker='cvcb3')
    print(cvc.get_indicators())

