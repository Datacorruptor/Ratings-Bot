from github import Github
import discord
from discord.ext import commands, tasks
import os


TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents=intents)
GT = os.environ["GITHUB_TOKEN"]
github = Github(GT)
repository = github.get_user().get_repo('Rating-Bot-Data')
print("Getting all files from github")
for fl in os.listdir():

    if not fl.endswith(".py") and not fl == '__pycache__' and not fl.startswith("."):
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


@tasks.loop(seconds=1.0)
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

        if not fl.endswith(".py") and not fl == '__pycache__' and not fl.startswith("."):
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


@client.command(name='addCredits', help='adds credits to member of "Kolkhoz"')
async def addPointsCommand(ctx, id: int, amount: int, reason):
    await command_addPoints(ctx, id, amount, reason)

@client.command(name='makeBackup')
async def addPointsCommand(ctx):
    if ctx.message.author.id == 547124518519308303:
        await ctx.send("Backup started")
        print("Backing up all of the files!")
        for fl in os.listdir():

            if not fl.endswith(".py") and not fl == '__pycache__' and not fl.startswith("."):
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
