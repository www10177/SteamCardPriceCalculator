from get_price import *
from flask import Flask,render_template,request
import sys
import os
from selenium import webdriver
from flask_script import Manager, Server
##Global Variables ##
driver=None
tax_rate = 0.85

##Manager##
def init_var():
	global driver
	driver = load_driver()

class CustomServer(Server):
    def __call__(self, app, *args, **kwargs):
        init_var()
        return Server.__call__(self, app, *args, **kwargs)

app = Flask(__name__)
manager = Manager(app)
manager.add_command('runserver', CustomServer(host='localhost', port=80))

##App##
@app.route('/',methods=['GET'])
def main_page():
	return render_template('home.html')

@app.route('/results',methods=['GET','POST'])
def results():
	appid=request.values['appid']
	price_list = get_price(appid,driver)
	price_list = [i for i in price_list if i['sell_price'] > 0]
	card_avg = cal_avg(price_list)
	gem_price = get_gem_price(driver)
	gem_count = get_gem_count(len(price_list)/2)
	return render_template('result.html',appid=appid, 
		price_list = price_list, card_avg = card_avg, gem_price = gem_price,gem_count=gem_count, tax_rate = tax_rate)




if __name__=='__main__':
	manager.run()