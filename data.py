import os
import pickle
from datetime import datetime
from tinydb import TinyDB, Query

db = TinyDB("db.json")

def getDbHandle():
    return db


def get_month():
    month = datetime.today().month
    if os.path.exists("month.pickle"):
        month = pickle.load(open("month.pickle", "rb"))
    else:
        pickle.dump(month, open('month.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
    return month


def save_month(month):
    pickle.dump(month, open('month.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
