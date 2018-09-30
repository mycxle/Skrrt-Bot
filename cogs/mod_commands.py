from checks import *
import helpers

class ModCommands:
    """Mod-Only Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @is_mod()
    async def goon(self, ctx, user=None):
        """Adds/Removes the goon role from user."""
        try:
            goon_role = discord.utils.get(ctx.message.server.roles, id=str(Global.security.get("goon_role")))
            m = None
            try:
                m = ctx.message.mentions[0]
            except:
                if not user is None:
                    try:
                        user_id = user
                        m = discord.utils.get(ctx.message.server.members, id=str(user_id))
                    except Exception as e:
                        await self.bot.say("EXCEPTION: " + str(e))
                else:
                    await self.bot.say("Please provide a user...")
                    return

            if goon_role in m.roles:
                await self.bot.remove_roles(m, goon_role)
                await self.bot.say(str(m.name + " is no longer a goon!"))
            else:
                await self.bot.add_roles(m, goon_role)
                await self.bot.say(str(m.name + " is now a goon!"))
        except Exception as e:
            await self.bot.say("EXCEPTION: " + str(e))


    @commands.command(pass_context=True)
    @is_mod()
    async def kick(self, ctx, *user):
        """Kicks user from server."""
        users = []
        mentions = ctx.message.mentions

        if len(mentions) == 0 and len(user) == 0:
            return await self.bot.say("`no user given!`")

        if len(mentions) > 0:
            users = mentions
        else:
            for u in user:
                error = False
                user_id = u.strip()
                try:
                    tmp = await self.bot.get_user_info(user_id)
                except:
                    await self.bot.say("`id doesn't exist!`")
                    error = True
                if error is not True:
                    try:
                        intid = int(user_id)
                    except:
                        await self.bot.say("`invalid id!`")
                        error = True
                if error is not True:
                    m = discord.utils.get(ctx.message.server.members, id=str(user_id))
                    if m is None:
                        await self.bot.say("`user not found!`")
                        error = True
                if error is not True:
                    users.append(m)

        if len(users) > 0:
            await self.bot.delete_message(ctx.message)

        for u in users:
            try:
                print("> " + str(u.id))
                await self.bot.kick(u)
                if len(users) > 1:
                    await self.bot.say("`" + u.name + "#" + str(u.discriminator) + " was kicked!`")
                else:
                    await self.bot.say(embed=helpers.get_moderation_embed(u, kick=True))
            except Exception as e:
                await self.bot.say("`error: " + str(e) + "`")

    @commands.command(pass_context=True)
    @is_mod()
    async def ban(self, ctx, *user):
        """Bans user from server."""
        users = []
        mentions = ctx.message.mentions

        if len(mentions) == 0 and len(user) == 0:
            return await self.bot.say("`no user given!`")

        if len(mentions) > 0:
            users = mentions
        else:
            for u in user:
                error = False
                user_id = u.strip()
                try:
                    tmp = await self.bot.get_user_info(user_id)
                except:
                    await self.bot.say("`id doesn't exist!`")
                    error = True
                if error is not True:
                    try:
                        intid = int(user_id)
                    except:
                        await self.bot.say("`invalid id!`")
                        error = True
                if error is not True:
                    m = discord.utils.get(ctx.message.server.members, id=str(user_id))
                    if m is None:
                        try:
                            m=discord.Object(id=user_id)
                            m.server= ctx.message.server
                            tmp = await self.bot.get_user_info(user_id)
                            m.name = tmp.name
                            m.discriminator = tmp.discriminator
                            m.avatar_url = tmp.avatar_url
                        except:
                            await self.bot.say("`user not found!`")
                            error = True
                if error is not True:
                    users.append(m)

        if len(users) > 0:
            await self.bot.delete_message(ctx.message)

        for u in users:
            try:
                print("> " + str(u.id))
                await self.bot.ban(u)
                if len(users) > 1:
                    await self.bot.say("`" + u.name + "#" + str(u.discriminator) + " was banned!`")
                else:
                    await self.bot.say(embed=helpers.get_moderation_embed(u, ban=True))
            except Exception as e:
                await self.bot.say("`error: " + str(e) + "`")

    @commands.command(pass_context=True)
    @is_mod()
    async def unban(self, ctx, *id):
        """Unbans user from server."""
        users = []

        if len(id) == 0:
            return await self.bot.say("`no id given!`")

        for u in id:
            error = False
            user_id = u.strip()
            try:
                tmp = await self.bot.get_user_info(user_id)
            except:
                await self.bot.say("`id doesn't exist!`")
                error = True
            if error is not True:
                try:
                    intid = int(user_id)
                except:
                    await self.bot.say("`invalid id!`")
                    error = True
            if error is not True:
                m = discord.utils.get(ctx.message.server.members, id=str(user_id))
                if m is None:
                    try:
                        m=discord.Object(id=user_id)
                        m.server= ctx.message.server
                        tmp = await self.bot.get_user_info(user_id)
                        m.name = tmp.name
                        m.discriminator = tmp.discriminator
                        m.avatar_url = tmp.avatar_url
                    except:
                        await self.bot.say("`user not found!`")
                        error = True
            if error is not True:
                users.append(m)

        if len(users) > 0:
            await self.bot.delete_message(ctx.message)

        for u in users:
            try:
                print("> " + str(u.id))
                await self.bot.unban(ctx.message.server, u)
                await self.bot.say("`" + u.name + "#" + str(u.discriminator) + " was unbanned!`")
            except Exception as e:
                await self.bot.say("`error: " + str(e) + "`")

    @commands.command(pass_context=True)
    @is_mod()
    async def poll(self, ctx, *text):
        """Creates a server poll."""
        polls_channel = ctx.message.server.get_channel(str(Global.security.get("polls_channel")))

        if len(text) > 0:
            msg = " ".join(text)
            await self.bot.send_message(polls_channel, msg)
        else:
            await self.bot.say("`no message provided!`")

    @commands.command(pass_context=True)
    @is_mod()
    async def say(self, ctx, *text):
        """Make the bot say something."""


        if len(text) > 0:
            msg = " ".join(text)
            await self.bot.say(msg)
            await self.bot.delete_message(ctx.message)
        else:
            await self.bot.say("`no message provided!`")
            await self.bot.delete_message(ctx.message)

def setup(bot):
    bot.add_cog(ModCommands(bot))
