from checks import *


class InfoCommands:
    """Information Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def headcount(self, ctx, *args):
        """Shows total number of users on server."""
        print("headcount")
        members = ctx.message.server.members
        total = 0
        for m in members:
            total += 1
        await self.bot.say('There are ' + str(total) + ' members on this server')

    @commands.command(pass_context=True)
    async def bancount(self, ctx, *args):
        """Shows total number of bans on server."""
        lst = await self.bot.get_bans(ctx.message.server)
        total = 0;
        print(lst)
        for item in lst:
            total += 1
        await self.bot.say('There are ' + str(total) + ' bans on this server')


def setup(bot):
    bot.add_cog(InfoCommands(bot))
