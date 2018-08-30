from discord.ext import commands
from globals import *
import discord

class ShopCommands:
    """Shop Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def shop(self, ctx, category=None):
        """See what's for sale in the shop."""
        if category is None:
            category = "role"
        if category == "role" or category == "roles":
            e = Global.shop.get_roles_embed(ctx)
            await self.bot.say(embed=e)

    @commands.command(pass_context=True)
    async def buy(self, ctx, *args):
        """Buy an item from the shop."""
        if len(args) != 2:
            return await self.bot.say("`provide shop category and item number!`")

        category = args[0]
        option = args[1]

        if category == "role" or category == "roles":
            try:
                r = Global.shop.get_role(int(option)-1)
            except:
                return await self.bot.say("`invalid item number!`")
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

    @commands.command(pass_context=True)
    async def inventory(self, ctx):
        """See what items you currently own."""
        my_roles = Global.db.child("inventory").child(ctx.message.author.id).child("roles").get().val()
        if my_roles is None:
            return await self.bot.say("`your inventory is empty!`")

        my_roles_list = list(my_roles.keys())
        mentions_list = []
        for r in my_roles_list:
            role = discord.utils.get(ctx.message.server.roles, id=r)
            mentions_list.append(role.mention)

        await self.bot.say("**you own the following roles: {}**".format(" ".join(mentions_list)))

    @commands.command(pass_context=True)
    async def role(self, ctx, role=None):
        """Add/Remove a role from yourself."""
        if role is None:
            return await self.bot.say("`you didn't provide the role name!`")

        my_roles = Global.db.child("inventory").child(ctx.message.author.id).child("roles").get().val()
        if my_roles is None:
            return await self.bot.say("`you don't own any roles!`")

        my_roles_list = list(my_roles.keys())
        roles = []
        for r in my_roles_list:
            the_role = discord.utils.get(ctx.message.server.roles, id=r)
            roles.append(the_role)

        role_name = role.lower()
        found_role = None

        for r in roles:
            r_name = r.name.lower()
            if role_name in r_name:
                found_role = r

        if found_role is None:
            return await self.bot.say("`couldn't find that role in your inventory!`")

        if found_role in ctx.message.author.roles:
            await self.bot.remove_roles(ctx.message.author, found_role)
            await self.bot.say("{} **removed {}!**".format(ctx.message.author.mention, found_role.mention))
        else:
            await self.bot.add_roles(ctx.message.author, found_role)
            await self.bot.say("{} **added {}!**".format(ctx.message.author.mention, found_role.mention))


def setup(bot):
    bot.add_cog(ShopCommands(bot))