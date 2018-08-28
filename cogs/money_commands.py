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
import asyncio
from timex import Timer
import collections

class MoneyCommands:
    """Money Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.mathcooldowns = []

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        the_user = str(ctx.message.author.id)
        if len(ctx.message.mentions) > 0:
            print("ok")
            tmp = ctx.message.mentions[0]
            print(str(tmp.id))
            the_user = tmp.id
        user_dict = db.child("money").child(the_user).get().val()
        if user_dict is None:
            db.child("money").child(the_user).set({"balance": "0", "last_daily": "..."})
            money = 0
        else:
            money = round(float(user_dict["balance"]), 2)
        if len(ctx.message.mentions) > 0:
            await self.bot.say("`they have $" + str(money) + "!`")
        else:
            await self.bot.say("`you have $" + str(money) + "!`")

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

    @commands.command(pass_context=True)
    async def grab(self, ctx):
        if Global.collectable is None: return

        user_dict = db.child("money").child(str(ctx.message.author.id)).get().val()
        if user_dict is None:
            db.child("money").child(str(ctx.message.author.id)).set({"balance": str(Global.collectable), "last_daily": "..."})
        else:
            balance = float(user_dict["balance"])
            balance += Global.collectable
            last_daily = str(user_dict["last_daily"])
            db.child("money").child(str(ctx.message.author.id)).set({"balance": str(round(balance, 2)), "last_daily": str(last_daily)})
        await self.bot.say(ctx.message.author.mention + " **grabbed ${}!**".format(str(round(Global.collectable, 2))))
        Global.collectable = None

    @asyncio.coroutine
    async def math_timeout(self, user):
        id = str(user.id)
        print("timeout")
        if id in Global.maths:
            del Global.maths[id]
            await self.bot.send_message(user.server.get_channel(str(sec.settings["math_channel"])),
                               str(user.mention + " `you took too long to answer!`"))

    @asyncio.coroutine
    async def math_cooldown(self, uid):
        self.mathcooldowns.remove(uid)

    @commands.command(pass_context=True)
    async def math(self, ctx):
        if str(ctx.message.channel.id) != str(sec.get("math_channel")):
            return await self.bot.say("`this isn't the math channel!`")
        else:
            id = str(ctx.message.author.id)
            if id in Global.maths:
                return

            if id in self.mathcooldowns:
                await self.bot.say(ctx.message.author.mention + " `slow down math wizard!`")
                return

            operation = random.choice(["+", "-", "*", "/"])
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)

            if operation == "-":
                if num2 > num1:
                    tmp = num1
                    num1 = num2
                    num2 = tmp
            elif operation == "/":
                if num2 > num1:
                    tmp = num1
                    num1 = num2
                    num2 = tmp
                while True:
                    if num1 % num2 == 0:
                        break
                    num2 = random.randint(1, 13)

            txt = " `what is {} {} {}?`".format(num1, operation, num2)

            if operation == "+":
                answer = num1 + num2
            elif operation == "-":
                answer = num1 - num2
            elif operation == "*":
                answer = num1 * num2
            elif operation == "/":
                answer = num1 // num2

            await self.bot.say(ctx.message.author.mention + txt)

            print(str(answer))
            print(str(id))
            Global.maths[id] = answer
            self.mathcooldowns.append(ctx.message.author.id)

            print(str(Global.maths))
            Timer(3, self.math_timeout, ctx.message.author)
            Timer(3, self.math_cooldown, ctx.message.author.id)

    @commands.command(pass_context=True)
    async def leaderboard(self, ctx):

        all_users = db.child("money").get().val()
        if "123" in all_users:
            del all_users["123"]

        top10 = list(collections.OrderedDict(sorted(all_users.items(), key=lambda key_value_pair: key_value_pair[1]['balance'], reverse=True)).items())[:10]

        string_list = []
        for entry in top10:
            try:
                member = await self.bot.get_user_info(str(entry[0]))
                string_list.append("{} - `${:.2f}`".format(member.mention, float(entry[1]["balance"])))
            except Exception as e:
                print(str(e))

        e = discord.Embed()
        e.colour=discord.Color.green()
        e.title="🚨 LEADERBOARD 🚨"
        e.set_thumbnail(url="https://cdn.shopify.com/s/files/1/1061/1924/files/Money_Face_Emoji.png")

        final_string = ""
        for i in range(len(string_list)):
            newline = "\n"
            if i == len(string_list) - 1: newline = ""
            final_string += "**{}** - {}{}".format(i+1, string_list[i], newline)

        e.description=final_string

        try:
            await self.bot.send_message(self.bot.get_channel(str(ctx.message.channel.id)), embed=e)
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(MoneyCommands(bot))