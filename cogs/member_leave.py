from discord.ext import commands
from globals import *
import helpers
from datetime import datetime
import discord

class MemberLeave:

    def __init__(self, bot):
        self.bot = bot

    async def on_member_remove(self, member):
        print(autobans)
        if str(member.id) in autobans:
            autobans.remove(str(member.id))
            return

        welcome_channel = member.server.get_channel(str(sec.settings["welcome_channel"]))
        print("MEMBER LEFT")
        e = discord.Embed()
        e.title = "Goodbye " + member.name + "!"
        e.description = "Have a great life!"
        e.colour = discord.Color.red()
        e.set_footer(icon_url=member.avatar_url, text=str(member.id))
        await self.bot.send_message(welcome_channel, "**> MEMBER LEFT:** " + member.mention, embed=e)

def setup(bot):
    bot.add_cog(MemberLeave(bot))