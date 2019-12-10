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
	
	if message.author.bot:
        return
    	if message.content.startswith("サブ垢"):
	channel = client.get_channel(653957662609768458)
        await channel.send("キーワード検知")
	
	
    	


bot.run(token)
