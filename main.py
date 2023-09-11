import os
import re
from dotenv import load_dotenv
import discord
import segno


load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

options = {'fill_color': 'white', 'back_color': 'black', 'size': 1}


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$code'):
        data = message.content[5:]
        if not data:
            await message.channel.send("no data")

        if data:
            args = data.strip().split()
            scale = 5
            color = "#000000"
            if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', args[0]):
                color = args.pop(0)
            if len(args) >= 2 and re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', args[1]):
                color = args.pop(1)
            if len(args) >= 1 and args[0].isdecimal():
                scale = int(args.pop(0))
            txt = " ".join(args)

            qr = segno.make_qr(txt)
            qr.save("qr.png", scale=scale, dark=color)

            await message.channel.send(file=discord.File('qr.png'))


client.run(TOKEN)
