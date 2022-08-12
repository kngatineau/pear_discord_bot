# bot.py

import os
import random

import discord

from dotenv import load_dotenv
from discord.ext import commands
import pytest as pytest
import bot_functions

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

client = discord.Client()

bot = commands.Bot(command_prefix="!", intents=intents)
msg_list = []
userslist = []
answers = []


@bot.command()
@commands.has_permissions(administrator=True)
async def create(ctx):
    global msg_list, userslist, answers
    msg_list = []
    userslist = []
    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i, prompt in enumerate(bot_functions.prompts):
        print("Value of i: " + str(i))
        prompt_embed = await ctx.send(embed=bot_functions.create_prompt_embed(i, prompt, answers))
        msg_list.append(prompt_embed)
        msg = await bot.wait_for("message", check=check, timeout=None)
        msg_list.append(msg)
        answers.append(msg.content)

        print(answers)
    channel = bot.get_channel(channel_id)
    msg = await ctx.send(embed=bot_functions.create_prompt_embed(6, "", answers))
    await msg.add_reaction(answers[2])

    message = await channel.fetch_message(channel.last_message_id)
    bot_functions.export_data(message, answers)
    for msg_ in msg_list:
        await msg_.delete()



channel_id = 1007126677568110653


@bot.command()
@commands.has_permissions(administrator=True)
async def pair(ctx):
    global msg_list
    msg_list = []
    msg_list = bot_functions.import_data()
    print("MSG:" + str(msg_list))
    message_id = int(msg_list[0])
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(str(message_id))

    users = set()

    for reaction in message.reactions:

        async for user in reaction.users():
            guild = bot.get_guild(976502346878177290)

            if guild.get_member(user.id) is None:
                await reaction.remove(user)

            else:
                if user.id != 949802757483810917:
                    users.add(user)

    global userslist
    userslist = list(users)
    random.shuffle(userslist)
    print("Length of userlist: " + str(len(userslist)))

    await ctx.send(embed=bot_functions.set_pair_embed(ctx, userslist, msg_list))


bot.run(TOKEN)
