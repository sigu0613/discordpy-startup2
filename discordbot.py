from discord.ext import commands
import os
import discord
import traceback
import asyncio
import random


bot = commands.Bot(command_prefix='.', description='検索')
client = discord.Client()
token = os.environ['DISCORD_BOT_TOKEN']

messageId = 657753236606025729


@client.event
async def on_message(message):
	if message.content.startswith('!test123'):
		print('反応')
		message = await client.get_channel.fetch_message(messageId)
		await message.channel.send(test)

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

bot.run(token)
