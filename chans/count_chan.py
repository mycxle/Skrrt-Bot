import asyncio
from globals import Global


class CountChan:
    def __init__(self):
        self.id = Global.security.get("counting_channel")

    @asyncio.coroutine
    async def on_message(self, bot, message):
        if message.channel.id != self.id:
            return
        secnd = False
        async for m in bot.logs_from(message.channel, limit=2):
            if secnd and message.author.id != bot.user.id:
                if message.author.id == m.author.id:
                    await bot.delete_message(message)
                else:
                    try:
                        if int(message.content) != int(m.content) + 1:
                            await bot.delete_message(message)
                    except:
                        await bot.delete_message(message)
            secnd = True
