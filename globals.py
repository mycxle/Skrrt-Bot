import os
import sys
import pyrebase

from security import Security
from money import Money
from shop import Shop

class Global:
    autobans = []
    collectable = None
    all_emojis = []
    maths = dict()
    db = None
    bot_prefix = ">"

    if len(sys.argv) >= 2 and sys.argv[1] == "l":
        import secrets
        db = pyrebase.initialize_app(secrets.FIREBASE_CONFIG).database()
    else:
        FIREBASE_CONFIG = {
            "apiKey": os.environ['apiKey'],
            "authDomain": os.environ['authDomain'],
            "databaseURL": os.environ['databaseURL'],
            "storageBucket": os.environ['storageBucket']
        }
        db = pyrebase.initialize_app(FIREBASE_CONFIG).database()

    security = Security(db)
    money = Money(db)
    shop = Shop(db)