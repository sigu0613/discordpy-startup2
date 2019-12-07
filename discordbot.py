from discord.ext import commands
import os
import discord
import traceback
import asyncio
import random

bot = commands.Bot(command_prefix='.', description='自動でチーム募集をするBOTです')
client = discord.Client()


token = os.environ['DISCORD_BOT_TOKEN']
recruit_message = {}
lastest_recruit_data = {}
cache_limit = 300

@bot.event
async def on_reaction_add(reaction, user):
	message = reaction.message
	if(message.id in recruit_message and not user.bot):
		emj = str(reaction.emoji)
		await message.remove_reaction(emj, user)
		isFull = False
		if(emj == "⬆️" and user.id != recruit_message[message.id]["writer_id"]):
			if(recruit_message[message.id]["max_user"] == -1 or len(recruit_message[message.id]["users"]) < recruit_message[message.id]["max_user"]):
				if(user.id not in recruit_message[message.id]["users"]):
					recruit_message[message.id]["users"].append(user.id)
			if(recruit_message[message.id]["max_user"] != -1 and len(recruit_message[message.id]["users"]) >= recruit_message[message.id]["max_user"]):
				isFull = True
		elif(emj == "⬇️" and user.id != recruit_message[message.id]["writer_id"] and user.id in recruit_message[message.id]["users"]):
			recruit_message[message.id]["users"].remove(user.id)
		elif(emj == "✖" and user.id == recruit_message[message.id]["writer_id"]):
			isFull = True

		users_str = "{}".format(message.guild.get_member(recruit_message[message.id]["writer_id"]).name)
		if(message.guild.get_member(recruit_message[message.id]["writer_id"]).nick != None):
			users_str = "{}".format(message.guild.get_member(recruit_message[message.id]["writer_id"]).nick)
		
		if(isFull):
			users = recruit_message[message.id]["users"]
			lottery_user = recruit_message[message.id]["lottery_user"]
			title = recruit_message[message.id]["title"]
			room = recruit_message[message.id]["room"]
			writer_id = recruit_message[message.id]["writer_id"]
			del recruit_message[message.id]
			if(lottery_user != -1 and len(users) >= lottery_user):
				users = random.sample(users, lottery_user)
			full_users = users + [writer_id]
			for user_id in users:
				if(bot.get_user(user_id) != None):
					if(message.guild.get_member(user_id).nick != None):
						users_str += "\n{}".format(message.guild.get_member(user_id).nick)
					else:
						users_str += "\n{}".format(message.guild.get_member(user_id).name)
			users_str.rstrip()

			for user_id in users:
				if(bot.get_user(user_id) != None):
					if(user_id not in lastest_recruit_data and len(lastest_recruit_data) >= cache_limit):
						del lastest_recruit_data[lastest_recruit_data.keys()[0]]
					lastest_recruit_data[user_id] = { "title" : title, "users" : full_users }
					if(room != "-1"):
						await message.guild.get_member(user_id).send("{}の部屋番号は　{}　です".format(title, room))
			if(writer_id not in lastest_recruit_data and len(lastest_recruit_data) >= cache_limit):
				del lastest_recruit_data[lastest_recruit_data.keys()[0]]
			lastest_recruit_data[writer_id] = { "title" : title, "users" : full_users }
			await message.edit(content = (title + "　募集終了\n```\n{} ```".format(users_str)))
			await message.remove_reaction("⬆️", bot.user)
			await message.remove_reaction("⬇️", bot.user)
			await message.remove_reaction("✖", bot.user)
		else:
			for user_id in recruit_message[message.id]["users"]:
				if(bot.get_user(user_id) != None):
					if(message.guild.get_member(user_id).nick != None):
						users_str += "\n{}".format(message.guild.get_member(user_id).nick)
					else:
						users_str += "\n{}".format(message.guild.get_member(user_id).name)
				else:
					recruit_message[message.id]["users"].remove(user_id)
			users_str.rstrip()
			rec_text = "募集中！"
			if(recruit_message[message.id]["lottery_user"] != -1):
				rec_text = "募集中！(抽選 {}人->{}人)".format(recruit_message[message.id]["max_user"], recruit_message[message.id]["lottery_user"])
			await message.edit(content = (recruit_message[message.id]["title"] + "　{rec_text} ＠{count}人(↑で参加 ↓で退出)\n```\n{str} ```".format(rec_text = rec_text, count = recruit_message[message.id]["max_user"] - len(recruit_message[message.id]["users"]), str = users_str)))
			recruit_message[message.id]["raw_message"] = message

@bot.command()
async def r_test(ctx, room_id = "-1"):
	sender_id = ctx.message.author.id
	if(sender_id in lastest_recruit_data):
		title = lastest_recruit_data[sender_id]["title"]
		users = lastest_recruit_data[sender_id]["users"]
		notify_txt = ""
		for user_id in users:
			notify_txt += ctx.message.guild.get_member(user_id).mention + " "
			if(user_id != sender_id):
				await ctx.message.guild.get_member(user_id).send("{}の新しい部屋番号は　{}　です".format(title, room_id))
		await ctx.send(notify_txt + "新しい部屋番号を送信しました")
		await ctx.message.delete()
	elif(bot.get_user(sender_id) != None):
		await ctx.send("{} 最後に参加した部屋が存在しないか、古すぎます。".format(bot.get_user(sender_id).mention))
		await ctx.message.delete()
		
@bot.command()
async def s_test(ctx, room_id = "-1", title = "", max_user = 2, remain_time = 300):
	users_str = "{}".format(ctx.message.author.name)
	if(ctx.message.author.nick != None):
		users_str = "{}".format(ctx.message.author.nick)
	users_str.rstrip("")
	mes = await ctx.send(title + "　募集中！　＠{count}人(↑で参加 ↓で退出)\n```\n{str} ```".format(count = max_user, str = users_str))
	recruit_message[mes.id] = { "room" : room_id, "time" : remain_time, "max_user" : max_user, "writer_id" : ctx.message.author.id, "title" : title, "users" : [], "raw_message" : mes, "lottery_user" : -1 }
	await ctx.message.delete()
	await mes.add_reaction("⬆️")
	await mes.add_reaction("⬇️")
	await mes.add_reaction("✖")
	
@bot.command()
async def l_test(ctx, room_id = "-1", title = "", max_user = 5, lottery_user = 2, remain_time = 300):
	users_str = "{}".format(ctx.message.author.name)
	if(ctx.message.author.nick != None):
		users_str = "{}".format(ctx.message.author.nick)
	users_str.rstrip("")
	mes = await ctx.send(title + "　募集中！(抽選 {max_user}人->{lottery_user}人)　＠{count}人(↑で参加 ↓で退出)\n```\n{str} ```".format(max_user = max_user, lottery_user = lottery_user, count = max_user, str = users_str))
	recruit_message[mes.id] = { "room" : room_id, "time" : 300, "max_user" : max_user, "writer_id" : ctx.message.author.id, "title" : title, "users" : [], "raw_message" : mes, "lottery_user" : lottery_user }
	await ctx.message.delete()
	await mes.add_reaction("⬆️")
	await mes.add_reaction("⬇️")
	await mes.add_reaction("✖")
	

@bot.command()
async def s1_test(ctx, room_id = "-1", title = ""):
	users_str = "{}".format(ctx.message.author.name)
	if(ctx.message.author.nick != None):
		users_str = "{}".format(ctx.message.author.nick)
	users_str.rstrip("")
	mes = await ctx.send(title + "　募集中！　＠{count}人(↑で参加 ↓で退出)\n```\n{str} ```".format(count = 1, str = users_str))
	recruit_message[mes.id] = { "room" : room_id, "time" : 300, "max_user" : 1, "writer_id" : ctx.message.author.id, "title" : title, "users" : [], "raw_message" : mes, "lottery_user" : -1 }
	await ctx.message.delete()
	await mes.add_reaction("⬆️")
	await mes.add_reaction("⬇️")
	await mes.add_reaction("✖")
	

async def disconnect_timer():
	while True:
		for mes_key in list(recruit_message.keys()):
			if(mes_key in recruit_message):
				mes = recruit_message[mes_key]["raw_message"]
				recruit_message[mes_key]["time"] = recruit_message[mes_key]["time"] - 1
				if(recruit_message[mes_key]["time"] <= 0):
					users = recruit_message[mes_key]["users"]
					title = recruit_message[mes_key]["title"]
					room = recruit_message[mes_key]["room"]
					writer_id = recruit_message[mes_key]["writer_id"]
					lottery_user = recruit_message[mes_key]["lottery_user"]
					if(lottery_user != -1 and len(users) >= lottery_user):
						users = random.sample(users, lottery_user)
					full_users = users + [writer_id]
					del recruit_message[mes_key]
					users_str = "{}".format(mes.guild.get_member(writer_id).name)
					if(mes.guild.get_member(writer_id).nick != None):
						users_str = "{}".format(mes.guild.get_member(writer_id).nick)
					for user_id in users:
						if(bot.get_user(user_id) != None):
							if(user_id not in lastest_recruit_data and len(lastest_recruit_data) >= cache_limit):
								del lastest_recruit_data[lastest_recruit_data.keys()[0]]
							lastest_recruit_data[user_id] = { "title" : title, "users" : full_users }
							if(room != "-1"):
								await mes.guild.get_member(user_id).send("{}の部屋番号は　{}　です".format(title, room))
							if(mes.guild.get_member(user_id).nick != None):
								users_str += "\n{}".format(mes.guild.get_member(user_id).nick)
							else:
								users_str += "\n{}".format(mes.guild.get_member(user_id).name)
						else:
							users.remove(user_id)
					users_str.rstrip()
					if(writer_id not in lastest_recruit_data and len(lastest_recruit_data) >= cache_limit):
						del lastest_recruit_data[lastest_recruit_data.keys()[0]]
					lastest_recruit_data[writer_id] = { "title" : title, "users" : full_users }
					await mes.edit(content = (title + "　募集終了\n```\n{} ```".format(users_str)))
					await mes.remove_reaction("⬆️", bot.user)
					await mes.remove_reaction("⬇️", bot.user)
					await mes.remove_reaction("✖", bot.user)
		await asyncio.sleep(1)

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
