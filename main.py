

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from globals import *

bot = Bot(command_prefix=">")

extensions = ["admin_commands", "mod_commands", "info_commands", "fun_commands", "member_join", "member_leave", "server_polls"]

@bot.event
async def on_ready():
    print("Bot logged in.")
    await bot.change_presence(game=discord.Game(name="with big goth tiddies"))

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CheckFailure):
        await bot.say("CheckFailure Encountered: " + str(error))
    else:
        await bot.say("Failure Encountered: " + str(error))

@bot.event
async def on_message(message):
    if str(message.channel.id) == str(sec.get("counting_channel")):
        secnd = False
        async for m in bot.logs_from(message.channel, limit=2):
            if secnd and message.author.id != bot.user.id:
                if message.author.id == m.author.id:
                    await bot.delete_message(message)
                else:
                    try:
                        if int(message.content) != int(m.content) + 1:
                            await bot.delete_message(message)
                    except:
                        await bot.delete_message(message)
            secnd = True
    else:
        await bot.process_commands(message)


token = None
if len(sys.argv) >= 2 and sys.argv[1] == "l":
    token = secrets.BOT_TOKEN
else:
    token = os.environ['BOT_TOKEN']

for extension in extensions:
    try:
        bot.load_extension("cogs." + extension)
    except Exception as e:
        exc = '{}: {}'.format(type(e).__name__, e)
        print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(token)
