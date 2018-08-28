from discord.ext import commands
import random
import praw
import sys
import os
import discord
from globals import *
from datetime import datetime
from dateutil import parser
from datetime import timedelta
import math

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

    def get_daily(self):
        return round(random.uniform(50, 100), 2)

    @commands.command(pass_context=True)
    async def daily(self, ctx):
        now_time = datetime.now()
        user_dict = db.child("money").child(str(ctx.message.author.id)).get().val()

        if user_dict is None:
            money = self.get_daily()
            db.child("money").child(str(ctx.message.author.id)).set({"balance": str(round(money, 2)), "last_daily": str(now_time)})
            await self.bot.say("`you earned ${}!`".format(str(round(money, 2))))
        else:
            balance = round(float(user_dict["balance"]), 2)
            last_daily = str(user_dict["last_daily"])
            if last_daily == "...":
                money = self.get_daily()
                balance += money
                db.child("money").child(str(ctx.message.author.id)).set({"balance": str(round(balance, 2)), "last_daily": str(now_time)})
                await self.bot.say("`you earned ${}!`".format(str(round(money, 2))))
                return
            lastdaily_time = parser.parse(last_daily)
            time_difference = now_time - lastdaily_time
            time_difference_in_minutes = math.floor(time_difference / timedelta(minutes=1))
            print("in minutes: " + str(time_difference_in_minutes))
            if time_difference_in_minutes < 720:
                optimal_time = (lastdaily_time + timedelta(hours=12)) - now_time
                days, seconds = optimal_time.days, optimal_time.seconds
                hours = days * 24 + seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60

                timestr = ""
                if hours > 0:
                    timestr = "{} hours".format(hours+1)
                elif minutes > 0:
                    timestr = "{} minutes".format(minutes)
                elif seconds > 0:
                    timestr = "{} seconds".format(seconds)
                await self.bot.say("`you can earn more in {}!`".format(timestr))
            else:
                money = self.get_daily()
                balance += money
                db.child("money").child(str(ctx.message.author.id)).set({"balance": str(round(balance, 2)), "last_daily": str(now_time)})
                await self.bot.say("`you earned ${}!`".format(str(round(money, 2))))

def setup(bot):
    bot.add_cog(MoneyCommands(bot))