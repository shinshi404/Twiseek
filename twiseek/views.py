from django.shortcuts import render
from django.http.response import HttpResponse
from requests_oauthlib import OAuth1Session
import json
import logging
from twiseek import tw_config

retweet_list = { '0': '0', '1': '10', '2': '10', '3': '100', '4': '1000'}
favo_list    = { '0': '0', '1': '10', '2': '10', '3': '100', '4': '1000'}
disp_list   = { '0': 5, '1': 10, '2': 20}
lang_list   = { '1': 'ja', '2': 'en', '3': 'de', '4': 'zh'}

def index(request):
  return render(request, 'twiseek/index.html')

def search(request):
  # 検索用文字列
  search_word = request.POST.get('search_word')
  retweet_str = " min_retweets:" + retweet_list[request.POST.get('retweet')]
  favo_str    = " min_faves:"    + favo_list[request.POST.get('favo')]
  lang_str    = " lang:" + lang_list[request.POST.get('lang')] if request.POST.get('lang') != '0' else ''
  search_word += retweet_str + favo_str + lang_str
  print('timeline')

  disp_count = disp_list[request.POST.get('disp')]
  twitter = verify() # APIキーを格納したオブジェクトを取得
  url = "https://api.twitter.com/1.1/search/tweets.json" #  検索用エンドポイントURL
  params = {'q' : search_word, 'count' : disp_count}
  # リクエスト
  req = twitter.get(url, params = params)

  data = {}
  print(req.status_code)
  if req.status_code == 200:
    timeline = json.loads(req.text)
    data['timeline'] = timeline['statuses']
    print('timeline')
    print(timeline)


#url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
#  
#  params ={'count' : 5}
#  req = twitter.get(url, params = params)
#  if req.status_code == 200:
#    timeline = json.loads(req.text)
#    data['timeline'] = timeline
#    for tweet in timeline:
#      print(tweet['user']['name']+'::'+tweet['text'])
#      print(tweet['created_at'])
#      print('----------------------------------------------------')
#  else:
#    print("ERROR: %d" % req.status_code)
#
  return render(request, 'twiseek/index.html', data)

def verify():
  CK  = tw_config.get_consumer_key() #(API key)
  CS  = tw_config.get_consumer_secret() #(API secret key)
  AT  = tw_config.get_access_token() #(Access token)
  ATS = tw_config.get_access_token_secret() #(Access token secret)
  return OAuth1Session(CK, CS, AT, ATS)
