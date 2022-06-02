import os
from datetime import datetime
from tinydb import TinyDB, Query

db = TinyDB("db.json")

def getDbHandle():
    return db


def get_month():
    month = datetime.today().month
    if os.path.exists("month"):
        month = open("month").read().strip()
    else:
        open("month","w").write(str(month))
    return month


def save_month(month):
    open("month","w").write(str(month))
