# bot.py

import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

import config_embed
import csv_controller
import pair_embed

#  sensitive values imported from .env
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
users_list = []
answers = []


#  "!create" command logic
@bot.command()
@commands.has_permissions(ban_members=True)
async def create(ctx):
    global msg_list, users_list, answers
    msg_list = []
    users_list = []
    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i, prompt in enumerate(config_embed.prompts):
        prompt_embed = await ctx.send(embed=config_embed.create_prompt_embed(i, prompt, answers))
        msg_list.append(prompt_embed)
        msg = await bot.wait_for("message", check=check, timeout=None)
        msg_list.append(msg)
        answers.append(msg.content)

    channel = bot.get_channel(int(CHANNEL_ID))
    msg = await ctx.send(embed=config_embed.create_prompt_embed(6, "", answers))
    await msg.add_reaction(answers[2])  # adds reaction to the host message

    message = await channel.fetch_message(channel.last_message_id)
    csv_controller.export_data(message, answers)
    for msg_ in msg_list:
        await msg_.delete()  # deletes config loop messages


#  !pair command logic
@bot.command()
@commands.has_permissions(ban_members=True)
async def pair(ctx):
    global msg_list
    msg_list = []
    msg_list = csv_controller.import_data()
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

    global users_list
    users_list = list(users)
    random.shuffle(users_list)

    await ctx.send(msg_list[4] + "\n", embed=pair_embed.set_pair_embed(users_list, msg_list))


bot.run(TOKEN)
