from discord.ext import commands
import os
import discord
import traceback
import asyncio
import random

bot = commands.Bot(command_prefix='.', description='キーワードを検知するとログchにメンションします')
client = discord.Client()


token = os.environ['DISCORD_BOT_TOKEN']
recruit_message = {}
lastest_recruit_data = {}
cache_limit = 300


@client.event
async def on_message(message):	
	if message.content.startswith("サブ垢"):
		channel = client.get_channel(653957662609768458)
		await channel.send("キーワード検知")
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')

async def startup():
	global bot
	await bot.login(token, bot=True)
	await bot.connect()
	bot.clear()

async def logout():
	global bot
	await bot.close()

loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(asyncio.gather(startup(), disconnect_timer()))
except KeyboardInterrupt:
	loop.run_until_complete(logout())
finally:
	loop.close()
bot.run(token)
