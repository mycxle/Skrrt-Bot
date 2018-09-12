from discord.ext import commands
import random
import praw
import sys
import os
import discord
from globals import Global
from blackjack.blackjack import BlackJack

class CasinoCommands:
    """Casino Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def blackjack(self, ctx, bet=None):
        """Starts a game of blackjack."""

        if str(ctx.message.channel.id) != str(Global.security.get("casino_channel")):
            return await self.bot.say("`this isn't the casino channel!`")

        if ctx.message.author.id in Global.bjgames:
            print("Already in blackjack")
            return

        if bet is None:
            return await self.bot.say("`please provide a bet!`")

        try:
            bet = round(float(bet), 2)
        except:
            return await self.bot.say("`invalid bet!`")

        if bet <= 0:
            return await self.bot.say("`bet must be positive!`")

        u = Global.money.get_user((ctx.message.author.id))
        balance = round(float(u["balance"]), 2)

        if bet > balance:
            return await self.bot.say("`you don't have enough money!`")

        bj = BlackJack(self.bot, ctx.message.author, bet)
        if bj.is_over() is False:
            Global.bjgames[ctx.message.author.id] = bj
            m = await self.bot.send_message(ctx.message.channel, embed=bj.create_embed())
            await self.bot.add_reaction(m, "▶")
            await self.bot.add_reaction(m, "⏹")
            #await self.bot.add_reaction(m, "⏩")
            #await self.bot.add_reaction(m, "🔀")
        else:
            winner = bj.who_won()
            bet = bj.bet

            u = Global.money.get_user(str(bj.user.id))
            balance = round(float(u["balance"]), 2)

            if winner == 1:
                if bet > balance:
                    Global.money.withdraw(str(bj.user.id), balance)
                    Global.money.deposit(self.bot.user.id, balance)
                else:
                    Global.money.withdraw(str(bj.user.id), bet)
                    Global.money.deposit(self.bot.user.id, bet)
            elif winner == 0:
                if bj.p.getHandvalue() == 21:
                    bet *= 2
                Global.money.withdraw(self.bot.user.id, bet)
                Global.money.deposit(str(bj.user.id), bet)

            new_embed = bj.create_embed(winEmbed=True)
            await self.bot.send_message(ctx.message.channel, embed=new_embed)


def setup(bot):
    bot.add_cog(CasinoCommands(bot))