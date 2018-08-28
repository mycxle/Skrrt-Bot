

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random

from timex import *

from globals import *

from datetime import datetime

bot_prefix = ">"
bot = Bot(command_prefix=bot_prefix)

extensions = ["admin_commands", "mod_commands", "info_commands", "fun_commands", "member_join", "member_leave", "server_polls", "money_commands"]
moneycooldowns = []

@bot.event
async def on_ready():
    print("Bot logged in.")
    await bot.change_presence(game=discord.Game(name="with big goth tiddies"))

@bot.event
async def on_command_error(error, ctx):
    print(str(error))
    if isinstance(error, commands.CheckFailure):
        await bot.say("CheckFailure Encountered: " + str(error))
    else:
        await bot.say("Failure Encountered: " + str(error))

def get_money():
    return round(random.uniform(0.1,1), 2)

@asyncio.coroutine
async def remove_money_cooldown(id):
    global moneycooldowns
    moneycooldowns.remove(id)

@bot.event
async def on_message(message):
    global bot_prefix
    if str(message.channel.id) not in sec.get("nomoney_channels"):
        if str(message.author.id) not in moneycooldowns and not str(message.content).startswith(bot_prefix) and message.author.bot is False:
            money = get_money()
            print("Got: " + str(money))
            user_dict = db.child("money").child(str(message.author.id)).get().val()
            if user_dict is None:
                now_time = datetime.now()
                db.child("money").child(str(message.author.id)).set({"balance": str(money), "last_daily": "..."})
            else:
                balance = float(user_dict["balance"])
                balance += money
                last_daily = str(user_dict["last_daily"])
                db.child("money").child(str(message.author.id)).set({"balance": str(round(balance, 2)), "last_daily": str(last_daily)})
            moneycooldowns.append(str(message.author.id))
            Timer(60, remove_money_cooldown, str(message.author.id))
        else:
            print("already in cooldowns")

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
    elif str(message.channel.id) in sec.get("suggestions_channels"):
        await bot.add_reaction(message, "👍")
        await bot.add_reaction(message, "👎")
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
