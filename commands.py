import random
import discord
from datetime import datetime
import time

async def headcount_command(message, client):
    members = message.server.members
    total = 0
    for m in members:
        total += 1
    await client.send_message(message.channel, 'There are ' +str(total) + ' members on this server')

async def bancount_command(message, client):
    lst = await client.get_bans(message.server)
    total = 0;
    print(lst)
    for item in lst:
        total += 1
    await client.send_message(message.channel, 'There are ' +str(total) + ' people banned')

async def evaluation_command(message, client):
    s = message.content[6:]
    try:
        res = eval(s)
        await client.send_message(message.channel, str(res))
    except:
        await client.send_message(message.channel, "please provide valid input..")

async def coin_command(message, client):
    choice = random.randint(1, 2)
    if choice == 1:
        await client.add_reaction(message, '🍆')
    elif choice == 2:
        await client.add_reaction(message, '🍑')

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

async def userinfo_command(message, client):
    user = message.author

    splt = message.content.split()
    if len(splt) >= 2:
        user = message.server.get_member(splt[1][2:-1])

    e = discord.Embed()
    e.set_thumbnail(url=user.avatar_url)

    name = user.nick
    if name is None:
        name = user.name
    e.title=name

    e.add_field(name="Username", value=user.name)
    e.add_field(name="ID", value=user.id)
    e.add_field(name="Status", value=user.status)
    e.add_field(name="Game", value=user.game)

    created = datetime_from_utc_to_local(user.created_at)
    created_str = '{}'.format(created.strftime('%A, %B %d %Y @ %I:%M%p'))

    e.add_field(name="Account Created", value=created_str)

    dt = user.joined_at
    dt_str = '{}'.format(dt.strftime('%A, %B %d %Y @ %I:%M%p'))

    e.add_field(name="Join Date", value=dt_str)

    fst = True
    roles_str = ""
    total_roles = 0
    for r in user.roles:
        if not fst:
            roles_str += str(r) + ", "
            total_roles += 1
        fst = False

    e.add_field(name="Roles [" + str(total_roles) + "]", value=roles_str[:-2])

    e.colour=discord.Color.red()
    msg = await client.send_message(message.channel, embed=e)