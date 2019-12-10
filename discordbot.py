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
text_id = {}
inform_id = 653957662609768458 

@client.event
async def on_message(message):
	if message.content == 'test123':
		if message.channel.id == text_id:
			inform_channel = [channel for channel in client.get_all_channels() if channel.id == inform_id][0] 
			await client.send_message(inform_channel, "キーワード検知")
		else:
			print('success')
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
