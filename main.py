#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tabelog
import firebase
from pygeocoder import Geocoder
import googlemaps
from bs4 import BeautifulSoup
import requests

tokyo_ramen_review = tabelog.Tabelog(base_url="https://tabelog.com/tokyo/A1308/rstLst/",test_mode=False)
print(tokyo_ramen_review.df)
firebase.main(tokyo_ramen_review.df)

