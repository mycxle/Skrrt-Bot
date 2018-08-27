from discord.ext import commands
import random
import praw
import sys
import os
import discord

class FunCommands:
    """Fun Commands"""

    def __init__(self, bot):
        self.bot = bot
        if len(sys.argv) >= 2 and sys.argv[1] == "l":
            import secrets
            self.reddit = praw.Reddit(client_id=secrets.r_client_id,
                                 client_secret=secrets.r_client_secret,
                                 user_agent=secrets.r_user_agent)
        else:
            self.reddit = praw.Reddit(client_id=os.environ['r_client_id'],
                                 client_secret=os.environ['r_client_secret'],
                                 user_agent=os.environ['r_user_agent'])

    @commands.command(pass_context=True)
    async def coin(self, ctx):
        """Flips a coin."""
        choice = random.randint(1, 2)
        if choice == 1:
            await self.bot.add_reaction(ctx.message, '🍆')
        elif choice == 2:
            await self.bot.add_reaction(ctx.message, '🍑')

    @commands.command()
    async def meme(self):
        """Posts random meme from r/dankmemes."""
        found = False
        n = random.randint(1, 91)
        count = 0
        for submission in self.reddit.subreddit('dankmemes').hot(limit=100):
            count += 1
            if count == n:
                found = True
            if found is True:
                u = submission.url
                if u.endswith("jpg") or u.endswith("jpeg") or u.endswith("png") or u.endswith("gif"):
                    e = discord.Embed()
                    e.set_image(url=submission.url)
                    e.title=submission.title
                    e.colour=discord.Color.red()
                    e.set_footer(text="made by " + str(submission.author.name))
                    await self.bot.say(embed=e)
                    break

def setup(bot):
    bot.add_cog(FunCommands(bot))