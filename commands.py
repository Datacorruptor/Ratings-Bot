import discord
from data import *
from operator import itemgetter
from logger import *
from utils import *
from CoolNumbers import numberGenerator

async def command_addPoints_channel(ctx, id: int, amount: int, reason):
    if (ctx.message.channel.id != 977674010798219275 and ctx.message.channel.id != 949378986151137300) or ctx.message.channel.name != "сеновал":
        return

    if ctx.message.author.id == 547124518519308303 \
            or ctx.message.author.id == 872855017529417788 \
            or ctx.message.author.id == 643516811635326977 \
            or ctx.message.author.id == 248857776611131392:

        channel = ctx.message.guild.get_channel(id)
        response=""
        member_string = "["
        for member in channel.members:
            res = addPoints(member, amount)
            response += str(member) + " " + res
            if res == "Социальные кредиты добавлены\n":
                member_string+=str(member)+", "
        member_string += "]"
        log_points(ctx.message.author, member_string, amount, reason)

        await ctx.send(response)
    else:
        await ctx.send('У вас нет прав.')

async def command_addPoints(ctx, id: int, amount: int, reason):
    if (ctx.message.channel.id != 977674010798219275 and ctx.message.channel.id != 949378986151137300) or ctx.message.channel.name != "сеновал":
        return

    if ctx.message.author.id == 547124518519308303 \
            or ctx.message.author.id == 872855017529417788 \
            or ctx.message.author.id == 643516811635326977 \
            or ctx.message.author.id == 248857776611131392:

        guild = ctx.message.guild
        target = guild.get_member(id)

        response = str(target)+" "+addPoints(target, amount)

        log_points(ctx.message.author,target,amount,reason)

        await ctx.send(response)
    else:
        await ctx.send('У вас нет прав.')

async def command_addTickets(ctx, id: int, amount: float, reason):
    if (ctx.message.channel.id != 977674010798219275 and ctx.message.channel.id != 949378986151137300) or ctx.message.channel.name != "сеновал":
        return

    if ctx.message.author.id == 547124518519308303 \
            or ctx.message.author.id == 872855017529417788 \
            or ctx.message.author.id == 643516811635326977 \
            or ctx.message.author.id == 248857776611131392:

        guild = ctx.message.guild
        target = guild.get_member(id)

        response = str(target) + " " + addTickets(target, amount)

        log_tickets(ctx.message.author, target, amount, reason)

        await ctx.send(response)
    else:
        await ctx.send('У вас нет прав.')

async def command_getPoints(ctx):

    db = getDbHandle()
    db_ticket = getDbTicketHandle()


    if (ctx.message.channel.name != "сеновал" and ctx.message.channel.name != "feature-test") or (ctx.message.channel.id != 977674010798219275 and ctx.message.channel.id != 949378986151137300 and ctx.message.channel.id != 985162878485139456):
        return

    log_use(ctx.message.author,'getPoints')
    bigShot = False
    User = Query()
    rows = db.search(User.id == ctx.message.author.id)
    if len(rows) > 0:
        row = rows[0]

        if int(row['points']) >= 250:
            bigShot = True
            frames = numberGenerator.getImage(int(row['points']),int(row['monthly_points']),"CoolNumbers")
            frames[0].save(str(int(row['points']))+'.gif', save_all=True, append_images=frames[1:], optimize=False,duration=160, loop=0, transparency=0, disposal=2)
            await ctx.send("Ваши соц.кредиты",file = discord.File(str(int(row['points']))+'.gif'))
            os.remove(str(int(row['points']))+'.gif')

        else:
            await ctx.send("У вас всего " + str(int(row['points'])) + " соц.кредитов. " + "За месяц вы набрали " + str(int(row['monthly_points'])) + " соц.кредитов.")
    else:
        await ctx.send("У вас всего 0 соц.кредитов. За месяц вы набрали 0 соц.кредитов. Вы вообще никто, и вас мы знать не знаем!")

    User = Query()
    rows = db_ticket.search(User.id == ctx.message.author.id)
    if len(rows) > 0:
        row = rows[0]

        if bigShot:
            frames = numberGenerator.getImage(int(row['tickets']),(str(round(float(row['tickets'])-int(row['tickets']),3))[2:]),"CoolNumbers")
            frames[0].save(str(int(row['tickets']))+'.gif', save_all=True, append_images=frames[1:], optimize=False,duration=160, loop=0, transparency=0, disposal=2)
            await ctx.send("Ваши талоны на фотографию ",file = discord.File(str(int(row['tickets']))+'.gif'))
            os.remove(str(int(row['tickets']))+'.gif')

        else:
            await ctx.send("У вас всего " + str(round(float(row['tickets']),3)) + " талонов на фотографию ")
    else:
        await ctx.send("У вас всего нет талонов на фотографию!")


async def command_getRating(ctx):

    db = getDbHandle()

    if (ctx.message.channel.id != 977674010798219275 and ctx.message.channel.id != 949378986151137300) or ctx.message.channel.name != "сеновал":
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

    if (ctx.message.channel.id != 977674010798219275 and ctx.message.channel.id != 949378986151137300) or ctx.message.channel.name != "сеновал":
        return

    log_use(ctx.message.author, 'getMonthlyRating')
    
    response = "МЕСЯЧНЫЙ CОЦИАЛЬНЫЙ РЕЙТИНГ\n"
    guild = ctx.message.guild

    result = reversed(sorted(db.all(), key=itemgetter('monthly_points')))

    for i in result:
        response += str(guild.get_member(i["id"])) + ": " + str(int(i["monthly_points"])) + " соц.кредитов\n"
    await ctx.send(response)

async def command_genImage(ctx,client,promt):

    db_ticket = getDbTicketHandle()
    log_use(ctx.message.author, 'ImageGen')

    TextChannel = None
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.id == 781662768130424836:
                TextChannel = channel

    User = Query()
    rows = db_ticket.search(User.id == ctx.message.author.id)

    status = None
    for guild in client.guilds:
        for member in guild.members:
            if member.id == 1016938991066562650:
                status = member.status

    if str(status) == "online":

        if len(rows) > 0:
            row = rows[0]
            if float(row['tickets']) >= 1:
                addTickets(ctx.message.author,-1)
                await TextChannel.send("start image generation "+promt+" "+str(ctx.message.channel.id))
                await ctx.send("Запрос на фотографию отправлен, как только он будет обработан, результат появится в канале")


            else:
                await ctx.send("У вас всего нет талонов на фотографию!")
        else:
            await ctx.send("У вас всего нет талонов на фотографию!")
    else:
        await ctx.send("В данное время нейросеть не онлайн, обратитесь @Ivan_Smitt#2683")

async def command_transfer(ctx,id,amount):

    if amount<0 or len(str(amount))>5:
        await ctx.send("Ненене, у нас в тестировщиках тоже умные люди сидят")
        return

    db_ticket = getDbTicketHandle()
    log_use(ctx.message.author, 'ticket transfer ' + str(id)+" "+ str(amount))



    User = Query()
    rows = db_ticket.search(User.id == ctx.message.author.id)

    if len(rows) > 0:
        row = rows[0]
        if float(row['tickets']) >= amount:

            guild = ctx.message.guild
            target = guild.get_member(id)

            addTickets(ctx.message.author, -amount)
            addTickets(target, amount)


            await ctx.send(str(target)+" перевод был совершён успешно")


        else:
            await ctx.send("У вас не хватает талонов на фотографию!")
    else:
        await ctx.send("У вас не хватает талонов на фотографию!")


