#coding:utf-8
from datetime import datetime
import urllib2, urllib
import json
import re
import time
import variable

APIKEY = '00299dcb49a1e0bf007cd961dce5a23d'
SECRET = '84f8ea75fb69f3c4'
AUTORIZATIONCODE = '81cf274fefa5aaa5'
access_token = '7eb8d10618927cd87c2a731249b77688'
refresh_token = '86756c6517b270e09360452f471752a0'
douban_user_id = '51146110'
DICT = []
TIMEFORMAT = '%Y-%m-%d %H:%M:%S'

#data = {'client_id': APIKEY, 'client_secret': SECRET, 'redirect_uri': 'http://icek.com/callback.html', 'grant_type': 'authorization_code', 'code': AUTORIZATIONCODE}
#f = urllib2.urlopen(url = 'https://www.douban.com/service/auth2/token', 
#               data = urllib.urlencode(data)
#               )

def make_author_requeset(url):
    author_req = urllib2.Request(url)
    author_req.add_header('Authorization', 'Bearer ' + access_token)
    return author_req


def yuan_fang_say(status_id, uid):
    req = make_author_requeset('https://api.douban.com/shuo/v2/statuses/%s/comments' % status_id)
    if urllib2.urlopen(url=req, data=urllib.urlencode({'text': '@%s %s' % (str(uid), '大人真乃神人也')})):
        print('Success say to %s' % uid)


def check_status(status_id, status_title, status_time):
    if re.search('@zhuxi0511', status_title) is not None and status_time > variable.check_time:
        variable.tmp_time = status_time
        req = make_author_requeset('https://api.douban.com/shuo/v2/statuses/%s' % status_id)
        json_status = json.loads(urllib2.urlopen(req).read())
        if json_status['user']['uid']:
            yuan_fang_say(status_id, json_status['user']['uid'])

def check_reply(status_id):
    req = make_author_requeset('https://api.douban.com/shuo/v2/statuses/%s/comments' % status_id)
    json_reply = json.loads(urllib2.urlopen(req).read())
    for reply in json_reply:
        reply_time = datetime.strptime(reply['created_at'], TIMEFORMAT)
        if re.search('@zhuxi0511', reply['text']) is not None and reply_time > variable.check_time:
            variable.tmp_time = reply_time
            if reply['user']['uid']:
                yuan_fang_say(status_id, reply['user']['uid'])

def check_notifications(comment_ids):
    for status_id, status_title, status_time in comment_ids:
        check_status(status_id, status_title, status_time)
        check_reply(status_id)

while True:
    author_req = make_author_requeset('https://api.douban.com/v2/notifications')
    f = urllib2.urlopen(author_req)
    notifications = f.read()
    json_notification = json.loads(notifications)
    #print json_notification
        
    hits = [(i['target_id'], i['target_title'], datetime.strptime(i['time'], TIMEFORMAT)) \
            for i in json_notification['notifications'] if i['cate'] == 'notification']

    check_notifications(hits)
    variable.check_time = variable.tmp_time
    print variable.check_time
    time.sleep(30)

if __name__ == '__main__':
    main()
