from discord.ext import commands
import asyncio
from globals import Global
from accs import *

loop = asyncio.get_event_loop()

skrrt_bot = commands.Bot(command_prefix=Global.bot_prefix)
skrrt_cog = Skrrt(skrrt_bot)
skrrt_bot.add_cog(skrrt_cog)
loop.create_task(skrrt_bot.start(skrrt_cog.token))

zkrrt_bot = commands.Bot(command_prefix=Global.bot_prefix)
zkrrt_cog = Zkrrt(zkrrt_bot)
zkrrt_bot.add_cog(zkrrt_cog)
loop.create_task(zkrrt_bot.start(zkrrt_cog.token))

try:
    loop.run_forever()
finally:
    loop.stop()