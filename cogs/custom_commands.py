from checks import *
import helpers

class CustomCommands:
    """Custom Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['bröd'])
    @is_brodgod()
    async def brod(self, ctx, user=None):
        """Adds/Removes the goon role from user."""
        try:
            brod_role = discord.utils.get(ctx.message.server.roles, id=str(Global.security.get("brod_role")))
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

            if brod_role in m.roles:
                await self.bot.remove_roles(m, brod_role)
                await self.bot.say(str(m.name + " is no longer in bröd gang!"))
            else:
                await self.bot.add_roles(m, brod_role)
                await self.bot.say(str(m.name + " is now in bröd gang!"))
        except Exception as e:
            await self.bot.say("EXCEPTION: " + str(e))

def setup(bot):
    bot.add_cog(CustomCommands(bot))