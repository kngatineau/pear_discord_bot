# bot.py

import os
import random

import discord

from dotenv import load_dotenv
from discord.ext import commands
import bot_functions

#  sensitive values stored in .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
GUILD_ID = os.getenv('GUILD_ID')
BOT_USER_ID = os.getenv('BOT_USER_ID')


intents = discord.Intents.default()
intents.members = True

client = discord.Client()

bot = commands.Bot(command_prefix="!", intents=intents)
msg_list = []
userslist = []
answers = []
misconduct_channel = bot.get_channel(1007894151263690762)

#  "!create" command logic
@bot.command()
@commands.has_permissions(ban_members=True)
async def create(ctx):
    global msg_list, userslist, answers
    msg_list = []
    userslist = []
    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i, prompt in enumerate(bot_functions.prompts):
        prompt_embed = await ctx.send(embed=bot_functions.create_prompt_embed(i, prompt, answers))
        msg_list.append(prompt_embed)
        msg = await bot.wait_for("message", check=check, timeout=None)
        msg_list.append(msg)
        answers.append(msg.content)

    channel = bot.get_channel(int(CHANNEL_ID))
    msg = await ctx.send(embed=bot_functions.create_prompt_embed(6, "", answers))
    await msg.add_reaction(answers[2])  # adds reaction to the host message

    message = await channel.fetch_message(channel.last_message_id)
    bot_functions.export_data(message, answers)
    for msg_ in msg_list:
        await msg_.delete()  # deletes config loop messages


#  !pair command logic
@bot.command()
@commands.has_permissions(ban_members=True)
async def pair(ctx):
    global msg_list
    msg_list = []
    msg_list = bot_functions.import_data()
    message_id = int(msg_list[0])
    channel = bot.get_channel(int(CHANNEL_ID))
    message = await channel.fetch_message(str(message_id))

    users = set()

    for reaction in message.reactions:
        async for user in reaction.users():
            guild = bot.get_guild(int(GUILD_ID))

            if guild.get_member(user.id) is None:
                await reaction.remove(user)  # removes reaction of user no longer in guild

            else:
                if user.id != int(BOT_USER_ID):
                    users.add(user)  # otherwise add user to list to be paired

    global userslist
    userslist = list(users)
    random.shuffle(userslist)

    await ctx.send(embed=bot_functions.set_pair_embed(ctx, userslist, msg_list))


bot.run(TOKEN)
