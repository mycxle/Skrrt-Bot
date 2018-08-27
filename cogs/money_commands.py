from discord.ext import commands
import random
import praw
import sys
import os
import discord
from globals import *

class MoneyCommands:
    """Money Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        user_dict = db.child("money").child(str(ctx.message.author.id)).get().val()
        money = round(float(user_dict["balance"]), 2)
        if user_dict is None:
            db.child("money").child(str(ctx.message.author.id)).set({"balance": "0", "last_daily": "..."})
            money = 0
        await self.bot.say("`you have $" + str(money) + "`")

def setup(bot):
    bot.add_cog(MoneyCommands(bot))