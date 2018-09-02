import discord
from discord.ext import commands
from discord.ext.commands import Bot
from globals import Global
from chans import *
import secrets
import sys
import os

class Skrrt:
    def __init__(self, bot):
        self.bot = bot
        self.extensions = ["admin_commands", "mod_commands", "info_commands", "fun_commands", "member_join", "member_leave", "server_polls", "money_commands", "shop_commands"]
        self.chans = [MathChan(), GenChan(), CountChan(), SuggestChan(), MoneyChans()]
        self.token = None
        if len(sys.argv) >= 2 and sys.argv[1] == "l":
            self.token = secrets.BOT_TOKEN
        else:
            self.token = os.environ['BOT_TOKEN']

        for extension in self.extensions:
            try:
                self.bot.load_extension("cogs." + extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))

    async def on_ready(self):
        print("Bot logged in.")
        await self.bot.change_presence(game=discord.Game(name="with big goth tiddies"))
        Global.all_emojis = list(self.bot.get_all_emojis())

    async def on_message(self, message):
        for c in self.chans:
            await c.on_message(self.bot, message)

        if message.author.id in Global.role_creators:
            entry = Global.role_creators[message.author.id]
            if message.channel.id == entry[0]:
                crc = entry[1]
                if crc.done is False:
                    resp = crc.get_response(message.content)
                    if resp == 0:
                        await self.bot.send_message(message.channel, message.author.mention + " " + "**Custom role canceled!**")
                        del Global.role_creators[message.author.id]
                    elif isinstance(resp, str):
                        await self.bot.send_message(message.channel, message.author.mention + " **" + resp + "**")
                    elif resp == 2:
                        msg = await self.bot.send_message(message.channel, message.author.mention, embed=Global.shop.get_custom_roles_instructions_embed(crc))
                        await self.bot.add_reaction(msg, "👍")
                        await self.bot.add_reaction(msg, "👎")
                        crc.confirmID = msg.id
                    elif resp == 3:
                        await self.bot.send_message(message.channel, message.author.mention + " " + crc.get_current())

    async def on_reaction_add(self, reaction, user):
        print("the fuck")

        message = reaction.message
        emoji = reaction.emoji

        if user.id in Global.role_creators:
            entry = Global.role_creators[user.id]
            crc = entry[1]
            print(message.id)
            print(crc.confirmID)
            if message.channel.id == entry[0] and message.id == crc.confirmID:
                print("we here")
                if emoji == "👍":
                    u = Global.money.get_user(user.id)
                    balance = round(float(u["balance"]), 2)
                    price = 3000
                    if balance < price:
                        del Global.role_creators[user.id]
                        await self.bot.send_message(message.channel, "`you don't have enough money!`")
                        return

                    everyone_role = discord.utils.get(message.server.roles, is_everyone=True)
                    r = await self.bot.create_role(server=message.server, name=crc.name, colour=discord.Colour(int(crc.color[1:], 16)),
                                              hoist=False, mentionable=False, permissions=everyone_role.permissions)

                    my_roles = Global.db.child("inventory").child(user.id).child("roles").get().val()
                    if my_roles is None:
                        Global.db.child("inventory").child(user.id).child("roles").set({str(r.id): str(r.id)})
                    else:
                        Global.db.child("inventory").child(user.id).child("roles").update({str(r.id): str(r.id)})

                    Global.money.withdraw(user.id, price)
                    Global.money.deposit(self.bot.user.id, price)

                    shop_role = discord.utils.get(message.server.roles, id=str(Global.security.get("roles_shop_id")))
                    exclusive_role = discord.utils.get(message.server.roles, id=str(Global.security.get("roles_exclusive_id")))

                    shop_pos = shop_role.position
                    exclusive_pos = exclusive_role.position

                    await self.bot.add_roles(user, r)
                    await self.bot.send_message(message.channel, "{} **you just created {} for ${:.2f}!**".format(user.mention, r.mention, price))

                    if crc.purchasable is True:
                        Global.db.child("shop").child("roles").update({str(r.id): str(crc.price)})
                        await self.bot.move_role(server=message.server, role=r, position=shop_pos-1)
                    else:
                        await self.bot.move_role(server=message.server, role=r, position=exclusive_pos-1)

                    del Global.role_creators[user.id]

                elif emoji == "👎":
                    await self.bot.send_message(message.channel, user.mention + " " + "**Custom role canceled!**")
                    del Global.role_creators[user.id]