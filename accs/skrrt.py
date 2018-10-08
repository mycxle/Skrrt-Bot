import discord
from discord.ext import commands
from discord.ext.commands import Bot
from globals import Global
from chans import *
import secrets
import sys
import os
from checks import *

class Skrrt:
    def __init__(self, bot):
        self.bot = bot
        self.extensions = ["admin_commands", "mod_commands", "info_commands", "fun_commands", "member_join", "member_leave", "server_polls", "money_commands", "shop_commands", "casino_commands", "custom_commands"]
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

        if len(sys.argv) >= 2 and sys.argv[1] == "l":
            pass
        else:
            voice_channel = discord.utils.get(message.server.channels, id='459913847806099456')
            secret_chan = discord.utils.get(message.server.channels, id='470827844487086082')

            members = voice_channel.voice_members
            memids = []

            for member in members:
                memids.append(str(member.id))

            if "497538479597682689" not in memids:
                await self.bot.send_message(secret_chan, "☆play https://www.youtube.com/watch?v=bKZ0tFTRODM")

        if message.author.id in Global.role_creators and not message.content.startswith(Global.bot_prefix):
            entry = Global.role_creators[message.author.id]
            if message.channel.id == entry[0]:
                print(message.content)
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

        # ===== BLACKJACK =====
        if user.id in Global.bjgames and Global.bjgames[user.id].msg.id == message.id:
            bjgame = Global.bjgames[user.id]
            if emoji == "▶":
                bust = bjgame.hit()
                if bust is False:
                    new_embed = bjgame.create_embed()
                    await self.bot.edit_message(message, embed=new_embed)
                else:
                    bjgame.done()
            elif emoji == "⏹":
                bjgame.done()
            elif emoji == "⏏" and bjgame.firstTurnDone is False:
                bjgame.surrender()
            elif emoji == "⏩" and bjgame.firstTurnDone is False:
                bjgame.double()

            await self.bot.remove_reaction(message, emoji, user)

            # if bjgame.firstTurnDone is True:
            #     print("asdfasdf")
            #     try:
            #         await self.bot.remove_reaction(message, "⏩", message.author)
            #     except:
            #         pass
            #     try:
            #         await self.bot.remove_reaction(message, "⏏", message.author)
            #     except:
            #         pass

            if bjgame.is_over():
                new_embed = bjgame.create_embed(winEmbed=True)
                await self.bot.edit_message(message, embed=new_embed)
                await self.bot.clear_reactions(message)

                winner = bjgame.who_won()
                bet = bjgame.bet
                if bjgame.surrendered is True:
                    bet /= 2

                u = Global.money.get_user(str(bjgame.user.id))
                balance = round(float(u["balance"]), 2)

                if winner == 1:
                    if bet > balance:
                        Global.money.withdraw(str(bjgame.user.id), balance)
                        Global.money.deposit(self.bot.user.id, balance)
                    else:
                        Global.money.withdraw(str(bjgame.user.id), bet)
                        Global.money.deposit(self.bot.user.id, bet)
                elif winner == 0:
                    Global.money.withdraw(self.bot.user.id, bet)
                    Global.money.deposit(str(bjgame.user.id), bet)


                del Global.bjgames[user.id]


    @commands.command(pass_context=True)
    @is_admin()
    async def load(self, ctx, extension):
        """Loads cog."""
        try:
            self.bot.load_extension("cogs." + extension)
            print("Loaded: {}".format(extension))
        except Exception as e:
            print("Error loading {}: {}".format(extension, str(e)))

    @commands.command(pass_context=True)
    @is_admin()
    async def unload(self, ctx, extension):
        """Unloads cog."""
        try:
            self.bot.unload_extension("cogs." + extension)
            print("Unloaded: {}".format(extension))
        except Exception as e:
            print("Error unloading {}: {}".format(extension, str(e)))

    @commands.command(pass_context=True)
    @is_admin()
    async def reload(self, ctx, extension):
        """Reloads cog."""
        await ctx.invoke(self.unload, extension)
        await ctx.invoke(self.load, extension)