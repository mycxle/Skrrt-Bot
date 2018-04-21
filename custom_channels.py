import asyncio

bot_id = "430603176463564810"

async def single_word_channel(message, client, word):
    if message.content != word and message.author.id != bot_id:
        await client.delete_message(message)
        msg = await client.send_message(message.channel, message.author.mention + ' the only word allowed on this channel is "' + word + '"')
        await asyncio.sleep(3)
        await client.delete_message(msg)
    elif message.content == word:
        sec = False
        async for m in client.logs_from(message.channel, limit=2):
            if sec:
                if message.author == m.author:
                    await client.delete_message(message)
                    msg = await client.send_message(message.channel, message.author.mention + ' don\'t say "' + word + '" twice in a row, give someone else a turn!')
                    await asyncio.sleep(3)
                    await client.delete_message(msg)
            sec = True

async def hi_channel(message, client):
    await single_word_channel(message, client, "hi")

async def lol_channel(message, client):
    await single_word_channel(message, client, "lol")

async def rip_channel(message, client):
    await single_word_channel(message, client, "rip")

async def counting_channel(message, client):
    sec = False
    async for m in client.logs_from(message.channel, limit=2):
        if sec and message.author.id != bot_id:
            if message.author.id == m.author.id:
                await client.delete_message(message)
                msg = await client.send_message(message.channel, message.author.mention + ' you cannot send multiple messages. give someone else a turn!')
                await asyncio.sleep(3)
                await client.delete_message(msg)
            else:
                try:
                    if int(message.content) != int(m.content) + 1:
                        await client.delete_message(message)
                        msg = await client.send_message(message.channel, message.author.mention + ' that\'s the wrong number dummy!')
                        await asyncio.sleep(3)
                        await client.delete_message(msg)
                except:
                    await client.delete_message(message)
                    msg = await client.send_message(message.channel, message.author.mention + ' that\'s not a number dummy!')
                    await asyncio.sleep(3)
                    await client.delete_message(msg)
        sec = True