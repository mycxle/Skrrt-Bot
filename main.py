import discord
from discord.ext import commands
from discord.ext.commands import Bot
from globals import Global
from chans import *
import secrets
import sys
import os

bot = Bot(command_prefix=Global.bot_prefix)
extensions = ["admin_commands", "mod_commands", "info_commands", "fun_commands", "member_join", "member_leave", "server_polls", "money_commands"]
chans = [MathChan(), GenChan(), CountChan(), SuggestChan(), MoneyChans()]


@bot.event
async def on_ready():
    print("Bot logged in.")
    await bot.change_presence(game=discord.Game(name="with big goth tiddies"))
    Global.all_emojis = list(bot.get_all_emojis())

#
# @bot.event
# async def on_command_error(error, ctx):
#     print(str(error))
#     if isinstance(error, commands.CheckFailure):
#         await bot.say("CheckFailure Encountered: " + str(error))
#     else:
#         await bot.say("Failure Encountered: " + str(error))


@bot.event
async def on_message(message):
    for c in chans:
        await c.on_message(bot, message)

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
