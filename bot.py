# bot.py
import os
import random

import discord
# from discord.ext.commands import bot
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

bot = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@bot.command()
async def create(ctx, title, description):
    embed = discord.Embed(title=title,
                          description=description,
                          color=0xFF5733)
    await ctx.send(embed=embed)


channel_id = 976502346878177293  # Replace with channel id
message_id = 984196833792364594  # Note these are ints, not strings


@bot.command()
async def pair(ctx):
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    users = set()
    print("TEST1")
    for reaction in message.reactions:
        async for user in reaction.users():
            users.add(user)
    userslist = list(users)
    random.shuffle(userslist)

    print(users)
    breakline = "\n"
    emoji = '\U0001F538'
    for user in userslist:
        embed = discord.Embed(title="Coffee Chat Pairings",
                              description=f"Pairings for this week are:\n"
                                          + f" {' '.join(user.mention + breakline if i % 2 != 0 else user.mention + emoji for i, user in enumerate(userslist)  ) } ",
                              color=0xFF5733)
        print("TEST")

    await ctx.send(embed=embed)


bot.run(TOKEN)
