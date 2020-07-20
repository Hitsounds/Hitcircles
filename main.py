import discord
from discord.ext import commands
import asyncio
import os
import random

client = commands.Bot(command_prefix=commands.when_mentioned_or(";"))

@client.event
async def on_ready():
	print("Bot is ready")
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

async def update_status_msg():
    await client.wait_until_ready()
    while not client.is_closed():
        status_messages = [discord.Game(name=i) for i in ["with hitsounds", "instead of doing work", "| gniyalP"]]
        await client.change_presence(activity=discord.Game(name=random.choice(status_messages)))
        await asyncio.sleep(900)


#Load extensions from ext folder
for ext in [i.replace('.py', '') for i in os.listdir("ext") if os.path.isfile(os.path.join("ext", i))]:
	try:
		client.load_extension(f"ext.{ext}")
	except Exception as e:
		print(f"Error in loading {ext}\n{e}")

client.loop.create_task(update_status_msg())
client.run(os.environ.get("DISCORD_TOKEN"))
