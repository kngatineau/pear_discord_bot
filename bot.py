# bot.py

import os
import random

import discord

from dotenv import load_dotenv
from discord.ext import commands

#  Loads the token data from the .env file and sets the 'TOKEN' variable
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#  Intents required to retrieve member data as per the Discord API update
intents = discord.Intents.default()
intents.members = True

#  sets the 'bot' and 'client' variables and prefix to trigger the bot to '!'
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client()


#  event that launches automatically when the bot runs/connects
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


#  Command triggered via '!create'
@bot.command()
@commands.has_permissions(administrator=True)
async def create(ctx, title, description, emoji):
    #  generates the embed to be sent as a response
    embed = discord.Embed(title=title,
                          description=description,
                          color=0xFF5733)

    #  initializes the channel to send the message in
    channel = bot.get_channel(channel_id)

    #  sends the embed to the channel the command was triggered in
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(emoji)

    print(str(emoji))

    #  writes the ID of the message created to a .txt file for later use
    message = await channel.fetch_message(channel.last_message_id)
    with open('root_message.txt', 'w', encoding="utf-8") as f:
        f.write(str(message.id))
        f.write("\n" + str(emoji))


#  currently hard coded to an ID in a test server, will move these to the .env or .txt file next iteration
channel_id = 976502346878177293


#  Command triggered via '!pair"
@bot.command()
@commands.has_permissions(administrator=True)
async def pair(ctx):
    #  opens the .txt file and reads the message ID of the reaction host post
    with open('root_message.txt') as r:
        message_id = int(r.readline())
        reaction_emoji = str(r.readline())
    print("Reaction emoji:" + reaction_emoji)
    #  sets the respective variables
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)

    #  sets an empty array to be filled with users
    users = set()

    #  await message.add_reaction(emoji)

    #  loops over the reactions on the specified post
    for reaction in message.reactions:

        #  loops over the users for each reaction
        async for user in reaction.users():
            guild = bot.get_guild(976502346878177290)

            if guild.get_member(user.id) is None:
                #  deletes a user if they no longer are a part of the server
                await reaction.remove(user)

            else:
                #  otherwise, adds them to the list
                if user.id != 949802757483810917:
                    users.add(user)

    #  copies the value of the list 'users' too 'userslist' so it can be shuffled, then shuffles the list
    userslist = list(users)
    random.shuffle(userslist)

    #  loops over the shuffled list of users
    if len(userslist) > 2:
        #  variables set as these values cannot be added directly to f string statements
        breakline = "\n"
        emoji = '\U0001F538'

        for _ in userslist:
            #  adds the list values to the 'pair' embed
            embed = discord.Embed(title="Coffee Chat Pairings",
                                  description=f"Pairings for this week are:\n"
                                              + f" {' '.join(user.mention + breakline if i % 2 != 0 else user.mention + emoji for i, user in enumerate(userslist))} ",
                                  color=0xFF5733)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Coffee Chat Pairings",
                              description="No pairings available.",
                              color=0xFF5733)
        await ctx.send(embed=embed)

    #  sends the embed
    #  await ctx.send(embed=embed)


bot.run(TOKEN)
