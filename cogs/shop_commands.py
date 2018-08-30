from discord.ext import commands
from globals import *
import discord

class ShopCommands:
    """Shop Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def shop(self, ctx, category=None):
        if category is None:
            pass
        elif category == "role" or category == "roles":
            e = Global.shop.get_roles_embed(ctx)
            await self.bot.say(embed=e)

    @commands.command(pass_context=True)
    async def buy(self, ctx, *args):
        if len(args) != 2:
            return

        category = args[0]
        option = args[1]

        if category == "role" or category == "roles":
            r = Global.shop.get_role(int(option)-1)
            role = discord.utils.get(ctx.message.server.roles, id=r[0])
            user = Global.money.get_user(ctx.message.author.id)
            balance = round(float(user["balance"]), 2)
            price = round(float(r[1]), 2)
            if balance < price:
                return await self.bot.say("`you don't enough money!`")

            my_roles = Global.db.child("inventory").child(ctx.message.author.id).child("roles").get().val()
            if my_roles is None:
                Global.db.child("inventory").child(ctx.message.author.id).child("roles").set({str(r[0]): str(r[0])})
            else:
                my_roles_list = list(my_roles.keys())
                if str(r[0]) in my_roles_list:
                    return await self.bot.say("`you already own that role!`")
                Global.db.child("inventory").child(ctx.message.author.id).child("roles").update({str(r[0]): str(r[0])})

            Global.money.withdraw(ctx.message.author.id, price)
            Global.money.deposit(self.bot.user.id, price)

            await self.bot.add_roles(ctx.message.author, role)
            return await self.bot.say("{} **you just bought {} for ${:.2f}!**".format(ctx.message.author.mention, role.mention, price))

def setup(bot):
    bot.add_cog(ShopCommands(bot))