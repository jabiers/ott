
import requests
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import firestore
from datetime import date, datetime, timedelta

# Initialize the default app
cred = credentials.Certificate("jabiott-firebase-adminsdk-w0rig-5b46a13752.json")
admin = firebase_admin.initialize_app(cred)
print(admin.name)  # "[DEFAULT]"
db = firestore.client()

# ip = requests.get('https://checkip.amazonaws.com').text.strip()
accounts = db.collection(u'netflix').where(u'currentStreaming', u'<=', 4).stream()
account = list(accounts)[0]
print(account.reference.collection("logs").document("111.222.333.444").set({datetime.now().strftime(r'%y%m%d %H:%M:%S'): "abc"}, merge=True))
# print(account.("password"))

# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')