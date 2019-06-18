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

    for item in stores.iterrows():
        doc_ref = db.collection(u'sources').document()
        doc_ref.set({
            u'store_name': item['store_name'],
            u'score': item['score'],
            u'link': item['link'],
            u'min_price': item['min_price'],
            u'max_price': item['max_price'],
            u'close_day': item['close_day'],
            u'lat': item['lat'],
            u'lon': item['lon'],
        })

