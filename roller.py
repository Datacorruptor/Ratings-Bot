import discord

async def create_roles(guild):
    if discord.utils.get(guild.roles, name='Ветеран труда') is None:
        await guild.create_role(name="Ветеран труда", color=0xBA9203)

    if discord.utils.get(guild.roles, name='Член правления') is None:
        await guild.create_role(name="Член правления", color=0xDAB707)

    if discord.utils.get(guild.roles, name='Бригадир') is None:
        await guild.create_role(name="Бригадир", color=0xF4D01A)

    if discord.utils.get(guild.roles, name='Заведующий фермы') is None:
        await guild.create_role(name="Заведующий фермы", color=0xADE515)

    if discord.utils.get(guild.roles, name='Старший колхозник') is None:
        await guild.create_role(name="Старший колхозник", color=0x66F529)

async def remove_veteran(guild,member):
    role = discord.utils.get(guild.roles, name='Ветеран труда')
    await member.create_dm()
    await member.dm_channel.send("Ваш статус Ветерана труда окончил свое действие по истечении месяца")
    await member.remove_roles(role)

async def grant_veteran(guild,member):
    role = discord.utils.get(guild.roles, name='Ветеран труда')
    await member.create_dm()
    await member.dm_channel.send(
        "Поздравляем!\nЗа ваши выдающиеся достижения и за заслуги перед отечеством вы награждаетесь почётным званием Ветерана труда!")
    await member.add_roles(role)

def get_all_ranks(guild):
    role1 = discord.utils.get(guild.roles, name='Старший колхозник')
    role2 = discord.utils.get(guild.roles, name='Заведующий фермы')
    role3 = discord.utils.get(guild.roles, name='Бригадир')
    role4 = discord.utils.get(guild.roles, name='Член правления')

    return role1,role2,role3,role4


async def set_rank(rank_level,guild,member):
    ranks = get_all_ranks(guild)
    await member.add_roles(ranks[rank_level])

async def clear_rank(guild,member):
    ranks = get_all_ranks(guild)
    for rank in ranks:
        await member.remove_roles(rank)

async def update_rank(rank_level,guild,member):
    ranks = get_all_ranks(guild)
    if ranks[rank_level] not in member.roles:
        await clear_rank(guild,member)
        await set_rank(rank_level,guild,member)

