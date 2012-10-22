#!/usr/bin/python
# -*- coding: utf-8 -*-

from token import API_KEY, API_SECRET, REDIRECT_URL, USER_NAME, USER_PASSWORD
#from douban_client import DoubanClient
from datetime import datetime
import urllib2, urllib
import json
import re
import time
import variable
from consts import roll

API_HOST = 'https://www.douban.com'
API_HOST = 'https://api.douban.com'
AUTH_HOST = 'https://www.douban.com'
TOKEN_URL = AUTH_HOST + '/service/auth2/token'
AUTHORIZE_URL = AUTH_HOST + '/service/auth2/auth'

#client = DoubanClient(API_KEY, API_SECRET)

def get_access_token():
    values = {'client_id': API_KEY, 'client_secret': API_SECRET, 'grant_type': 'password', 'username': USER_NAME, 'password': USER_PASSWORD}
    data = urllib.urlencode(values)
    req = urllib2.Request(TOKEN_URL, data)
    res = urllib2.urlopen(req)
    res_data = json.loads(res.read())
    return res_data['access_token'], res_data['douban_user_id'], res_data['expires_in'], res_data['refresh_token']

ACCESS_TOKEN, UID, EXPIR, REFRESH_TOKEN = get_access_token()
print ACCESS_TOKEN
#client.auth_with_code(ACCESS_TOKEN)

#to-do save in database
#def get_followers():
#    followers = client.user.followers(UID)
#    followers_id = [i['id'] for i in followers]
#    return followers_id
#
#def get_following():
#    following = client.user.following(UID)
#    following_id = [i['id'] for i in following]
#    return following_id
#
##TO-DO, save in database
#def follow_people():
#    to_follow = list(set(get_followers()) - set(get_following()))
#
#def get_notification():
    #notification = client.notification.get()
    #print notification

#AUTORIZATIONCODE = '81cf274fefa5aaa5'
#access_token = '7eb8d10618927cd87c2a731249b77688'
#refresh_token = '86756c6517b270e09360452f471752a0'
#douban_user_id = '51146110'
DICT = []
TIMEFORMAT = '%Y-%m-%d %H:%M:%S'

#data = {'client_id': APIKEY, 'client_secret': SECRET, 'redirect_uri': 'http://icek.com/callback.html', 'grant_type': 'authorization_code', 'code': AUTORIZATIONCODE}
#f = urllib2.urlopen(url = 'https://www.douban.com/service/auth2/token', 
#               data = urllib.urlencode(data)
#               )

def make_author_request(url):
    print url
    author_req = urllib2.Request('{0}?apikey={1}'.format(url, API_KEY))
    author_req.add_header('Authorization', 'Bearer ' + ACCESS_TOKEN)
    return author_req

def yuan_fang_say(status_id, uid, message):
    req = make_author_request('https://api.douban.com/shuo/v2/statuses/%s/comments' % status_id)
    reply = roll(message)
    try:
        if urllib2.urlopen(url=req, data=urllib.urlencode({'text': '@%s %s' % (str(uid), str(reply))})):
            print('Success say to %s' % uid)
    except:
        print('failed say to %s' % uid)
    time.sleep(3)


def check_status(status_id):
    req = make_author_request('https://api.douban.com/shuo/v2/statuses/%s' % status_id)
    try:
        status = json.loads(urllib2.urlopen(req).read())
        status_time = datetime.strptime(status['created_at'], TIMEFORMAT)
        if re.search('@yuanfanglee', status['text']) is not None and status_time > variable.check_time:
            variable.tmp_time = status_time
            if status['user']['uid']:
                yuan_fang_say(status_id, status['user']['uid'], status['text'])
    except:
        print 'check status failed'

def check_reply(status_id):
    req = make_author_request('https://api.douban.com/shuo/v2/statuses/%s/comments?count=200' % status_id)
    try:
        json_reply = json.loads(urllib2.urlopen(req).read())
        for reply in json_reply:
            reply_time = datetime.strptime(reply['created_at'], TIMEFORMAT)
            if re.search('@yuanfanglee', reply['text']) is not None and reply_time > variable.check_time:
                variable.tmp_time = reply_time
                if reply['user']['uid']:
                    yuan_fang_say(status_id, reply['user']['uid'], reply['text'])
    except:
        print 'check reply failed'

def check_notifications(comment_ids):
    for status_id in comment_ids:
        check_status(status_id)
        check_reply(status_id)

def main():
    f = open('reply_time.txt')
    tmp_time = f.readline()
    try:
        tmp_time = datetime.strptime(tmp_time, TIMEFORMAT)
    except ValueError, v:
        if len(v.args) > 0 and v.args[0][:26] == 'unconverted data remains: ':
            tmp_time = tmp_time[:-(len(v.args[0])-26)]
            tmp_time = datetime.strptime(tmp_time, TIMEFORMAT)
        else:
            raise v
    variable.check_time = variable.tmp_time = tmp_time
    f.close()
    while True:
        author_req = make_author_request('https://api.douban.com/v2/notifications')
        f = urllib2.urlopen(author_req)
        notifications = f.read()
        json_notification = json.loads(notifications)
        #print json_notification
    
        hits = [i['target_id'] \
                for i in json_notification['notifications'] if i['cate'] == 'notification']
    
        check_notifications(hits)
        variable.check_time = variable.tmp_time
        print variable.check_time
        f = open('reply_time.txt', 'w')
        f.write(variable.check_time.strftime(TIMEFORMAT))
        f.close()
        time.sleep(30)

if __name__ == '__main__':
    main()
