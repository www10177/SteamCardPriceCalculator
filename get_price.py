import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
#Url Setup
exchange_url  ='https://www.steamcardexchange.net/index.php?gamepage-appid-{appid}'
appid=550080
ua = UserAgent()
headers = {'User-Agent': ua.random}

#Requests
req = requests.get(exchange_url.format(appid=appid),headers=headers)

#Parse HTML
card_link_list = []

#Get All Card link list fomr steamcardexchange
soup = BeautifulSoup(req.text,'html.parser')
print(len(soup.find_all('div',class_='showcase-element-container card')))
for showcase in soup.find_all('div',class_='showcase-element-container card'):
	for card in showcase.find_all('div',class_='element-button'):
		for a in card.find_all('a'):
			card_link_list.append(a.get('href')

#Get Card Price from steam market
for link in card_link_list:
	marketname = link.split('/')[-1]
	req  = requests.get(link,headers=headers)
	print(marketname)
	r = requests.get(market_url.format(marketname=marketname),headers=headers)
	print(r.text)
