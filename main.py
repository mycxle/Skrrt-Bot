import re

from helpers import *
from admin_commands import *
from commands import *
from custom_channels import *

client = discord.Client()

prefix = "-"
game = "with big goth tiddies"

admin_commands = {
    "say": say_command,
    "kick": kick_command,
    "warn": warn_command,
    "ban": ban_command,
    "softban": softban_command,
    "unban": unban_command,
    "unbanall": unbanall_command,
    "member": member_command,
    "normie": normie_command,
    "game": game_command,
    "purge": purge_command,
    "mute": mute_command,
    "unmute": unmute_command,
    "mutelist": mutelist_command,
    "wipe": wipe_command
}

commands = {
    "headcount": headcount_command,
    "bancount": bancount_command,
    "eval": evaluation_command,
    "coin": coin_command,
    "userinfo": userinfo_command
}

custom_channels = {
    "392158484176830464": hi_channel,
    "392461625640222720": lol_channel,
    "392803097296240642": rip_channel,
    "419025423461253120": counting_channel
}

async def call_command(message, commandDictionary):
    cmd = message.content.split()[0][1:]
    if cmd in commandDictionary:
        await commandDictionary[cmd](message, client)

async def call_custom_channel(message):
    if message.channel.id in custom_channels:
        await custom_channels[message.channel.id](message, client)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name=game))

@client.event
async def on_message(message):
    await call_custom_channel(message)

    if message.author.top_role.id == "380618184379727883":
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
        if len(urls) > 0:
            await client.delete_message(message)
            msg = await client.send_message(message.channel, message.author.mention + ' Sorry but normies aren\'t allowed to post links..')
            await asyncio.sleep(3)
            await client.delete_message(msg)

    if message.content.lower().startswith(prefix):
        await call_command(message, commands)
        if is_admin(message.author.id):
            await call_command(message, admin_commands)

@client.event
async def on_member_join(member):
    print("MEMBER JOINED")
    # lst = member.server.roles
    # for l in lst:
    #     if l.id == "380618184379727883":
    #         await client.add_roles(member, l)
    e = discord.Embed()
    e.set_thumbnail(url=member.avatar_url)
    e.title="Welcome to Skrrt Gang!"
    e.description=member.mention + " Remember to have a look at " + member.server.get_channel("428692044568068096").mention +"!"
    e.colour=discord.Color.red()
    message = await client.send_message(member.server.get_channel("355493390378336267"), embed=e)
    for x in client.get_all_emojis():
        print(x.name + " | " + x.id)
        if x.id == "418597486324875275":
            await client.add_reaction(message, x)

    await client.add_reaction(message, "🇭")
    await client.add_reaction(message, "🇮")

    for x in client.get_all_emojis():
        print(x.name + " | " + x.id)
        if x.id == "418792186386186250":
            await client.add_reaction(message, x)

with open("token.txt") as f:
    token = f.readline()
client.run(token)