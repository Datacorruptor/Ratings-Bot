from data import *
from tinydb.operations import add


def addPoints(target, amount):
    db = getDbHandle()

    roles = [i.name for i in target.roles]
    if "Колхоз" in roles:
        User = Query()

        if len(db.search(User.id == target.id))>0 :
            db.update(add('points',amount), User.id == target.id)
            db.update(add('monthly_points', amount), User.id == target.id)
        else:
            db.insert({'id': target.id, 'points': amount, 'monthly_points': amount})

        print(db.all())

        return "Социальные кредиты добавлены\n"
    else:
        return "Человек НЕ находится в колхозе\n"



