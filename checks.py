import discord
from discord.ext import commands

from globals import *

admins = {'498438002054266880': True, '408062249324773387': True}

def is_admin():
    def predicate(ctx):
        return admins.get(ctx.message.author.id, False)
    return commands.check(predicate)

def is_mod():
    def predicate(ctx):
        mod_role = discord.utils.get(ctx.message.server.roles, id=str(Global.security.get("mod_role")))
        return admins.get(ctx.message.author.id, False) or mod_role in ctx.message.author.roles
    return commands.check(predicate)

def is_brodgod():
    def predicate(ctx):
        brodgod_role = discord.utils.get(ctx.message.server.roles, id=str(Global.security.get("brodgod_role")))
        mod_role = discord.utils.get(ctx.message.server.roles, id=str(Global.security.get("mod_role")))
        return admins.get(ctx.message.author.id, False) or (brodgod_role in ctx.message.author.roles) or (mod_role in ctx.message.author.roles)
    return commands.check(predicate)