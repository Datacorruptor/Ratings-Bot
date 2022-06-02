from github import Github
import discord
from discord.ext import commands, tasks

import data
from commands import *
from timers import *
from events import *

TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents=intents)
GT = os.environ["GITHUB_TOKEN"]
github = Github(GT)
repository = github.get_user().get_repo('Rating-Bot-Data')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    for guild in client.guilds:

        await create_roles(guild)

    channel = client.get_channel(977674010798219275)  # channel id here
    await channel.send("Дядя Вова в здании!")

    activityCheck.start()
    secondyCheck.start()
    monthlyCheck.start()
    hourlyCheck.start()


@tasks.loop(seconds=1.0)
async def secondyCheck():
    await timer_gsecondyCheck(client)
    pass


@tasks.loop(seconds=300.0)
async def activityCheck():
    await timer_activityCheck(client)
    pass


@tasks.loop(seconds=60.0)
async def monthlyCheck():
    await timer_monthlyCheck(client)
    pass


@tasks.loop(seconds=30.0)
async def hourlyCheck():
    await timer_hourlyCheck(client)
    pass

@tasks.loop(seconds=60.0)
async def backupCheck():
    print("Backing up all of the files!")
    for fl in os.listdir():

        if not fl.endswith(".py"):
            content = open(fl).read()
            try:
                file = repository.get_contents(fl)
                repository.update_file(file.path, "NEW update", content, file.sha)
            except Exception:
                repository.create_file(fl, "NEW file", content)


@client.event
async def on_member_join(member):
    await event_on_member_join(member)


@client.command(name='addCredits', help='adds credits to member of "Kolkhoz"')
async def addPointsCommand(ctx, id: int, amount: int, reason):
    await command_addPoints(ctx, id, amount, reason)


@client.command(name='c', help='get your credits')
async def getPointsCommand(ctx):
    await command_getPoints(ctx)


@client.command(name='r', help='get total rating')
async def getRatingCommand(ctx):
    await command_getRating(ctx)


@client.command(name='mr', help='get monthly rating')
async def getMonthlyRatingCommand(ctx):
    await command_getMonthlyRating(ctx)


print("Getting all files from github")
for fl in os.listdir():
    if not fl.endswith(".py"):
        try:
            file = repository.get_contents(fl)
            open(fl,'wb').write(file.decoded_content)
        except Exception:
            pass
client.run(TOKEN)
