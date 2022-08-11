# bot.py

import os
import random
import csv
import numpy as np

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
async def create(ctx):
    prompts = (
        "What is the **TITLE** of the **HOST** message?",
        "What is the **DESCRIPTION** of the **HOST** message?",
        "Enter the **REACTION** to collect users:",
        "Enter the **TITLE** of the **PAIR** message:",
        "Enter the **DESCRIPTION** of the **PAIR** message:"
    )
    answers = []
    colours = (
        0xff0000,
        0xffa700,
        0xfff400,
        0xa3ff00,
        0x2cba00
    )
    msg_list = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    def config_fields(i_count, embed_):
        match i_count:
            case 0:
                return ""
            case 1:
                embed_.add_field(name="Host Message", value="Title: ✅️", inline=False)
            case 2:
                embed_.add_field(name="Host Message", value="Title: ✅️\nDescription: ✅️", inline=False)
            case 3:
                embed_.add_field(name="Host Message", value=f"Title: ✅️\nDescription: ✅️\nReaction: {answers[2]} ",
                                 inline=False)
            case 4:
                embed_.add_field(name="Host Message", value=f"Title: ✅️\nDescription: ✅️\nReaction: {answers[2]} ",
                                 inline=True)
                embed_.add_field(name="Pair Message", value=f"Title: ✅️", inline=True)

    for i, prompt in enumerate(prompts):
        print("Value of i: " + str(i))
        em = discord.Embed(
            title=f"Configuration - Step {i + 1} of 5",
            description=prompt,
            color=colours[i])
        em.set_author(name="Pear", url="https://github.com/kgatineau/pear_discord_bot",
                      icon_url=bot.user.avatar_url)
        config_fields(i, em)
        em.set_footer(text="Type the answer as a message and hit enter.")

        prompt_embed = await ctx.send(embed=em)
        msg_list.append(prompt_embed)
        msg = await bot.wait_for("message", check=check, timeout=None)
        msg_list.append(msg)
        answers.append(msg.content)

        print(answers)

    #  generates the embed to be sent as a response
    embed = discord.Embed(title=answers[0],
                          description=answers[1],
                          color=0xFF5733)
    embed.set_author(name="Pear", url="https://github.com/kgatineau/pear_discord_bot",
                  icon_url=bot.user.avatar_url)

    #  initializes the channel to send the message in
    channel = bot.get_channel(channel_id)

    #  sends the embed to the channel the command was triggered in
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(answers[2])

    for msg_ in msg_list:
        await msg_.delete()

    #  writes the ID of the message created to a .txt file for later use
    message = await channel.fetch_message(channel.last_message_id)
    with open('Pear/pear-bot/root_message.csv', 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(message.id)] + answers)


#  currently hard coded to an ID in a test server, will move these to the .env or .txt file next iteration
channel_id = 1007139879022506094


#  Command triggered via '!pair"
@bot.command()
@commands.has_permissions(administrator=True)
async def pair(ctx):
    import_data = []
    with open('pear-bot/root_message.csv', encoding='utf-8') as file_name:
        import_data = np.loadtxt(file_name, delimiter=",", dtype="str")

    message_id = int(import_data[0])

    print("IMPORT DATA: " + str(import_data))
    print("MESSAGE ID " + str(message_id))

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

    userslist = list(users)
    random.shuffle(userslist)

    if len(userslist) > 2:
        breakline = "\n"
        emoji = '\U0001F538'

        for _ in userslist:
            embed = discord.Embed(title=f"{import_data[4]}",
                                  description=f"{import_data[5]}\n"
                                              + f" {' '.join(user.mention + breakline if i % 2 != 0 else user.mention + emoji for i, user in enumerate(userslist))} ",
                                  color=0xFF5733)
            embed.set_author(name="Pairing with Pear!", url="https://github.com/kgatineau/pear_discord_bot",
                             icon_url=bot.user.avatar_url)
            embed.set_footer(text=f"Pear generated by: {ctx.author.display_name}")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{import_data[4]}",
                              description="No pairings available. Try again when more users react to the host "
                                          "message.\n",
                              color=0xFF5733)
        embed.set_author(name="Pear", url="https://github.com/kgatineau/pear_discord_bot",
                         icon_url=bot.user.avatar_url)
        embed.set_footer(text=f"Pear generated by: {ctx.author.display_name}")
        await ctx.send(embed=embed)


bot.run(TOKEN)
