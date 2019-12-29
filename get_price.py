from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import re
from urllib.parse import unquote
import requests
def load_driver():
    options = webdriver.ChromeOptions()
    options.add_extension('./extensions/Better-Buy-Orders_v1.6.2.crx')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://store.steampowered.com/login/?redir=&redir_ssl=1')
    input('ENTER to continue')

    return driver

def get_price_tuple(link,driver):
    driver.get(link)
    select = Select(driver.find_element_by_id('currency_buyorder'))
    select.select_by_value('30')
    sell_ele = driver.find_element_by_id('market_commodity_forsale')
    buy_ele = driver.find_element_by_id('market_commodity_buyrequests')
    while True:
        if 'NT' in buy_ele.text:
            break
    print(sell_ele.text)
    print(buy_ele.text)
    reg = r'(\d*).*NT\$ (\d*.\d*) .*'
    sell_re = re.search(reg,sell_ele.text).groups()
    buy_re = re.search(reg,buy_ele.text).groups()
    return (sell_re,buy_re)







def get_price(appid,driver):
    #Url Setup
    exchange_url  ='https://www.steamcardexchange.net/index.php?gamepage-appid-{appid}'

    #Requests
    req=requests.get(exchange_url.format(appid=appid))

    #Parse HTML
    card_link_list = []

    #Get All Card link list fomr steamcardexchange
    soup = BeautifulSoup(req.text,'html.parser')
    for showcase in soup.find_all('div',class_='showcase-element-container card'):
        for card in showcase.find_all('div',class_='element-button'):
            for a in card.find_all('a'):
                card_link_list.append(a.get('href'))

    #Get Card Price from steam market
    price_list = []
    #print(card_link_list)

    for link in card_link_list:
        marketname = unquote(link.split('/')[-1])
        d = {'name':marketname,'link':link}
        if 'Foil' in marketname:
            d['sell_price'] = -99
            d['sell_vol'] = -99
            d['buy_price']=-99
            d['buy_vol']=-99
        else:
            price_tuple = get_price_tuple(link,driver)
            d['sell_vol'] = int(price_tuple[0][0])
            d['sell_price'] = float(price_tuple[0][1])
            d['buy_vol']=int(price_tuple[1][0])
            d['buy_price']=float(price_tuple[1][1])
        price_list.append(d)
    return price_list
def cal_avg(price_list) :
    #Input: price_list from get_price
    #Return:price_tuple(with fee,without fee) (Sum of not foil card only)
    price_list = [i for i in price_list if i['sell_price'] > 0]
    sell_price,buy_price = 0.0,0.0
    for item in price_list:
        sell_price+= item['buy_price']
        buy_price += item['sell_price']
    l = len(price_list)
    return sell_price/l

def get_gem_price(driver):
    #Return Gem price(float)
    url = r'https://steamcommunity.com/market/listings/753/753-Sack%20of%20Gems'
    price_t = get_price_tuple(url,driver)
    return float(price_t[0][1])
def get_gem_count(length):
    # card_len : gem_count
    table = {13:462,10:600,9:667, 8:750,7:857,6:1000,5:1200}
    try : 
        return table[length]
    except exception as e:
        print(e)
        return 100000000



