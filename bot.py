# bot.py
import os
import random

import discord
# from discord.ext.commands import bot

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@bot.command()
async def create(ctx, title, description):
    embed = discord.Embed(title=title,
                          description=description,
                          color=0xFF5733)
    channel = bot.get_channel(channel_id)

    await ctx.send(embed=embed)
    message = await channel.fetch_message(channel.last_message_id)
    with open('root_message.txt', 'w') as f:
        f.write(str(message.id))


channel_id = 976502346878177293  # Replace with channel id


#  message_id = 984196833792364594  # Note these are ints, not strings


@bot.command()
async def pair(ctx):
    channel = bot.get_channel(channel_id)
    with open('root_message.txt') as r:
        message_id = int(r.read())
    message = await channel.fetch_message(message_id)
    users = set()
    guild = bot.get_guild(976502346878177290)

    for reaction in message.reactions:
        async for user in reaction.users():
            if guild.get_member(user.id) is None:
                await reaction.remove(user)
            else:
                users.add(user)

    userslist = list(users)
    random.shuffle(userslist)
    breakline = "\n"
    emoji = '\U0001F538'

    for user in userslist:
        embed = discord.Embed(title="Coffee Chat Pairings",
                              description=f"Pairings for this week are:\n"
                                          + f" {' '.join(user.mention + breakline if i % 2 != 0 else user.mention + emoji for i, user in enumerate(userslist))} ",
                              color=0xFF5733)


    await ctx.send(embed=embed)


bot.run(TOKEN)
