#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

class Tabelog:
    """
    食べログスクレイピングクラス
    test_mode=Trueで動作させると、最初のページの３店舗のデータのみを取得できる
    """
    def __init__(self, base_url, test_mode=False, begin_page=1, end_page=30):

        # 変数宣言
        self.store_id = ''
        self.store_id_num = 0
        self.store_name = ''
        self.score_tabelog = 0
        self.score_retty = 0
        self.link_tabelog = ''
        self.link_retty = ''
        self.min_price = 0
        self.max_price = 0
        self.close_day = ''
        self.lat = ''
        self.lng = ''
        self.genre_list = ''
        self.columns = ['store_id', 'store_name', 'score_tabelog', 'score_retty', 'link_tabelog', 'link_retty', 'min_price', 'max_price', 'close_day', 'lat', 'lng', 'genre_list']
        self.df = pd.DataFrame(columns=self.columns)
        self.__regexcomp = re.compile(r'\n|\s') # \nは改行、\sは空白

        page_num = begin_page # 店舗一覧ページ番号

        if test_mode:
            list_url = base_url + str(page_num) +  '/?Srt=D&SrtT=rt&sort_mode=1' #食べログの点数ランキングでソートする際に必要な処理
            self.scrape_list(list_url, mode=test_mode)
        else:
            while True:
                list_url = base_url + str(page_num) +  '/?Srt=D&SrtT=rt&sort_mode=1' #食べログの点数ランキングでソートする際に必要な処理
                if self.scrape_list(list_url, mode=test_mode) != True:
                    break

                # INパラメータまでのページ数データを取得する
                if page_num >= end_page:
                    break
                page_num += 1
        return

    def scrape_list(self, list_url, mode):
        """
        店舗一覧ページのパーシング
        """
        r = requests.get(list_url)
        if r.status_code != requests.codes.ok:
            return False

        soup = BeautifulSoup(r.content, 'html.parser')
        soup_a_list = soup.find_all('a', class_='list-rst__rst-name-target') # 店名一覧

        if len(soup_a_list) == 0:
            return False

        if mode:
            for soup_a in soup_a_list[:2]:
                item_url = soup_a.get('href') # 店の個別ページURLを取得
                self.store_id_num += 1
                self.scrape_item(item_url, mode)
        else:
            for soup_a in soup_a_list:
                item_url = soup_a.get('href') # 店の個別ページURLを取得
                self.store_id_num += 1
                self.scrape_item(item_url, mode)

        return True

    def scrape_item(self, item_url, mode):
        """
        個別店舗情報ページのパーシング
        """
        start = time.time()

        # 食べログ店舗URL保存
        self.link_tabelog = item_url

        r = requests.get(item_url)
        if r.status_code != requests.codes.ok:
            print(f'error:not found{ item_url }')
            return

        soup = BeautifulSoup(r.content, 'html.parser')

        # 店舗名称取得
        # <h2 class="display-name">
        #     <span>
        #         麺匠　竹虎 新宿店
        #     </span>
        # </h2>
        store_name_tag = soup.find('h2', class_='display-name')
        store_name = store_name_tag.span.string
        print('{}→店名：{}'.format(self.store_id_num, store_name.strip()), end='')
        self.store_name = store_name.strip()

        # 評価点数取得
        #<b class="c-rating__val rdheader-rating__score-val" rel="v:rating">
        #    <span class="rdheader-rating__score-val-dtl">3.58</span>
        #</b>
        rating_score_tag = soup.find('b', class_='c-rating__val')
        rating_score = rating_score_tag.span.string
        self.score_tabelog = float(rating_score)


        # 価格帯の取得
        # <p class="rdheader-budget__icon rdheader-budget__icon--lunch">
        #     <i>昼の予算</i>
        #     <span class="rdheader-budget__price">
        #     <a href="https://tabelog.com/tokyo/A1308/A130801/13160987/dtlratings/#price-range" class="rdheader-budget__price-target">￥1,000～￥1,999</a>
        #     </span>
        # </p>
        lunch_price_tag = soup.find('p', class_='rdheader-budget__icon--lunch')
        lunch_price = lunch_price_tag.a.string
        print('ランチ価格：{}'.format(lunch_price), end='')
        lunch_price_list = re.split('[～￥]', lunch_price) # ['a', 'b', 'c', 'd', 'e']と出力される

  
        if (lunch_price_list[1] == ''):
            self.min_price = 0
            self.max_price = int(lunch_price_list[2].replace(',',''))
        else:
            self.min_price = int(lunch_price_list[1].replace(',',''))
            self.max_price = int(lunch_price_list[3].replace(',',''))

        # 定休日の取得
        # <dd id="short-comment" class="rdheader-subinfo__closed-text">
        #     不定休                  
        # </dd>
        close_day_tag = soup.find('dd', class_='rdheader-subinfo__closed-text')
        close_day = close_day_tag.string
        print('定休日：{}'.format(close_day), end='')
        self.close_day = close_day.replace(' ','')

        # 住所の取得
        # <p class="rstinfo-table__address"><span><a href="/tokyo/" class="listlink">東京都</a></span><span><a href="/tokyo/C13103/rstLst/" class="listlink">港区</a><a href="/tokyo/C13103/C36141/rstLst/" class="listlink">赤坂</a>2-6-24</span> <span>1F</span></p>
        address_tag = soup.find('p', class_='rstinfo-table__address')
        address = address_tag.text
        
        # 緯度経度の取得
        url = 'http://www.geocoding.jp/api/'
        payload = {'q': address}
        r = requests.get(url, params=payload)
        ret = BeautifulSoup(r.content,'lxml')
        if ret.find('error'):
            raise ValueError(f"Invalid address submitted. {address}")
        else:
            lat = float(ret.find('lat').string)
            lng = float(ret.find('lng').string)
            self.lat = lat
            self.lng = lng
            print('　緯度{}'.format(lat), end='')
            print('　経度{}'.format(lng), end='')

        # ジャンルの取得
        # <dl class="rdheader-subinfo__item">
        #     <dt class="rdheader-subinfo__item-title">ジャンル：</dt>
        #     <dd class="rdheader-subinfo__item-text">        
        #         <div class="linktree" onmouseover="this.className='linktree is-selected';" onmouseout="this.className='linktree';">
        #         <div class="linktree__parent">
        #             <a href="https://tabelog.com/rstLst/cake/" class="linktree__parent-target">
        #             <span class="linktree__parent-target-text">ケーキ</span>
        #             </a>
        #         </div>
        #         <div class="linktree__childbox">
        #             <div class="c-balloon c-balloon--top linktree__childbaloon">
        #             <ul class="linktree__childlist"><li class="linktree__childlist-item"><a href="https://tabelog.com/tokyo/A1318/A131811/rstLst/cake/">ケーキ×代々木上原・東北沢</a></li><li class="linktree__childlist-item"><a href="https://tabelog.com/tokyo/A1318/rstLst/cake/">ケーキ×京王・小田急沿線</a></li><li class="linktree__childlist-item"><a href="https://tabelog.com/tokyo/rstLst/cake/">ケーキ×東京</a></li>
        #             </ul>
        #             </div>
        #         </div>
        #         </div>
        #         <div class="linktree" onmouseover="this.className='linktree is-selected';" onmouseout="this.className='linktree';">
        #         <div class="linktree__parent">
        #             <a href="https://tabelog.com/rstLst/CC010101/" class="linktree__parent-target">
        #             <span class="linktree__parent-target-text">カフェ</span>
        #             </a>
        #         </div>
        #         <div class="linktree__childbox">
        #             <div class="c-balloon c-balloon--top linktree__childbaloon">
        #             <ul class="linktree__childlist"><li class="linktree__childlist-item"><a href="https://tabelog.com/tokyo/A1318/A131811/rstLst/CC010101/">カフェ×代々木上原・東北沢</a></li><li class="linktree__childlist-item"><a href="https://tabelog.com/tokyo/A1318/rstLst/CC010101/">カフェ×京王・小田急沿線</a></li><li class="linktree__childlist-item"><a href="https://tabelog.com/tokyo/rstLst/CC010101/">カフェ×東京</a></li>
        #             </ul>
        #             </div>
        #         </div>
        #         </div>
        #         <div class="linktree" onmouseover="this.className='linktree is-selected';" onmouseout="this.className='linktree';">
        #         <div class="linktree__parent">
        #             <a href="https://tabelog.com/rstLst/SC0101/" class="linktree__parent-target">
        #             <span class="linktree__parent-target-text">パン</span>
        #             </a>
        #         </div>
        #         <div class="linktree__childbox">
        #             <div class="c-balloon c-balloon--top linktree__childbaloon">
        #             <ul class="linktree__childlist"><li class="linktree__childlist-item"><a href="https://tabelog.com/tokyo/A1318/A131811/rstLst/SC0101/">パン×代々木上原・東北沢</a></li><li class="linktree__childlist-item"><a href="https://tabelog.com/tokyo/A1318/rstLst/SC0101/">パン×京王・小田急沿線</a></li><li class="linktree__childlist-item"><a href="https://tabelog.com/tokyo/rstLst/SC0101/">パン×東京</a></li>
        #             </ul>
        #             </div>
        #         </div>
        #         </div>
        #     </dd>
        # </dl>
        
        genre_tagArea = soup.findAll('dl', class_='rdheader-subinfo__item')[1]
        genre_tagList = genre_tagArea.findAll('span', class_='linktree__parent-target-text')
        genre_list = []
        for genre_tag in genre_tagList:
            genre = genre_tag.string
            genre_list.append(genre)
        print('ジャンル：{}'.format(genre_list), end='')
        self.genre_list = genre_list

        # Rettyの評価取得
        r = requests.get('https://retty.me/restaurant-search/search-result/?free_word_category=' + self.store_name)
        soup = BeautifulSoup(r.content, 'html.parser')
        # <a href="https://retty.me/area/PRE13/ARE18/SUB1801/100001429789/" target="_blank" class="image-viewer__link"><ul mode="in-out" class="image-viewer__view"><li><img src="https://ximg.retty.me/crop/s220x220/-/retty/img_repo/l/01/17856959.jpg" alt=""></li><li style="display: none;"><img src="https://ximg.retty.me/crop/s220x220/-/retty/img_repo/l/01/18363840.jpg" alt=""></li><li style="display: none;"><img src="https://ximg.retty.me/crop/s220x220/-/retty/img_repo/l/01/17856962.jpg" alt=""></li></ul> <!----></a>
        link = soup.find('section', class_='columns__item--restaurants')
        # popularity = popularity_tag.svg

        try:
            restaurants = link.contents[3].attrs[':restaurants']
            tmpLink = restaurants.split('\'url\':\'')[1]
            tmpLink2 = tmpLink.split('\',\'lng\'')[0]
            link = tmpLink2.replace('\\', '')
            # rettyリンク格納
            self.link_retty = link
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'html.parser')
            # <div :level="3" class="restaurant-summary__popularity-label js-popularity-label" is="popularity-label" name="和食"></div>
            popularity_tag = soup.find('div', class_='restaurant-summary__popularity-label')
            popularity = popularity_tag.attrs[':level']
            # retty上にデータがあれば格納
            self.score_retty = float(popularity)
        except:
            # retty上にデータがなければ0を格納
            self.score_retty = 0

        self.make_df()
        return

    def make_df(self):
        self.store_id = str(self.store_id_num).zfill(8) #0パディング
        # ['store_id', 'store_name', 'score', 'link', 'price', 'close_day', 'lat', 'lng', 'genre_list]
        se = pd.Series([self.store_id, self.store_name, self.score_tabelog, self.score_retty, self.link_tabelog, self.link_retty, self.min_price , self.max_price , self.close_day, self.lat , self.lng, self.genre_list], self.columns) # 行を作成
        self.df = self.df.append(se, self.columns) # データフレームに行を追加
        return

