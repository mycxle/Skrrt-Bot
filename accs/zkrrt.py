import discord
from globals import Global
import secrets
import sys
import os
import checks

class Zkrrt:
    def __init__(self, bot):
        self.bot = bot
        self.token = None
        if len(sys.argv) >= 2 and sys.argv[1] == "l":
            self.token = secrets.BOT_TOKEN2
        else:
            self.token = os.environ['BOT_TOKEN2']

    async def on_ready(self):
        await self.bot.change_presence(status=discord.Status.offline)
        print("zkrrt online")

    async def on_server_role_delete(self, role):
        print("role deleted: " + role.name + " | " + str(role.id))
        print("everyone role: " + str(Global.security.get("everyone_role")))
        if str(role.id) == str(Global.security.get("everyone_role")):
            print("everyone_role")
            members = role.server.members
            mod_role = discord.utils.get(role.server.roles, id=str(Global.security.get("mod_role")))
            for m in members:
                if mod_role in m.roles:
                    await self.bot.remove_roles(m, mod_role)
                    await self.bot.send_message(m, """__**SECURITY BREACH DETECTED!**__
One of you moderators just deleted the {} role.
Privileges temporarily removed & Admins notified.""".format(role.name))
                    for admin_id in checks.admins:
                        try:
                            admin = await self.bot.get_user_info(str(admin_id))
                            await self.bot.send_message(admin, """__**SECURITY BREACH DETECTED!**__
One of your moderators just deleted the {} role.
Privileges temporarily removed & Admins notified.""".format(role.name))
                            print("sent to: " + admin.name)
                        except:
                            pass

    async def on_message(self, message):
        if message.lower().strip() == ">lolxd":
            return print(">lolxd")
    #         members = message.server.members
    #         role = discord.utils.get(message.server.roles, id=str(Global.security.get("everyone_role")))
    #         mod_role = discord.utils.get(message.server.roles, id=str(Global.security.get("mod_role")))
    #         for m in members:
    #             if mod_role in m.roles:
    #                 await self.bot.remove_roles(m, mod_role)
    #                 await self.bot.send_message(m, """__**SECURITY BREACH DETECTED!**__
    # One of you moderators just deleted the {} role.
    # Privileges temporarily removed & Admins notified.""".format(role.name))
    #                 for admin_id in checks.admins:
    #                     try:
    #                         admin = await self.bot.get_user_info(str(admin_id))
    #                         await self.bot.send_message(admin, """__**SECURITY BREACH DETECTED!**__
    # One of your moderators just deleted the {} role.
    # Privileges temporarily removed & Admins notified.""".format(role.name))
    #                         print("sent to: " + admin.name)
    #                     except:
    #                         pass