from discord.ext import commands
import os
import discord
import traceback
import asyncio
import random

bot = commands.Bot(command_prefix='.', description='キーワードを検知するとログchにメンションします')
client = discord.Client()


token = os.environ['DISCORD_BOT_TOKEN']
inform_id = 653957662609768458 

@client.event
async def on_message(message):
	if message.content == "!delete":
	await message.delete()
	await message.channel.send( "削除しました" )
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
