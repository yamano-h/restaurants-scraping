#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tabelog
import firebase
from pygeocoder import Geocoder
import googlemaps
from bs4 import BeautifulSoup
import requests

# tokyo_ramen_review = tabelog.Tabelog(base_url="https://tabelog.com/rstLst/?utf8=%E2%9C%93&utf8=%E2%9C%93&pal=tokyo&LstPrf=A1308&hfc=0&commit=%E7%B5%9E%E3%82%8A%E8%BE%BC%E3%82%80&lid=&RdoCosTp=1&LstCos=0&LstCosT=3&search_date=2019%2F6%2F18%28%E7%81%AB%29&svd=20190618&svps=2&svt=1900&LstRev=0&commit=%E7%B5%9E%E3%82%8A%E8%BE%BC%E3%82%80&LstSitu=0&LstSmoking=0/",test_mode=True)

# firebase.main(tokyo_ramen_review.df)

# gmaps = googlemaps.Client(key="AIzaSyA8aSK47j-BscE4iwf5M35njmPptVCJtvY")
# address = u'赤坂 らいもん'
# result = gmaps.places(address)
# print(result)

r = requests.get('https://retty.me/restaurant-search/search-result/?free_word_category=%E8%B5%A4%E5%9D%82%20%E3%82%89%E3%81%84%E3%82%82%E3%82%93')
soup = BeautifulSoup(r.content, 'html.parser')
# <a href="https://retty.me/area/PRE13/ARE18/SUB1801/100001429789/" target="_blank" class="image-viewer__link"><ul mode="in-out" class="image-viewer__view"><li><img src="https://ximg.retty.me/crop/s220x220/-/retty/img_repo/l/01/17856959.jpg" alt=""></li><li style="display: none;"><img src="https://ximg.retty.me/crop/s220x220/-/retty/img_repo/l/01/18363840.jpg" alt=""></li><li style="display: none;"><img src="https://ximg.retty.me/crop/s220x220/-/retty/img_repo/l/01/17856962.jpg" alt=""></li></ul> <!----></a>
link = soup.find('section', class_='columns__item--restaurants')
# popularity = popularity_tag.svg
restaurants = link.contents[3].attrs[':restaurants']
tmpLink = restaurants.split('\'url\':\'')[1]
link = tmpLink.split('\',\'lng\'')[0]
print(link)  
# r = requests.get('https://retty.me/area/PRE13/ARE18/SUB1803/100001484708/')

# soup = BeautifulSoup(r.content, 'html.parser')
# # <div :level="3" class="restaurant-summary__popularity-label js-popularity-label" is="popularity-label" name="和食"></div>
# popularity_tag = soup.find('div', class_='restaurant-summary__popularity-label')
# # popularity = popularity_tag.svg
# print(popularity_tag.attrs[':level'])

# <div :restaurants="[{'id':'100001429789','url':'https:\/\/retty.me\/area\/PRE13\/ARE18\/SUB1801\/100001429789\/','lng':'139.7362371650297','lat':'35.67687618758872','isPaid':false,'catchCopy':'','popularity':{'restaurant_id':100001429789,'kimete_popularity_id':1,'name':'\u548c\u98df','level':3},'name':'\u8d64\u5742\u3089\u3044\u3082\u3093','countWannago':'894','images':['https:\/\/ximg.retty.me\/crop\/s220x220\/-\/retty\/img_repo\/l\/01\/17856959.jpg','https:\/\/ximg.retty.me\/crop\/s220x220\/-\/retty\/img_repo\/l\/01\/18363840.jpg','https:\/\/ximg.retty.me\/crop\/s220x220\/-\/retty\/img_repo\/l\/01\/17856962.jpg'],'categoryText':'\u725b\u30bf\u30f3 \/ \u713c\u8089 \/ \u725b\u6599\u7406','subAreaName':'\u8d64\u5742','stationName':'\u6c38\u7530\u753a','stationDistance':70,'stationDistanceMinute':1,'locationText':'\u6c38\u7530\u753a\u99c5 \u5f92\u6b691\u5206\uff0870m\uff09','budgetLunch':'\uff5e2000\u5186','budgetDinner':'\u55b6\u696d\u6642\u9593\u5916','holiday':'\u4e0d\u5b9a\u4f11\n','isTopUserReport':true,'reportTopUserCategory':'','reportUserIconURL':'https:\/\/graph.facebook.com\/1310790982\/picture?type=square\u0026width=40\u0026height=40','reportScoreType':'1','reportCreatedAt':'2019\u5e7403\u670810\u65e5','reportText':'\u91d1\u7adc\u5c71\u306e\u5a18\u3055\u3093\u592b\u5a66\u304c\u3084\u3089\u308c\u3066\u3044\u308b\u300c\u8d64\u5742\u3089\u3044\u3082\u3093\u300d\u306e\u30c7\u30a3\u30ca\u30fc\u306b\u884c\u3063\u3066\u53c2\u308a\u307e\u3057\u305f\u3002\n\u30ac\u30b9\u7db2\u713c\u304d\u3067\u81ea\u5206\u9054\u3067\u713c\u3044\u3066\u9802\u304f\u30b9\u30bf\u30a4\u30eb\u3067\u3059\u306e\u3067\u3001\u713c\u304d\u30b9\u30da\u30b7\u30e3\u30ea\u30b9\u30c8\u304c\u3044\u306a\u3044\u3068\u307e\u305a\u3044\u304b\u3082^ ^\n\n\u5206\u539a\u3044\u30bf\u30f3\u3001\u60da\u308c\u60da\u308c\u3059\u308b\u3088\u3046\u2026','reportUserName':'Miki Imai'}]" is="restaurant-list" no-image-src="/images/pancake/no-image.svg" registration-url="">\n<ul class="filter filter--placeholder"><li></li><li></li><li></li></ul>\n<ul class="search-result__restaurants restaurants restaurants--placeholder">\n<li class="restaurants__item">\n<section class="restaurant restaurant--placeholder">\n<div class="restaurant__header restaurant__header--placeholder"></div>\n<div class="restaurant__content">\n<div class="restaurant__images restaurant__images--placeholder"></div>\n<div class="restaurant__detail restaurant__detail--placeholder">\n<div class="information-list information-list--placeholder"></div>\n<div class="actions actions--placeholder"></div>\n</div>\n</div>\n</section>\n</li>\n<li class="restaurants__item">\n<section class="restaurant restaurant--placeholder">\n<div class="restaurant__header restaurant__header--placeholder"></div>\n<div class="restaurant__content">\n<div class="restaurant__images restaurant__images--placeholder"></div>\n<div class="restaurant__detail restaurant__detail--placeholder">\n<div class="information-list information-list--placeholder"></div>\n<div class="actions actions--placeholder"></div>\n</div>\n</div>\n</section>\n</li>\n</ul>\n</div>