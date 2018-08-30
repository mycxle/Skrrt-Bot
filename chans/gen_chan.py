import asyncio
from globals import Global
import random
import discord


class GenChan:
    def __init__(self):
        self.id = Global.security.get("general_channel")

    @asyncio.coroutine
    async def on_message(self, bot, message):
        msg_content = message.content
        author = message.author
        if message.channel.id == self.id and not msg_content.startswith(Global.bot_prefix) and not author.bot:
            num = random.randint(1, 201)
            if num == 5 or num == 7:
                await bot.add_reaction(message, random.choice(Global.all_emojis))
            elif num == 6:
                Global.collectable = random.choice([1, 5, 10, 20])
                e = discord.Embed()
                e.colour=discord.Color.green()
                e.title="🚨 FREE MONEY 🚨"
                e.description="A random ${} appeared!\nType `{}grab` to collect!".format(Global.collectable, Global.bot_prefix)
                e.set_thumbnail(url="https://cdn.shopify.com/s/files/1/1061/1924/files/Money_Face_Emoji.png")
                await bot.send_message(message.channel, embed=e)
