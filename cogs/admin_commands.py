from checks import *

class AdminCommands:
    """Admin-Only Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['everyone'])
    @is_admin()
    async def ping(self, ctx, *text):
        """Pings the entire server."""
        e = discord.utils.get(ctx.message.server.roles, id=str(sec.get("everyone_role")))
        await self.bot.edit_role(ctx.message.server, e, mentionable=True)

        await self.bot.delete_message(ctx.message)
        ghost = False
        if len(text) == 1:
            if text[0].lower() == "g" or text[0].lower() == "ghost" or text[0].lower() == "ghostping":
                ghost = True

        if not ghost:
            new_args = list(text[0:])
            text = ' '.join(new_args)
            await self.bot.say(e.mention + " " + text)
        else:
            m = await self.bot.say(e.mention)
            await self.bot.delete_message(m)

        await self.bot.edit_role(ctx.message.server, e, mentionable=False)

    @commands.command(pass_context=True)
    @is_admin()
    async def ghostping(self, ctx):
        """Ghostpings the entire server."""
        await ctx.invoke(self.ping, "ghostping")

    @commands.command(pass_context=True)
    @is_admin()
    async def whitelist(self, ctx):
        """Enables/Disables server whitelist."""
        if sec.get("whitelist") == 1:
            sec.set("whitelist", 0)
            await self.bot.say("Whitelist Only: DISABLED")
        else:
            sec.set("whitelist", 1)
            await self.bot.say("Whitelist Only: ENABLED")

    @commands.command(pass_context=True, aliases=['set'])
    @is_admin()
    async def dbset(self, ctx, var=None, val=None):
        """Sets value of DB variable."""
        e = discord.Embed()
        e.colour = discord.Color.red()
        if var is None and val is None:
            return await self.bot.say("ERROR: Command takes 2 arguments")
        try:
            sec.set(var, val)
            e.add_field(name=var, value=val)
            await self.bot.say(embed=e)
        except Exception as e:
            await self.bot.say("ERROR: " + str(e))


    @commands.command(pass_context=True, aliases=['get'])
    @is_admin()
    async def dbget(self, ctx, var=None):
        """Gets value of DB variable."""

        e = discord.Embed()
        e.colour = discord.Color.red()


        if var is None:
            s = ""
            for k in sec.settings:
                s += str(k) + "(" + str(sec.settings[k]) + "), "
                e.add_field(name=str(k), value=str(sec.settings[k]))
            await self.bot.say(embed=e)
        else:
            try:
                e.add_field(name=var, value=sec.get(var))
                await self.bot.say(embed=e)
            except Exception as e:
                await self.bot.say("ERROR: " + str(e))

    @commands.command(pass_context=True, aliases=['add'])
    @is_admin()
    async def dbadd(self, ctx, list=None, val=None):
        """Adds value to DB list."""

        e = discord.Embed()
        e.colour = discord.Color.red()

        if list is None and val is None:
            return await self.bot.say("ERROR: Command takes 2 arguments")
        try:
            sec.add(list, val)
            e.add_field(name=list, value=str(sec.settings[list]))
            await self.bot.say(embed=e)
        except Exception as e:
            await self.bot.say("ERROR: " + str(e))

    @commands.command(pass_context=True, aliases=['remove'])
    @is_admin()
    async def dbremove(self, ctx, list=None, index=None):
        """Removes value from DB list."""

        e = discord.Embed()
        e.colour = discord.Color.red()


        if list is None and index is None:
            return await self.bot.say("ERROR: Command takes 2 arguments")
        try:
            sec.remove(list, index)
            e.add_field(name=list, value=str(sec.settings[list]))
            await self.bot.say(embed=e)
        except Exception as e:
            await self.bot.say("ERROR: " + str(e))

    async def lock_unlock_channels(self, ctx, val):
        unlck = None
        if val == 1:
            unlck = False

        sec.set("is_locked_channels", val)
        everyone_overwrite = discord.PermissionOverwrite(send_messages=unlck)
        everyone_role = None
        for r in ctx.message.server.roles:
            if r.is_everyone:
                everyone_role = r
        for c in sec.settings["channels_list"]:
            channel = ctx.message.server.get_channel(c)
            if channel in ctx.message.server.channels:
                await self.bot.edit_channel_permissions(channel, everyone_role, everyone_overwrite)

    @commands.command(pass_context=True)
    @is_admin()
    async def lock(self, ctx, option=None):
        """Locks all channels and/or joins."""
        if not option is None:
            if option == "s":
                if sec.get("is_locked_server") == 1:
                    return await self.bot.say("SERVER IS ALREADY LOCKED!")
                sec.set("is_locked_server", 1)
                await self.bot.say("SERVER IS LOCKED!")
            elif option == "c":
                if sec.get("is_locked_channels") == 1:
                    return await self.bot.say("CHANNELS ARE ALREADY LOCKED!")
                await self.lock_unlock_channels(ctx, 1)
                await self.bot.say("CHANNELS ARE LOCKED!")
            else:
                await self.bot.say("ERROR: Invalid argument")
        else:
            if sec.get("is_locked_server") == 1 and sec.get("is_locked_channels") == 1:
                return await self.bot.say("WE ARE ALREADY FULLY LOCKED!")
            sec.set("is_locked_server", 1)
            await self.lock_unlock_channels(ctx, 1)
            await self.bot.say("WE ARE NOW FULLY LOCKED!")

    @commands.command(pass_context=True)
    @is_admin()
    async def unlock(self, ctx, option=None):
        """Unlocks all channels and/or joins."""
        if not option is None:
            if option == "s":
                if sec.get("is_locked_server") == 0:
                    return await self.bot.say("SERVER IS ALREADY UNLOCKED!")
                sec.set("is_locked_server", 0)
                await self.bot.say("SERVER IS UNLOCKED!")
            elif option == "c":
                if sec.get("is_locked_channels") == 0:
                    return await self.bot.say("CHANNELS ARE ALREADY UNLOCKED!")
                await self.lock_unlock_channels(ctx, 0)
                await self.bot.say("CHANNELS ARE UNLOCKED!")
            else:
                await self.bot.say("ERROR: Invalid argument")
        else:
            if sec.get("is_locked_server") == 0 and sec.get("is_locked_channels") == 0:
                return await self.bot.say("WE ARE ALREADY FULLY UNLOCKED!")
            sec.set("is_locked_server", 0)
            await self.lock_unlock_channels(ctx, 0)
            await self.bot.say("WE ARE NOW FULLY UNLOCKED!")


def setup(bot):
    bot.add_cog(AdminCommands(bot))
