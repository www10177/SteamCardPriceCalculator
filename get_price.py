import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import browser_cookie3
import steam.webauth as wa
def get_session():
    username = input('Please Enter User Name')
    password = input('Please Enter Password')
    captcha=None
    twofactor=None
    print(username,password)
    while True:
        try:
            user = wa.WebAuth(username,password)
        except (wa.CaptchaRequired, wa.LoginIncorrect) as exp:
            print(exp)
            if isinstance(exp, LoginIncorrect):
                password = input('Please Enter Correct Password')
            if isinstance(exp, wa.CaptchaRequired):
                print('Please Solve Captcha')
                print (user.captcha_url)
            else:
                print('other exceptiion')
                captcha = None
        else:
            break
    while True:
        twofactor =  input('Please Enter TwoFactorCode')
        user.login(twofactor_code= twofactor)
        break
        try:
            user.login(twofactor_code= twofactor)
        except wa.TwoFactorCodeRequired:
            twofactor = input('Please Enter TwoFactorCode')
        except exceptiion as e:
            print(e)
        else:
            print('Login Success')
            break
    return user.session


def strip_price(s):
    s = s.strip()
    s = s.replace(',','')
    s= s.replace('NT$','')
    return float(s)
def get_price(appid,sess):

    #Url Setup
    exchange_url  ='https://www.steamcardexchange.net/index.php?gamepage-appid-{appid}'
    ua = UserAgent()
    headers = {'User-Agent': ua.chrome}
    #Requests
    req = requests.get(exchange_url.format(appid=appid),headers=headers)

    #Parse HTML
    card_link_list = []

    #Get All Card link list fomr steamcardexchange
    soup = BeautifulSoup(req.text,'html.parser')
    for showcase in soup.find_all('div',class_='showcase-element-container card'):
        for card in showcase.find_all('div',class_='element-button'):
            for a in card.find_all('a'):
                card_link_list.append(a.get('href'))

    #Get Card Price from steam market
    currency_str = '/render?start=0&count=10&currency=30&format=json'
    price_list = []
    #print(card_link_list)

    for link in card_link_list:
        marketname = link.split('/')[-1]
        d = {'name':marketname,'link':link}
        print(link+currency_str)
        req  = sess.get(link+currency_str,headers=headers)
        json = req.json()
        if 'Foil' in marketname:
            '''
            d['sell_price_with_fee'] = -1
            d['sell_price_without_fee'] = -1
            price_list.append(d)

            continue
            '''
            pass
        #print(json)
        try :
            html = json['results_html']
            soup = BeautifulSoup(html,'html.parser')
            price = soup.find('span',class_='market_listing_price market_listing_price_with_fee')
            d['sell_price_with_fee'] = strip_price(price.get_text())
            price = soup.find('span',class_='market_listing_price market_listing_price_without_fee')
            d['sell_price_without_fee'] = strip_price(price.get_text())
        except Exception as e:
            print(e)
            print('GET_PRICE:link parse except')
            d['sell_price_with_fee'] = -1
            d['sell_price_without_fee'] = -1
        price_list.append(d)

        #Get 24hr Volume
        #req  = requests.get(link,headers=headers)
        #soup = BeautifulSoup(req.text,'html.parser')
        #for div in soup.find_all('div',class_='es_sold_amount'):
        #   print(div)
    return price_list
def cal_avg(price_list) :
    #Input: price_list from get_price
    #Return:price_tuple(with fee,without fee) (Sum of not foil card only)
    price_list = [i for i in price_list if 'Foil' not in i['name']]
    without_fee,with_fee = 0.0,0.0
    for item in price_list:
        with_fee+= item['sell_price_with_fee']
        without_fee += item['sell_price_without_fee']
    l = len(price_list)
    return without_fee/l

def get_gem_price(sess):
    #Return Gem price(float)
    try :
        ua = UserAgent()
        headers = {'User-Agent': ua.chrome}
        url = r'https://steamcommunity.com/market/listings/753/753-Sack%20of%20Gems/render?start=0&count=10&currency=30&format=json'
        req  = sess.get(url,headers=headers)
        html = req.json()['results_html']
        soup = BeautifulSoup(html,'html.parser')
        price = soup.find('span',class_='market_listing_price market_listing_price_with_fee')
        return strip_price(price.get_text())
    except Exception as e :
        print(e)
        return -1

