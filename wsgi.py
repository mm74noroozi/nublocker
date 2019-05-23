from flask import Flask, session, redirect, url_for, escape, request
import requests as rq
from bs4 import BeautifulSoup as bs
application = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
main="<form method='post'>url<input type=text name=search><input type=submit value=GO></form>"

@app.route('/',methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		str=request.form['search']
		if str[:4] != 'http':
			str='https://'+str
		r=rq.get(str)
		response=bs(r.text,'html.parser')
		for img in response.select("[src]"):
			if img['src'][:4]== 'http':
				img['src']='/files?q='+img['src']
			else:
				img['src']='/files?q='+r.url+img['src'][1:]
		for link in response.select("[href]"):
			if link['href'][:4]== 'http':
				link['href']='/files?q='+link['href']
			else:
				link['href']='/files?q='+r.url+link['href'][1:]
		return main+response.prettify()
	return main

@app.route('/files',methods=['GET','POST'])
def files():
	return rq.get(request.args['q']).content, 200, {'Content-Type': 'application'}
	
if __name__ == '__main__':
    application.run(debug=True)

