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

def addTickets(target, amount):
    db_ticket = getDbTicketHandle()

    User = Query()

    if len(db_ticket.search(User.id == target.id))>0 :
        db_ticket.update(add('tickets',amount), User.id == target.id)
    else:
        db_ticket.insert({'id': target.id, 'tickets': amount})

    print(db_ticket.all())

    return "Талоны на фотографию добавлены\n"



