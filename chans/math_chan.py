import asyncio
from globals import Global


class MathChan:
    def __init__(self):
        self.id = Global.security.get("math_channel")

    @asyncio.coroutine
    async def on_message(self, bot, message):
        msg_content = message.content
        author = message.author
        if not(message.channel.id == self.id and not msg_content.startswith(Global.bot_prefix) and not author.bot):
            return
        if author.id in Global.maths:
            try:
                num = int(msg_content)
                ans = Global.maths.get(author.id)
                math_channel = message.server.get_channel(self.id)

                if num is ans:
                    del Global.maths[author.id]
                    amount = Global.money.get_math_money()
                    Global.money.deposit(author.id, amount)
                    txt = author.mention + " `that's correct! you earned ${:.2f}!`".format(amount)
                    await bot.send_message(math_channel, txt)
                else:
                    del Global.maths[str(author.id)]
                    await bot.send_message(math_channel, author.mention + " `that's incorrect!`")
            except Exception as e:
                print(str(e))
