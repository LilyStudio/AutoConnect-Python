#!/usr/bin/env python3

import urllib.request
import urllib.parse
import json
import time

def checkStatus(url, username):
	statusJson = urllib.request.urlopen(url).read().decode('utf-8')
	statusInfo = json.loads(statusJson)

	if statusInfo['reply_code'] == 1:
		return 1
	elif statusInfo['reply_code'] == 0:
		if statusInfo['rows'][0]['username'] == username:
			return 0
		else:
			return 2

def logOut(url):
	urllib.request.urlopen(url)
	print("Current wrong user logged out.")

def logIn(url, userinfo):
	# print(url + urllib.parse.urlencode(userinfo))
	logInJson = urllib.request.urlopen(url + urllib.parse.urlencode(userinfo)).read().decode('utf-8')
	logInInfo = json.loads(logInJson)

	if logInInfo['reply_code'] == 1:
		print("Log in success")
	else:
		print(logInInfo['reply_msg'])
	return 0

def runOnce():
	urlsJson = open('urls.json')
	urls = json.loads(urlsJson.read())
	urlsJson.close()
	userJson = open('user.json')
	user = json.loads(userJson.read())
	userJson.close()

	status = checkStatus(urls['checkStatus'], user['username'])
	if status == 0:
		print("Correct user")
	elif status == 1:
		print("Logged out")
	elif status == 2:
		print("Wrong user")

	if status == 0:
		pass
	else:
		if status == 2:
			logOut(urls['logOut'])
			time.sleep(3)
		logIn(urls['logIn'], user)
	
def runKeep():
	urlsJson = open('urls.json')
	urls = json.loads(urlsJson.read())
	urlsJson.close()
	userJson = open('user.json')
	user = json.loads(userJson.read())
	userJson.close()

	while True:

		status = checkStatus(urls['checkStatus'], user['username'])
		if status == 0:
			print("Correct user")
		elif status == 1:
			print("Logged out")
		elif status == 2:
			print("Wrong user")

		if status == 0:
			pass
		else:
			if status == 2:
				logOut(urls['logOut'])
				time.sleep(3)
			logIn(urls['logIn'], user)
		
		time.sleep(60)
	

if __name__ == '__main__':
	runKeep()
