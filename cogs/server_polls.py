from globals import *
from checks import *
from discord.ext import commands

class ServerPolls:
    """Server Polls"""

    def __init__(self, bot):
        self.bot = bot

    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        emoji = reaction.emoji

        if message.content.startswith(">poll") and message.author.id == user.id:
            if is_mod():
                substr = message.content[6:]
                theid = str(sec.get("polls_channel"))
                async for m in self.bot.logs_from(message.server.get_channel(theid), limit=50):
                    if m.content == substr:
                        await self.bot.add_reaction(m ,emoji)


def setup(bot):
    bot.add_cog(ServerPolls(bot))
