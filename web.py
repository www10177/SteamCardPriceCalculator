from get_price import *
from flask import Flask,render_template,request

app =Flask(__name__)

@app.route('/',methods=['GET'])
def home():
	return render_template('home.html')

@app.route('/results',methods=['GET','POST'])
def results():
	appid=request.values['appid']
	price_list = get_price(appid)
	print(price_list)
	card_avg = '{:.02f}'.format(cal_avg(price_list))
	gem_price = '{:.02f}'.format(get_gem_price())
	return render_template('result.html',appid=appid, 
		price_list = price_list, card_avg = card_avg, gem_price = gem_price)




if __name__=='__main__':
	app.run()
