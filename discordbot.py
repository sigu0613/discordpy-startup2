from discord.ext import commands
import os
import discord
import traceback
import asyncio
import random
from googlesearch import search

bot = commands.Bot(command_prefix='.', description='検索')
client = discord.Client()

ModeFlag = 0
token = os.environ['DISCORD_BOT_TOKEN']

@client.event
async def on_message(message):
	if message.author.bot:
		return
	if ModeFlag == 1:
		kensaku = message.content
		ModeFlag = 0
		count = 0
		# 日本語で検索した上位5件を順番に表示
		for url in search(kensaku, lang="jp",num = 2):
			await message.channel.send(url)
			count += 1
			if(count == 2):
				break
	# google検索モードへの切り替え
	if message.content == '!google':
		ModeFlag = 1
		await message.channel.send('検索するワードをチャットで発言してね')

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
