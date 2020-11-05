import requests
from bs4 import BeautifulSoup as bs
import html2text as h2t

email1='emailexample1@inbox.lv'
email2='emailexample2@inbox.lv'
token_name1 = 'authenticity_token' 						#git twitter
token_name2 = 'authURL' 								#netflix
token_name3 = 'csrfmiddlewaretoken'
email = 'emailexample1@inbox.lv'
twitter = 'https://twitter.com/account/begin_password_reset'
github = 'https://github.com/password_reset'
netflix = 'https://netflix.com/api/shakti/vf5ae854f/login/help'

def getTokenAndCookies(url, token_name):
	r = requests.get(url)
	string = r.text.partition(token_name)[2]
	string = string[9:100]
	cym='"'
	if(string.find(cym)==-1): cym="'"
	token = string[:string.find(cym)]
	return token, r.cookies

def passwordReset(url, token_name, email):
	token, cookies = getTokenAndCookies(url, token_name)
	r = requests.post(url, cookies=cookies, data = {token_name : token, 'email' : email})
	return r.text

def registrationCheck(html):
	soap = bs(html, 'lxml')
	if(soap.text.find('Check your email')!=-1): 
		return True
	else:
		return False