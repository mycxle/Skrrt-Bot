import discord
import random

toe_punishment = ["https://cdn.discordapp.com/attachments/414956681362014228/414964856031019008/Screenshot_20180119-160311.jpg",
                  "https://cdn.discordapp.com/attachments/414956681362014228/414966414387052544/IMG_20180216_154625.jpg",
                  "https://cdn.discordapp.com/attachments/414956681362014228/414995340987727882/DLPULmnW0AA7X6C.jpg"]
toe_warn = ["https://cdn.discordapp.com/attachments/414956681362014228/414999379238191105/C6h-NWYW0AAV19n.jpg",
            "https://cdn.discordapp.com/attachments/414956681362014228/415004875181522944/DFCygLbXoAA1DNT.jpg",
            "https://cdn.discordapp.com/attachments/414956681362014228/414993011747979264/DPiGSHzWsAIGnvM.jpg"]

async def say_command(message, client):
    channel = message.content.split()[1]
    args = message.content.split()
    count = 0
    strng = ""
    for a in args:
        if count >= 2:
            strng = strng + a + " "
        count += 1
    await client.send_message(message.server.get_channel(channel), strng)

def create_embed(pic_list, title, desc, color):
    e = discord.Embed()
    e.set_image(url=random.choice(pic_list))
    e.title=title
    e.description=desc
    e.colour=color
    return e

async def kick_command(message, client):
    user = message.content.split()[1][2:-1]
    await client.kick(message.server.get_member(user))
    msg = await client.send_message(message.channel,embed=create_embed(toe_punishment,"SO LONG FUCK NIGGA!", "Kicked <@"+ user + ">!", discord.Color.red()))
    for x in client.get_all_emojis():
        print(x.name + " | " + x.id)
        if x.id == "402604191635472384":
            await client.add_reaction(msg, x)
    await client.add_reaction(msg, "🇷")
    await client.add_reaction(msg, "🇮")
    await client.add_reaction(msg, "🇵")
    for x in client.get_all_emojis():
        print(x.name + " | " + x.id)
        if x.id == "402604192092651532":
            await client.add_reaction(msg, x)

async def warn_command(message, client):
    user = message.content.split()[1][2:-1]
    args = message.content.split()
    count = 0
    strng = ""
    for a in args:
        if count >= 2:
            strng = strng + a + " "
        count += 1
    msg = await client.send_message(message.channel, embed=create_embed(toe_warn,"BETTER STOP THAT FUCK SHIT!", "Warning: " + "<@" + user + ">!\nReason: " + strng, discord.Color.red()))
    await client.add_reaction(msg, "😡")
    await client.add_reaction(msg, "🇳")
    await client.add_reaction(msg, "🇴")
    for x in client.get_all_emojis():
        print(x.name + " | " + x.id)
        if x.id == "402606578383060995":
            await client.add_reaction(msg, x)

async def ban_command(message, client, days=7):
    user = message.content.split()[1]
    if message.content.split()[1].startswith("<"):
        user = user[2:-1]
    print(user)
    Fakemember=discord.Object(id=user)
    Fakemember.server= message.server

    await client.ban(Fakemember, delete_message_days=days)
    msg = await client.send_message(message.channel, embed=create_embed(toe_punishment,"SO LONG FUCK NIGGA!", "Banned <@"+ user + ">!", discord.Color.red()))
    for x in client.get_all_emojis():
        print(x.name + " | " + x.id)
        if x.id == "402604191635472384":
            await client.add_reaction(msg, x)
    await client.add_reaction(msg, "🇷")
    await client.add_reaction(msg, "🇮")
    await client.add_reaction(msg, "🇵")
    for x in client.get_all_emojis():
        print(x.name + " | " + x.id)
        if x.id == "402604192092651532":
            await client.add_reaction(msg, x)

async def softban_command(message, client):
    await ban_command(message, client, days=0)

async def unban_command(message, client):
    user = message.content.split()[1]
    if user.startswith("<"):
        user = user[2:-1]
    lst = await client.get_bans(message.server)
    print(lst)
    for item in lst:
        if item.id == user:
            await client.unban(message.server, item)
            break

async def unbanall_command(message, client):
    await client.send_message(message.channel, 'This command is currently disabled.')
    return
    msg = await client.send_message(message.channel, 'Unbanning all users...')
    lst = await client.get_bans(message.server)
    total = 0;
    print(lst)
    for item in lst:
        total += 1
    lst = await client.get_bans(message.server)
    count = 0;
    for item in lst:
        await client.unban(message.server, item)
        count += 1
        await client.edit_message(msg, 'Unbanning all users... [{}/{}]'.format(count, total))
    await client.edit_message(msg, 'Successfully unbanned all {} users!'.format(total))

async def member_command(message, client):
    user = message.content.split()[1][2:-1]
    lst = message.server.roles
    for l in lst:
        if l.id == "378983979228856348":
            await client.add_roles(message.server.get_member(user), l)

async def normie_command(message, client):
    user = message.content.split()[1][2:-1]
    lst = message.server.roles
    for l in lst:
        if l.id == "380618184379727883":
            await client.replace_roles(message.server.get_member(user), l)

async def game_command(message, client):
    game = message.content[6:]
    await client.change_presence(game=discord.Game(name=game))

async def purge_command(message, client):
    num = int(message.content.split()[1])
    deleted = await client.purge_from(message.channel, limit=num, before=message)
    await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))

async def mute_command(message, client):
    user = message.content.split()[1][2:-1]
    lst = message.server.roles
    for l in lst:
        print(l.name + " | " + l.id)
        if l.id == "421403738301923328":
            await client.add_roles(message.server.get_member(user), l)
            await client.send_message(message.channel, "User has been muted!")
            break

async def unmute_command(message, client):
    user = message.content.split()[1][2:-1]
    lst = message.server.roles
    for l in lst:
        print(l.name + " | " + l.id)
        if l.id == "421403738301923328":
            await client.remove_roles(message.server.get_member(user), l)
            await client.send_message(message.channel, "User has been unmuted!")
            break

async def mutelist_command(message, client):
    members = message.server.members
    member_list_str = ""
    total = 0
    for m in members:
        for r in m.roles:
            if r.id == "421403738301923328":
                member_list_str += m.name + "#" +m.discriminator + ", "
                total += 1
                break
    if total == 0:
        await client.send_message(message.channel, "Currently there are no users muted!")
    else:
        await client.send_message(message.channel, "Currently muted: " + member_list_str[:-2])

wipe_user = ""
def is_me(m):
    print(str(m.author) + " | " + wipe_user)
    return m.author.id == wipe_user
async def wipe_command(message, client):
    user = message.content.split()[1]
    if message.content.split()[1].startswith("<"):
        user = user[2:-1]
    global wipe_user
    wipe_user = user
    deleted = await client.purge_from(message.channel, limit=int(message.content.split()[2]), before=message, check=is_me)
    await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))