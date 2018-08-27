import os
import sys

import pyrebase

from security import Security

db = None
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

sec = Security(db)

autobans = []