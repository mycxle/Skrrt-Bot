from helpers import *
from admin_commands import *
from commands import *
from custom_channels import *
import os
from datetime import datetime

client = discord.Client()

prefix = ">"
game = "with big goth tiddies"

admin_commands = {
	"say": say_command,
	"kick": kick_command,
	"warn": warn_command,
	"ban": ban_command,
	"softban": softban_command,
	"unban": unban_command,
	"unbanall": unbanall_command,
	"member": member_command,
	"normie": normie_command,
	"game": game_command,
	"purge": purge_command,
	"mute": mute_command,
	"unmute": unmute_command,
	"mutelist": mutelist_command,
	"wipe": wipe_command,
	"idlist": list_ids_command,
	"headcount": headcount_command,
	"bancount": bancount_command,
	"eval": evaluation_command,
	"coin": coin_command,
	"userinfo": userinfo_command,
	"poll": poll_command
}

commands = {

}

custom_channels = {
	"392158484176830464": hi_channel,
	"392461625640222720": lol_channel,
	"392803097296240642": rip_channel,
	"424697496565055499": counting_channel
}

async def call_command(message, commandDictionary):
	cmd = message.content.split()[0][1:]
	if cmd in commandDictionary:
		await commandDictionary[cmd](message, client)

async def call_custom_channel(message):
	if message.channel.id in custom_channels:
		await custom_channels[message.channel.id](message, client)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	await client.change_presence(game=discord.Game(name=game))

@client.event
async def on_message(message):
	await call_custom_channel(message)

	if message.content.lower().startswith(prefix):
		await call_command(message, commands)
		if is_admin(message.author.id):
			await call_command(message, admin_commands)

@client.event
async def on_member_join(member):
	created = datetime_from_utc_to_local(member.created_at)
	current = datetime.now()
	diff = current - created
	days, seconds = diff.days, diff.seconds
	hours = days * 24 + seconds // 3600
	minutes = (seconds % 3600) // 60
	seconds = seconds % 60
	print("Account is " + str(hours) + " old.")
	if hours <= 72:
		print("BAN THIS FUCKER")

	print("MEMBER JOINED")
	e = discord.Embed()
	e.set_thumbnail(url=member.avatar_url)
	e.title="Welcome to Skrrt Gang!"
	e.description=member.mention + " be sure to read " + member.server.get_channel("428692044568068096").mention
	e.colour=discord.Color.red()
	message = await client.send_message(member.server.get_channel("437332997235146775"), embed=e)
	'''for x in client.get_all_emojis():
		print(x.name + " | " + x.id)
		if x.id == "430626791950909440":
			await client.add_reaction(message, x)

	await client.add_reaction(message, "🇭")
	await client.add_reaction(message, "🇮")

	for x in client.get_all_emojis():
		print(x.name + " | " + x.id)
		if x.id == "430626845726343168":
			await client.add_reaction(message, x)'''

@client.event
async def on_member_remove(member):
	await client.send_message(member.server.get_channel("437332997235146775"), "**OOF! " + member.name + "#" + str(member.discriminator) + " just left the gang.. **😢")

token = os.environ['BOT_TOKEN']
client.run(token)