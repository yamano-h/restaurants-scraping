import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection(u'sources')
docs = users_ref.get()


def main(stores):
            # ['store_id', 'store_name', 'score', 'link', 'price', 'close_day', 'lat', 'lon']

    for index, item in stores.iterrows():
        doc_ref = db.collection(u'sources').document()
        doc_ref.set({
            u'store_name': item['store_name'],
            u'scores': {
                u'tabelog': item['score_tabelog'],
                u'retty': item['score_retty'],
            },
            u'link': {
                u'tabelog': item['link_tabelog'],
                u'retty': item['link_retty'],
            },
            u'min_price': item['min_price'],
            u'max_price': item['max_price'],
            u'close_day': item['close_day'],
            u'lat': item['lat'],
            u'lng': item['lng'],
            u'genre_list': item['genre_list'],
        })

