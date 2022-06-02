from operator import itemgetter

from data import *
from logger import *
from utils import *
from roller import *


async def timer_gsecondyCheck(client):
    db = getDbHandle()

    for guild in client.guilds:

        kolhoz = [member for member in guild.members if
                  "Колхоз" in [i.name for i in member.roles] and member.voice != None]

        kolhoz_sobr = [member for member in kolhoz if member.voice.channel.name == "🌾 Общее собрание"]

        kolhoz = [member for member in guild.members if "Колхоз" in [i.name for i in member.roles]]

        for member in kolhoz_sobr:

            User = Query()

            if len(db.search(User.id == member.id)) == 0:
                db.insert({'id': member.id, 'points': 0, 'monthly_points': 0})

            print(member.nick)
            print(member.name)
            user = db.search(User.id == member.id)[0]
            try:
                if member.nick == None:
                    if len(member.name)<=24:
                        await member.edit(nick=str(int(user['points'])).zfill(4) + " || " + member.name)
                    else:
                        await member.edit(nick=str(int(user['points'])).zfill(4) + " || change nick (too long)")
                else:
                    if member.nick.__contains__("||"):
                        if len(member.nick) <= 24:
                            await member.edit(
                                nick=str(int(user['points'])).zfill(4) + " || " + member.nick.split(" || ")[1])
                        else:
                            await member.edit(nick=str(int(user['points'])).zfill(4) + " || change nick (too long)")
                    else:
                        if len(member.nick) <= 24:
                            await member.edit(nick=str(int(user['points'])).zfill(4) + " || " + member.nick)
                        else:
                            await member.edit(nick=str(int(user['points'])).zfill(4) + " || change nick (too long)")
            except:
                await member.edit(nick=str(int(user['points'])).zfill(4) + " || change nick")

        for member in kolhoz:

            if member in kolhoz and member not in kolhoz_sobr:
                try:
                    if member.nick == None:
                        pass
                    else:
                        if member.nick.__contains__("||"):
                            await member.edit(nick=member.nick.split(" || ")[1])
                except:
                    await member.edit(nick="change nick")


async def timer_activityCheck(client):
    for guild in client.guilds:

        kolhoz = [member for member in guild.members if
                  "Колхоз" in [i.name for i in member.roles] and member.voice != None]
        kolhoz = [member for member in kolhoz if member.voice.afk == False and member.voice.self_mute == False and member.voice.self_deaf == False]

        for member in kolhoz:
            addPoints(member, 0.25)
            log("SYSTEM#0000 added 0.25 point to " + str(member) + " for activity")


async def timer_monthlyCheck(client):
    print("monthcheck")
    db = getDbHandle()
    month = get_month()
    print("month",month)
    curmonth = datetime.today().month
    print("curmonth", curmonth)
    if int(curmonth) != int(month) :

        for guild in client.guilds:
            month = curmonth
            save_month(month)

            kolhoz = [member for member in guild.members if 'Ветеран труда' in [i.name for i in member.roles]]
            for member in kolhoz:
                await remove_veteran(guild, member)

            try:
                max_monthly_users = reversed(sorted(db.all(), key=itemgetter('monthly_points')))
                max_monthly_points = list(max_monthly_users)[0]["monthly_points"]

                Users = Query()
                users_with_max = db.search(Users.monthly_points>=max_monthly_points)

                for user in users_with_max:
                    member = guild.get_member(user['id'])
                    await grant_veteran(guild, member)

            except Exception:
                print("Никто не получил Ветерана труда")

            db.update({'monthly_points': 0})


async def timer_hourlyCheck(client):
    db = getDbHandle()

    for guild in client.guilds:

        for user in db.all():

            exists_somethere = False
            for guild in client.guilds:
                if guild.get_member(user['id'])!=None:
                    exists_somethere = True

            member = guild.get_member(user['id'])

            if member is None:
                if not exists_somethere:
                    User = Query()
                    db.remove(User.id == user['id'])
                continue

            if user['points'] < 250:
                await clear_rank(guild, member)
            elif user['points'] < 500:
                await update_rank(0, guild, member)
            elif user['points'] < 1000:
                await update_rank(1, guild, member)
            elif user['points'] < 2000:
                await update_rank(2, guild, member)
            else:
                await update_rank(3, guild, member)

            if "Колхоз" not in [i.name for i in member.roles]:
                await clear_rank(guild, member)
                User = Query()
                db.remove(User.id == user['id'])