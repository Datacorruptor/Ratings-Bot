from data import *
from operator import itemgetter
from logger import *
from utils import *


async def command_addPoints(ctx, id: int, amount: int, reason):
    if ctx.message.channel.name != "сеновал" and (ctx.message.channel.id == 977674010798219275 or ctx.message.channel.id == 949378986151137300):
        return

    if ctx.message.author.id == 547124518519308303 \
            or ctx.message.author.id == 872855017529417788 \
            or ctx.message.author.id == 643516811635326977 \
            or ctx.message.author.id == 248857776611131392:

        guild = ctx.message.guild
        target = guild.get_member(id)

        response = addPoints(target, amount)

        log_points(ctx.message.author,target,amount,reason)

        await ctx.send(response)
    else:
        await ctx.send('У вас нет прав.')

async def command_getPoints(ctx):

    db = getDbHandle()

    if ctx.message.channel.name != "сеновал":
        return

    log_use(ctx.message.author,'getPoints')

    User = Query()
    rows = db.search(User.id == ctx.message.author.id)
    if len(rows) > 0:
        row = rows[0]
        await ctx.send("У вас всего " + str(int(row['points'])) + " соц.кредитов. " +
                       "За месяц вы набрали " + str(int(row['monthly_points'])) + " соц.кредитов.")
    else:
        await ctx.send("У вас всего 0 соц.кредитов. За месяц вы набрали 0 соц.кредитов. Вы вообще никто, и вас мы знать не знаем!")

async def command_getRating(ctx):

    db = getDbHandle()

    if ctx.message.channel.name != "сеновал":
        return

    log_use(ctx.message.author, 'getRating')


    response = "ОБЩИЙ CОЦИАЛЬНЫЙ РЕЙТИНГ\n"
    guild = ctx.message.guild

    result = reversed(sorted(db.all(), key=itemgetter('points')))

    for i in result:
        response += str(guild.get_member(i["id"])) + ": " + str(int(i["points"])) + " соц.кредитов\n"
    await ctx.send(response)

async def command_getMonthlyRating(ctx):

    db = getDbHandle()

    if ctx.message.channel.name != "сеновал":
        return

    log_use(ctx.message.author, 'getMonthlyRating')
    
    response = "МЕСЯЧНЫЙ CОЦИАЛЬНЫЙ РЕЙТИНГ\n"
    guild = ctx.message.guild

    result = reversed(sorted(db.all(), key=itemgetter('monthly_points')))

    for i in result:
        response += str(guild.get_member(i["id"])) + ": " + str(int(i["monthly_points"])) + " соц.кредитов\n"
    await ctx.send(response)