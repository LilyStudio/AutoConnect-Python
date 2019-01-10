#!/usr/bin/env python3

import urllib.request
import urllib.parse
import argparse
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
    logInJson = urllib.request.urlopen(url + urllib.parse.urlencode(userinfo)).read().decode('utf-8')
    logInInfo = json.loads(logInJson)

    if logInInfo['reply_code'] == 1:
        print("Log in success")
    else:
        print(logInInfo['reply_msg'])
    return 0


def runKeep(args):
    urlsJson = open('urls.json')
    urls = json.loads(urlsJson.read())
    urlsJson.close()

    user = {'username': args.username, 'password': args.password}

    while True:

        status = checkStatus(urls['checkStatus'], args.username)
        if status == 0:
            print("Correct user")
        elif status == 1:
            print("Logged out")
        elif status == 2:
            print("Wrong user")

        if status == 0:
            pass
        else:
            if status == 2 and args.mode == 'REPLACE':
                print("Replacing...")
                logOut(urls['logOut'])
                time.sleep(3)
                logIn(urls['logIn'], user)
                print("Replace done")

        time.sleep(60)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="为了解决南大弱智网络中心给一间宿舍一个IP造成的舍友异地登陆后的断网问题")
    parser.add_argument('-u', '--username', required=True, help='username')
    parser.add_argument('-p', '--password', required=True, help='password')
    parser.add_argument('-m', '--mode', help='r: replace if wrong user login')
    args = parser.parse_args()
    runKeep(args)
