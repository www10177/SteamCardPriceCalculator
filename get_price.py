import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
def strip_price(s):
	s = s.strip()
	s= s.strip('NT$')
	return float(s)

def get_price(appid):
	#Url Setup
	exchange_url  ='https://www.steamcardexchange.net/index.php?gamepage-appid-{appid}'
	ua = UserAgent()
	headers = {'User-Agent': ua.random}
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
	for link in card_link_list[:1]:
		marketname = link.split('/')[-1]
		d = {'name':marketname,'link':link}
		req  = requests.get(link+currency_str,headers=headers)
		json = req.json()
		try :
			if json['success'] is not True:
				continue
			html = json['results_html']
		except:
			print('link parse except')
			continue
		soup = BeautifulSoup(html,'html.parser')
		price = soup.find('span',class_='market_listing_price market_listing_price_with_fee')
		d['sell_price_with_fee'] = strip_price(price.get_text())
		price = soup.find('span',class_='market_listing_price market_listing_price_without_fee')
		d['sell_price_without_fee'] = strip_price(price.get_text())
		price_list.append(d)

		#Get 24hr Volume
		#req  = requests.get(link,headers=headers)
		#soup = BeautifulSoup(req.text,'html.parser')
		#for div in soup.find_all('div',class_='es_sold_amount'):
		#	print(div)
	return d 

