import discord
from discord.ext import commands
from discord.ext.commands import Bot
from globals import Global
from chans import *
import secrets
import sys
import os

bot = Bot(command_prefix=Global.bot_prefix)
extensions = ["admin_commands", "mod_commands", "info_commands", "fun_commands", "member_join", "member_leave", "server_polls", "money_commands", "shop_commands"]
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

    if message.author.id in Global.role_creators:
        entry = Global.role_creators[message.author.id]
        if message.channel.id == entry[0]:
            crc = entry[1]
            if crc.done is False:
                resp = crc.get_response(message.content)
                if resp == 0:
                    await bot.send_message(message.channel, message.author.mention + " " + "**Custom role canceled!**")
                    del Global.role_creators[message.author.id]
                elif isinstance(resp, str):
                    await bot.send_message(message.channel, message.author.mention + " **" + resp + "**")
                elif resp == 2:
                    msg = await bot.send_message(message.channel, message.author.mention, embed=Global.shop.get_custom_roles_instructions_embed(crc))
                    await bot.add_reaction(msg, "👍")
                    await bot.add_reaction(msg, "👎")
                    crc.confirmID = msg.id
                elif resp == 3:
                    await bot.send_message(message.channel, message.author.mention + " " + crc.get_current())
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
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
                    await bot.send_message(message.channel, "`you don't have enough money!`")
                    return

                everyone_role = discord.utils.get(message.server.roles, is_everyone=True)
                r = await bot.create_role(server=message.server, name=crc.name, colour=discord.Colour(int(crc.color[1:], 16)),
                                      hoist=False, mentionable=False, permissions=everyone_role.permissions)

                my_roles = Global.db.child("inventory").child(user.id).child("roles").get().val()
                if my_roles is None:
                    Global.db.child("inventory").child(user.id).child("roles").set({str(r.id): str(r.id)})
                else:
                    Global.db.child("inventory").child(user.id).child("roles").update({str(r.id): str(r.id)})

                Global.money.withdraw(user.id, price)
                Global.money.deposit(bot.user.id, price)

                shop_role = discord.utils.get(message.server.roles, id=str(Global.security.get("roles_shop_id")))
                exclusive_role = discord.utils.get(message.server.roles, id=str(Global.security.get("roles_exclusive_id")))

                shop_pos = shop_role.position
                exclusive_pos = exclusive_role.position

                await bot.add_roles(user, r)
                await bot.send_message(message.channel, "{} **you just created {} for ${:.2f}!**".format(user.mention, r.mention, price))

                if crc.purchasable is True:
                    Global.db.child("shop").child("roles").update({str(r.id): str(crc.price)})
                    await bot.move_role(server=message.server, role=r, position=shop_pos-1)
                else:
                    await bot.move_role(server=message.server, role=r, position=exclusive_pos-1)

                del Global.role_creators[user.id]

            elif emoji == "👎":
                await bot.send_message(message.channel, user.mention + " " + "**Custom role canceled!**")
                del Global.role_creators[user.id]

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
