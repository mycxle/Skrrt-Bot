from discord.ext.commands import Bot
import discord
import pyrebase
import security
import helpers
from datetime import datetime
import os
import sys

if len(sys.argv) >= 2 and sys.argv[1] == "l":
    import secrets

db = None
if len(sys.argv) >= 2 and sys.argv[1] == "l":
    db = pyrebase.initialize_app(secrets.FIREBASE_CONFIG).database()
else:
    FIREBASE_CONFIG = {
        "apiKey": os.environ['apiKey'],
        "authDomain": os.environ['authDomain'],
        "databaseURL": os.environ['databaseURL'],
        "storageBucket": os.environ['storageBucket']
    }
    db = pyrebase.initialize_app(FIREBASE_CONFIG).database()

skrrt_bot = Bot(command_prefix=">")
sec = security.Security(db)

autobans = []


def is_admin(id):
    return {
        '167797932156911616': True,
        '408062249324773387': True
    }.get(id, False)


@skrrt_bot.event
async def on_ready():
    print("Bot logged in.")
    await skrrt_bot.change_presence(game=discord.Game(name="with big goth tiddies"))


@skrrt_bot.event
async def on_member_join(member):
    welcome_channel = member.server.get_channel(str(sec.settings["welcome_channel"]))
    rules_channel = member.server.get_channel(str(sec.settings["rules_channel"]))
    logs_channel = member.server.get_channel(str(sec.settings["logs_channel"]))

    member_name = member.name
    newaccounts_age = int(sec.get("newaccounts_age")) * 24
    server_locked = int(sec.get("is_locked_server"))

    if server_locked == 1:
        autobans.append(member.id)
        await skrrt_bot.send_message(logs_channel,
                                     "LOCKED SERVER AUTO-BAN: " + member_name + " | " + str(member.id))
        return await skrrt_bot.ban(member, delete_message_days=1)

    if newaccounts_age > 0:
        created = helpers.datetime_from_utc_to_local(member.created_at)
        current = datetime.now()
        diff = current - created
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        print("Account is " + str(hours) + " old.")
        if hours < newaccounts_age:
            autobans.append(member.id)
            await skrrt_bot.send_message(logs_channel,
                                         "NEW ACCOUNT AUTO-BANNED: " + member_name + " | " + str(member.id) + " | Age: "
                                         + str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s")
            return await skrrt_bot.ban(member, delete_message_days=1)

    print("MEMBER JOINED")
    e = discord.Embed()
    e.set_thumbnail(url=member.avatar_url)
    e.title = "Welcome " + member_name + "!"
    e.description = "Be sure to read " + rules_channel.mention
    e.colour = discord.Color.green()
    e.set_footer(text=str(member.id))
    await skrrt_bot.send_message(welcome_channel, "**>MEMBER JOINED:** " + member.mention, embed=e)


@skrrt_bot.event
async def on_member_remove(member):
    print(autobans)
    if str(member.id) in autobans:
        autobans.remove(str(member.id))
        return

    welcome_channel = member.server.get_channel(str(sec.settings["welcome_channel"]))
    print("MEMBER LEFT")
    e = discord.Embed()
    e.title = "Goodbye " + member.name + "!"
    e.description = "Have a great life!"
    e.colour = discord.Color.red()
    e.set_footer(icon_url=member.avatar_url, text=str(member.id))
    await skrrt_bot.send_message(welcome_channel, "**>MEMBER LEFT:** " + member.mention, embed=e)


@skrrt_bot.event
async def on_message(message):
    if str(message.channel.id) == str(sec.get("counting_channel")):
        secnd = False
        async for m in skrrt_bot.logs_from(message.channel, limit=2):
            if secnd and message.author.id != skrrt_bot.user.id:
                if message.author.id == m.author.id:
                    await skrrt_bot.delete_message(message)
                else:
                    try:
                        if int(message.content) != int(m.content) + 1:
                            await skrrt_bot.delete_message(message)
                    except:
                        await skrrt_bot.delete_message(message)
            secnd = True
    else:
        await skrrt_bot.process_commands(message)


@skrrt_bot.command(pass_context=True)
async def whitelist(ctx):
    if not is_admin(str(ctx.message.author.id)):
        return
    if sec.get("whitelist") == 1:
        sec.set("whitelist", 0)
        await skrrt_bot.say("Whitelist Only: DISABLED")
    else:
        sec.set("whitelist", 1)
        await skrrt_bot.say("Whitelist Only: ENABLED")


@skrrt_bot.command(pass_context=True)
async def set(ctx, *args):
    if not is_admin(str(ctx.message.author.id)):
        return
    if len(args) != 2:
        return await skrrt_bot.say("ERROR: Command takes 2 arguments")
    try:
        sec.set(args[0], int(args[1]))
    except Exception as e:
        await skrrt_bot.say("ERROR: " + str(e))


@skrrt_bot.command(pass_context=True)
async def get(ctx, *args):
    if not is_admin(str(ctx.message.author.id)):
        return
    if len(args) == 0:
        s = ""
        for k in sec.settings:
            s += str(k) + "(" + str(sec.settings[k]) + "), "
        await skrrt_bot.say("ALL VARIABLES: " + s[:-2])
    else:
        try:
            await skrrt_bot.say(sec.get(args[0]))
        except Exception as e:
            await skrrt_bot.say("ERROR: " + str(e))


@skrrt_bot.command(pass_context=True)
async def add(ctx, *args):
    if not is_admin(str(ctx.message.author.id)):
        return
    if len(args) < 2:
        return await skrrt_bot.say("ERROR: Command takes 2 arguments")
    try:
        new_args = list(args[1:])
        sec.add(args[0], ' '.join(new_args))
    except Exception as e:
        await skrrt_bot.say("ERROR: " + str(e))


@skrrt_bot.command(pass_context=True)
async def remove(ctx, *args):
    if not is_admin(str(ctx.message.author.id)):
        return
    if len(args) < 2:
        return await skrrt_bot.say("ERROR: Command takes 2 arguments")
    try:
        sec.remove(args[0], args[1])
    except Exception as e:
        await skrrt_bot.say("ERROR: " + str(e))


async def lock_unlock_channels(ctx, val):
    unlck = None
    if val == 1:
        unlck = False

    sec.set("is_locked_channels", val)
    everyone_overwrite = discord.PermissionOverwrite(send_messages=unlck)
    everyone_role = None
    for r in ctx.message.server.roles:
        if r.is_everyone:
            everyone_role = r
    for c in sec.settings["channels_list"]:
        channel = ctx.message.server.get_channel(c)
        if channel in ctx.message.server.channels:
            await skrrt_bot.edit_channel_permissions(channel, everyone_role, everyone_overwrite)


@skrrt_bot.command(pass_context=True)
async def lock(ctx, *args):
    if not is_admin(str(ctx.message.author.id)):
        return
    if len(args) > 0:
        if args[0] == "s":
            if sec.get("is_locked_server") == 1:
                return await skrrt_bot.say("SERVER IS ALREADY LOCKED!")
            sec.set("is_locked_server", 1)
            await skrrt_bot.say("SERVER IS LOCKED!")
        elif args[0] == "c":
            if sec.get("is_locked_channels") == 1:
                return await skrrt_bot.say("CHANNELS ARE ALREADY LOCKED!")
            await lock_unlock_channels(ctx, 1)
            await skrrt_bot.say("CHANNELS ARE LOCKED!")
        else:
            await skrrt_bot.say("ERROR: Invalid argument")
    else:
        if sec.get("is_locked_server") == 1 and sec.get("is_locked_channels") == 1:
            return await skrrt_bot.say("WE ARE ALREADY FULLY LOCKED!")
        sec.set("is_locked_server", 1)
        await lock_unlock_channels(ctx, 1)
        await skrrt_bot.say("WE ARE NOW FULLY LOCKED!")


@skrrt_bot.command(pass_context=True)
async def unlock(ctx, *args):
    if not is_admin(str(ctx.message.author.id)):
        return
    if len(args) > 0:
        if args[0] == "s":
            if sec.get("is_locked_server") == 0:
                return await skrrt_bot.say("SERVER IS ALREADY UNLOCKED!")
            sec.set("is_locked_server", 0)
            await skrrt_bot.say("SERVER IS UNLOCKED!")
        elif args[0] == "c":
            if sec.get("is_locked_channels") == 0:
                return await skrrt_bot.say("CHANNELS ARE ALREADY UNLOCKED!")
            await lock_unlock_channels(ctx, 0)
            await skrrt_bot.say("CHANNELS ARE UNLOCKED!")
        else:
            await skrrt_bot.say("ERROR: Invalid argument")
    else:
        if sec.get("is_locked_server") == 0 and sec.get("is_locked_channels") == 0:
            return await skrrt_bot.say("WE ARE ALREADY FULLY UNLOCKED!")
        sec.set("is_locked_server", 0)
        await lock_unlock_channels(ctx, 0)
        await skrrt_bot.say("WE ARE NOW FULL UNLOCKED!")


@skrrt_bot.command(pass_context=True)
async def headcount(ctx, *args):
    if not is_admin(str(ctx.message.author.id)):
        return
    print("headcount")
    members = ctx.message.server.members
    total = 0
    for m in members:
        total += 1
    await skrrt_bot.say('There are ' + str(total) + ' members on this server')


@skrrt_bot.command(pass_context=True)
async def bancount(ctx, *args):
    if not is_admin(str(ctx.message.author.id)):
        return
    lst = await skrrt_bot.get_bans(ctx.message.server)
    total = 0;
    print(lst)
    for item in lst:
        total += 1
    await skrrt_bot.say('There are ' + str(total) + ' people banned')


@skrrt_bot.command(pass_context=True)
async def goon(ctx, *args):
    if not is_admin(str(ctx.message.author.id)):
        return
    try:
        goon_role = discord.utils.get(ctx.message.server.roles, id="474056561707450370")
        m = None
        try:
            m = ctx.message.mentions[0]
        except:
            if len(args) > 0:
                try:
                    user_id = int(args[0])
                    m = discord.utils.get(ctx.message.server.members, id=str(user_id))
                except Exception as e:
                    await skrrt_bot.say("EXCEPTION: " + str(e))
            else:
                await skrrt_bot.say("Please provide a user...")
                return

        if goon_role in m.roles:
            await skrrt_bot.remove_roles(m, goon_role)
            await skrrt_bot.say(str(m.name + " is no longer a goon!"))
        else:
            await skrrt_bot.add_roles(m, goon_role)
            await skrrt_bot.say(str(m.name + " is now a goon!"))
    except Exception as e:
        await skrrt_bot.say("EXCEPTION: " + str(e))


@skrrt_bot.command(pass_context=True)
async def everyone(ctx, *args):
    e = discord.utils.get(ctx.message.server.roles, id="428709693540794395")
    await skrrt_bot.delete_message(ctx.message)
    m = await skrrt_bot.say(e.mention)
    if len(args) > 0:
        if args[0] == "g":
            await skrrt_bot.delete_message(m)


token = None
if len(sys.argv) >= 2 and sys.argv[1] == "l":
    token = secrets.BOT_TOKEN
else:
    token = os.environ['BOT_TOKEN']
skrrt_bot.run(token)
