#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tabelog
import firebase
from pygeocoder import Geocoder
import googlemaps
from bs4 import BeautifulSoup
import requests

tokyo_ramen_review = tabelog.Tabelog(base_url="https://tabelog.com/rstLst/?utf8=%E2%9C%93&utf8=%E2%9C%93&pal=tokyo&LstPrf=A1308&hfc=0&commit=%E7%B5%9E%E3%82%8A%E8%BE%BC%E3%82%80&lid=&RdoCosTp=1&LstCos=0&LstCosT=3&search_date=2019%2F6%2F18%28%E7%81%AB%29&svd=20190618&svps=2&svt=1900&LstRev=0&commit=%E7%B5%9E%E3%82%8A%E8%BE%BC%E3%82%80&LstSitu=0&LstSmoking=0/",test_mode=True)
print(tokyo_ramen_review.df)
firebase.main(tokyo_ramen_review.df)