import asyncio
from globals import Global


class SuggestChan:
    def __init__(self):
        self.ids = Global.security.get("suggestions_channels")

    @asyncio.coroutine
    async def on_message(self, bot, message):
        if message.channel.id in self.ids:
            await bot.add_reaction(message, "👍")
            await bot.add_reaction(message, "👎")
