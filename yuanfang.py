#coding:utf-8
import urllib2, urllib
import json
import re

 
APIKEY = '00299dcb49a1e0bf007cd961dce5a23d'
SECRET = '84f8ea75fb69f3c4'
AUTORIZATIONCODE = '81cf274fefa5aaa5'
access_token = '7eb8d10618927cd87c2a731249b77688'
refresh_token = '86756c6517b270e09360452f471752a0'
douban_user_id = '51146110'
DICT = []
data = {'client_id': APIKEY, 'client_secret': SECRET, 'redirect_uri': 'http://icek.com/callback.html', 'grant_type': 'authorization_code', 'code': AUTORIZATIONCODE}
#f = urllib2.urlopen(url = 'https://www.douban.com/service/auth2/token', 
#               data = urllib.urlencode(data)
#               )

req = urllib2.Request(url = 'https://api.douban.com/v2/notifications')
req.add_header('Authorization', 'Bearer ' + access_token)
f = urllib2.urlopen(req)
notifications = f.read()
a = json.loads(notifications)
print a['notifications']
#for i in a['notifications']:
    
hits = [i['target_id'] for i in a['notifications'] \
        if re.search('@zhuxi0511', i['target_title']) is not None]

print hits
def add_comments(comment_ids):
    for i in comment_ids:
        req = urllib2.Request(url = 'https://api.douban.com/shuo/v2/statuses/%s/comments' % i)
        req.add_header('Authorization', 'Bearer ' + access_token)
        data = {'text': '大人真乃神人也'}
        f = urllib2.urlopen(url=req, data=urllib.urlencode(data))
        print f.read()

add_comments(hits)

