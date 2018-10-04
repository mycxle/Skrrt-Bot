from checks import *

class AdminCommands:
    """Admin-Only Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['everyone'])
    @is_admin()
    async def ping(self, ctx, *text):
        """Pings the entire server."""
        e = discord.utils.get(ctx.message.server.roles, id=str(Global.security.get("everyone_role")))
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
        if Global.security.get("whitelist") == 1:
            Global.security.set("whitelist", 0)
            await self.bot.say("Whitelist Only: DISABLED")
        else:
            Global.security.set("whitelist", 1)
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
            Global.security.set(var, val)
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
            for k in Global.security.settings:
                s += str(k) + "(" + str(Global.security.settings[k]) + "), "
                e.add_field(name=str(k), value=str(Global.security.settings[k]))
            await self.bot.say(embed=e)
        else:
            try:
                e.add_field(name=var, value=Global.security.get(var))
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
            Global.security.add(list, val)
            e.add_field(name=list, value=str(Global.security.settings[list]))
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
            Global.security.remove(list, index)
            e.add_field(name=list, value=str(Global.security.settings[list]))
            await self.bot.say(embed=e)
        except Exception as e:
            await self.bot.say("ERROR: " + str(e))

    async def lock_unlock_channels(self, ctx, val):
        unlck = None
        if val == 1:
            unlck = False

        Global.security.set("is_locked_channels", val)
        everyone_overwrite = discord.PermissionOverwrite(send_messages=unlck)
        everyone_role = None
        for r in ctx.message.server.roles:
            if r.is_everyone:
                everyone_role = r
        for c in Global.security.settings["channels_list"]:
            channel = ctx.message.server.get_channel(c)
            if channel in ctx.message.server.channels:
                await self.bot.edit_channel_permissions(channel, everyone_role, everyone_overwrite)

    @commands.command(pass_context=True)
    @is_admin()
    async def lock(self, ctx, option=None):
        """Locks all channels and/or joins."""
        if not option is None:
            if option == "s":
                if Global.security.get("is_locked_server") == 1:
                    return await self.bot.say("SERVER IS ALREADY LOCKED!")
                Global.security.set("is_locked_server", 1)
                await self.bot.say("SERVER IS LOCKED!")
            elif option == "c":
                if Global.security.get("is_locked_channels") == 1:
                    return await self.bot.say("CHANNELS ARE ALREADY LOCKED!")
                await self.lock_unlock_channels(ctx, 1)
                await self.bot.say("CHANNELS ARE LOCKED!")
            else:
                await self.bot.say("ERROR: Invalid argument")
        else:
            if Global.security.get("is_locked_server") == 1 and Global.security.get("is_locked_channels") == 1:
                return await self.bot.say("WE ARE ALREADY FULLY LOCKED!")
            Global.security.set("is_locked_server", 1)
            await self.lock_unlock_channels(ctx, 1)
            await self.bot.say("WE ARE NOW FULLY LOCKED!")

    @commands.command(pass_context=True)
    @is_admin()
    async def unlock(self, ctx, option=None):
        """Unlocks all channels and/or joins."""
        if not option is None:
            if option == "s":
                if Global.security.get("is_locked_server") == 0:
                    return await self.bot.say("SERVER IS ALREADY UNLOCKED!")
                Global.security.set("is_locked_server", 0)
                await self.bot.say("SERVER IS UNLOCKED!")
            elif option == "c":
                if Global.security.get("is_locked_channels") == 0:
                    return await self.bot.say("CHANNELS ARE ALREADY UNLOCKED!")
                await self.lock_unlock_channels(ctx, 0)
                await self.bot.say("CHANNELS ARE UNLOCKED!")
            else:
                await self.bot.say("ERROR: Invalid argument")
        else:
            if Global.security.get("is_locked_server") == 0 and Global.security.get("is_locked_channels") == 0:
                return await self.bot.say("WE ARE ALREADY FULLY UNLOCKED!")
            Global.security.set("is_locked_server", 0)
            await self.lock_unlock_channels(ctx, 0)
            await self.bot.say("WE ARE NOW FULLY UNLOCKED!")

    @commands.command(pass_context=True)
    @is_admin()
    async def updateinventories(self, ctx, *role):
        """Binds role to current users' inventories."""
        the_role = None
        if len(role) == 0:
            return await self.bot.say("`please specify the role`")
        if len(role) == 1:
            test = discord.utils.get(ctx.message.server.roles, id=str(role[0]))
            if test is not None:
                the_role = test
            else:
                roles_list = ctx.message.server.roles
                for r in roles_list:
                    name = r.name.lower()
                    if str(role[0]).lower() in name:
                        the_role = r
        else:
            roles_list = ctx.message.server.roles
            for r in roles_list:
                name = r.name.lower()
                if str(" ".join(role)).lower() in name:
                    the_role = r

        added_to = []
        members = ctx.message.server.members
        for m in members:
            if the_role in m.roles:
                my_roles = Global.db.child("inventory").child(m.id).child("roles").get().val()
                if my_roles is None:
                    Global.db.child("inventory").child(m.id).child("roles").set({str(the_role.id): str(the_role.id)})
                else:
                    Global.db.child("inventory").child(m.id).child("roles").update({str(the_role.id): str(the_role.id)})
                added_to.append(str(m.name) + "#" + str(m.discriminator))

        await self.bot.say("**added {} to the following inventories:** {}".format(the_role.mention, ", ".join(added_to)))

    @commands.command(pass_context=True)
    @is_admin()
    async def withdraw(self, ctx, amount=None):
        """Withdraws money from the server bank."""

        if amount is None:
            return await self.bot.say("`please provide an amount!`")

        try:
            amount = round(float(amount), 2)
        except:
            return await self.bot.say("`invalid amount!`")

        if amount <= 0:
            return await self.bot.say("`amount must be positive!`")

        u = Global.money.get_user((self.bot.user.id))
        balance = round(float(u["balance"]), 2)

        if amount > balance:
            return await self.bot.say("`the bank doesn't have that much!`")

        Global.money.withdraw(self.bot.user.id, amount)
        Global.money.deposit(ctx.message.author.id, amount)

        await self.bot.say("`${:.2f} successfully withdrawn!`".format(amount))

    @commands.command(pass_context=True)
    @is_admin()
    async def purge(self, ctx, num=None):
        """Purges messages from a channel."""

        if num is None:
            return await self.bot.say("`please provide a number!`")
            await self.bot.delete_message(ctx.message)
        else:
            try:
                num = int(num)
            except:
                return await self.bot.say("invalid number!`")
                await self.bot.delete_message(ctx.message)

        try:
            deleted = await self.bot.purge_from(ctx.message.channel, limit=num, before=ctx.message)
            await self.bot.delete_message(ctx.message)
        except Exception as e:
            await self.bot.say("EXCEPTION: " + str(e))
            await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(AdminCommands(bot))
