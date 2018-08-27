from discord.ext import commands
from globals import *
import helpers
from datetime import datetime
import discord

class MemberJoin:

    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        welcome_channel = member.server.get_channel(str(sec.settings["welcome_channel"]))
        rules_channel = member.server.get_channel(str(sec.settings["rules_channel"]))
        logs_channel = member.server.get_channel(str(sec.settings["logs_channel"]))

        member_name = member.name
        newaccounts_age = int(sec.get("newaccounts_age")) * 24
        server_locked = int(sec.get("is_locked_server"))

        if server_locked == 1:
            autobans.append(member.id)
            await self.bot.send_message(logs_channel,
                                   "LOCKED SERVER AUTO-BAN: " + member_name + " | " + str(member.id))
            return await self.bot.ban(member, delete_message_days=1)

        if newaccounts_age > 0:
            created = helpers.datetime_from_utc_to_local(member.created_at)
            current = datetime.now()
            diff = current - created
            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            print("Account is " + str(hours) + " old.")
            if hours < newaccounts_age:
                autobans.append(member.id)
                await self.bot.send_message(logs_channel,
                                       "NEW ACCOUNT AUTO-BANNED: " + member_name + " | " + str(member.id) + " | Age: "
                                       + str(hours) + "h " + str(minutes) + "m " + str(seconds) + "s")
                return await self.bot.ban(member, delete_message_days=1)

        print("MEMBER JOINED")
        e = discord.Embed()
        e.set_thumbnail(url=member.avatar_url)
        e.title = "Welcome " + member_name + "!"
        e.description = "Be sure to read " + rules_channel.mention
        e.colour = discord.Color.green()
        e.set_footer(text=str(member.id))
        await self.bot.send_message(welcome_channel, "**> MEMBER JOINED:** " + member.mention, embed=e)

def setup(bot):
    bot.add_cog(MemberJoin(bot))