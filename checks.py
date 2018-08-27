import discord
from discord.ext import commands

from globals import *

admins = {'167797932156911616': True, '408062249324773387': True}

def is_admin():
    def predicate(ctx):
        return admins.get(ctx.message.author.id, False)
    return commands.check(predicate)

def is_mod():
    def predicate(ctx):
        mod_role = discord.utils.get(ctx.message.server.roles, id=str(sec.get("mod_role")))
        return admins.get(ctx.message.author.id, False) or mod_role in ctx.message.author.roles
    return commands.check(predicate)