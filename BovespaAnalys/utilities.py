from requests import get
from bs4 import BeautifulSoup
import pandas as pd

class Data:
    def __init__(self, ticker):
        self._ticker = ticker
        self._url = f'https://statusinvest.com.br/acoes/{self._ticker}'
    def get_all_indicators(self):
        html = get(self._url).text
        soup = BeautifulSoup(html, 'html.parser')
        html_table = soup.select("div.width-auto:nth-child(2)")[0] # select the exactly table with the fundamental indicators
        indicators = [element.text for element in html_table.find_all('h3')]
        valuations = [element.text for element in html_table.find_all('strong')]
        if len(indicators) != len(valuations):
            # the h3 tags show the indicador name on site, however that are some duplicates h3 tags that are not showm in the front end, but exists and
            # refers to the same indicador, to avoid errors, the
            shown = ('P/VP', 'P/L', 'P/Ebitda', 'P/Ebit', 'P/Ativo', 'EV/Ebitda', 'EV/EBIT', 'PSR', 'P/Cap.Giro', 'P/Ativo Circ Liq', 'Margem Bruta',
                     'Margem Ebitda', 'Margem Ebit', 'Margem Líquida', 'Giro Ativos', 'ROE', 'ROA', 'ROIC', 'LPA', 'VPA', 'Dívida Líquida / Patrimônio',
                     'Dívida Líquida / EBITDA', 'Dívida Líquida / EBIT', 'Patrimônio / Ativos', 'Passivos / Ativos', 'Liquidez Corrente', 'CAGR Receitas 5 Anos',
                     'CAGR Lucros 5 Anos')
            indicators = [element for element in indicators if (element in shown) == True]
        for index in range(len(valuations)):
            value = valuations[index]
            if '%' in value:
                value = value[:-1]
            try:
                value = value.replace(',', '.')
                value = float(value)
            except ValueError:
                value = 'Not avaiable'
            valuations[index] = value
        fundamental_indicators = dict(zip(indicators, valuations))
        return fundamental_indicators


class Stock(Data):
    def __repr__(self):
        return f'BrazilianStock object <{self._ticker.upper()}>'
    @property
    def profit_indicators(super):
        indicators = ('ROE', 'ROIC', 'Margem Ebitda', 'Margem Líquida')
        return {key: values for (key, values) in super.get_all_indicators().items() if key in indicators}
    @property
    def price_indicators(self):
        indicators = ('P/VP', 'P/L', 'P/Ativo')
        return {key:values for (key, values) in self.get_all_indicators().items() if key in indicators}
    @property
    def debt_indicators(self):
        indicators = ('Dívida Líquida / Patrimônio', 'Dívida Líquida / EBITDA',  'Passivos / Ativos')
        # there is a pŕoblem with this indicators, because the html source get more h3 tags here, and some
        # indicadors are not the same
        return {key: values for (key, values) in self.get_all_indicators().items() if key in indicators}


class Analyzer:
    def __repr__(self):
      return f'FundamentalAnalyzer obecjt'
    def __init__(self, ticker):
        self._ticker = ticker
        self._points = 0
        self._basic_fundamentals = {
            'price_indicators': {
                'P/VP': 3,
                'P/L': 20,
                'P/Ativo': 2},
            'profit_indicators': {
                'Margem Ebtida': 15,
                'Margem Líquida': 8,
                'ROE': 10,
                'ROIC': 5},
            'debt_indicadors': {
                'Dívida Líq/Patrim': 1,
                'Dívida Líq/EBITDA': 3,
                'Passivos / Ativos': 1}}

    def analyze_metrics(self, indicators):
        chosen_metrics = ('ROE', 'ROIC', 'Margem Ebitda', 'Margem Líquida', 'P/VP', 'P/L', 'P/Ativo',
                          'Dívida Líquida / Patrimônio', 'Dívida Líquida / EBITDA',  'Passivos / Ativos')
        indicators = {key: indicators[key] for key in chosen_metrics}
        metrics_df = pd.DataFrame.from_dict(indicators, orient='index', columns=["Current Value"])
        for column in ("Min", "Max", "Weigh", " +Points", "-Points"):
            metrics_df[column] = pd.Series()
        '''metrics_df.loc['ROE', 'Min'] = 10
        metrics_df.loc['ROIC', 'Min'] = 5
        metrics_df.loc['Margem Ebitda', 'Min'] = 15
        metrics_df.loc['Margem Líquida', 'Min'] = 8
        metrics_df.loc['P/VP', 'Min'] = 0.8
        metrics_df.loc['P/L', 'Min'] = 3
        metrics_df.loc['P/Ativo', 'Min'] = 0,6
        metrics_df.loc['ROE', 'Max'] = 100
        metrics_df.loc['ROIC']['Max'] = 80
        metrics_df.loc['Margem Líquida']
        print(metrics_df.loc[['ROE'], ['Current Value', "Max"]])'''
        #metrics_df.loc[['ROE'], ['Min', 'Max']] = 10, 100
        print(metrics_df)


if __name__ == "__main__":
    # Testing area
    '''request = get('https://statusinvest.com.br/acoes/cvcb3').text
    soup = BeautifulSoup(request, 'html.parser')
    print(soup.select("div.width-auto:nth-child(2)"))
    petr = Data(ticker='petr4')
    cvc = Data('cvcb3')
    print(cvc.get_all_indicators())
    print(cvc.get_all_indicators())
    print(petr.profit_indicators)
    clas = Stock('cvcb3')
    print(clas.get_all_indicators())
    print(clas.price_indicators, '\n', clas.profit_indicators, '\n', clas.debt_indicators)'''
    ana = Analyzer('cvcb3')
    stock = Stock('cvcb3')
    ana.analyze_metrics(stock.get_all_indicators())