import requests
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options
from time import sleep
import pandas as pd

url = 'https://statusinvest.com.br/acoes/cvcb3'

option = Options()
option.headless = True
browser = webdriver.Firefox()
browser.get(url)
sleep(5)

while (True):
    try:
        # Select the frequency
        browser.find_element_by_xpath('/html/body/main/div[4]/div/div/div[2]/header/div[2]/div[1]/a').click()
        browser.find_element_by_xpath("/html/body/main/div[4]/div/div/div[2]/header/div[2]/div[1]/ul/li[2]/a").click()

        # Remove delta H
        browser.find_element_by_xpath("/html/body/main/div[4]/div/div/div[2]/header/div[2]/div[2]/div/input").click()
        browser.find_element_by_xpath("/html/body/main/div[4]/div/div/div[2]/header/div[2]/div[2]/div/ul/li[4]/span").click()
        browser.find_element_by_xpath("/html/body/main/div[4]/div/div/div[2]/header/div[2]/div[3]/div[1]/input").click()

        # Select the historical period
        # need two lines one to remove the click from the DATA (DELTA h) and another to really select the period field
        browser.find_element_by_xpath("/html/body/main/div[4]/div/div/div[2]/header/div[2]/div[3]/div[1]/input").click()
        browser.find_element_by_xpath("/html/body/main/div[4]/div/div/div[2]/header/div[2]/div[3]/div[1]/ul/li[8]/span").click()
        break
    #except ElementClickInterceptedException:
    except:
        browser.quit()
        browser = webdriver.Firefox()
        browser.get(url)
sleep(3)

# Get the html table
browser.find_element_by_xpath("/html/body/main/div[4]/div/div/div[2]/div[2]/button").click()
table = browser.find_element_by_xpath("/html/body/main/div[4]/div/div/div[2]/div[1]/div[1]/table")
table = table.get_attribute('outerHTML')
soup = BeautifulSoup(table, 'html.parser')
table = soup.find('table')

table = pd.read_html(str(table))[0]
cols = tuple(table.columns)
for col in cols:
    if ('H %' in col) or ('V %' in col):
        table = table.drop(col, 1)
print(table)
