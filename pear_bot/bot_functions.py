#  bot_functions.py
import os

import discord
import pandas as pd
from dotenv import load_dotenv

import csv

#  for use of 'mentioning' channel in embed. not necessary if you are not planning to mention any channels.
load_dotenv()
MENTION_CHANNEL_ID = os.getenv('MENTION_CHANNEL_ID')

prompts = (
    "What is the **TITLE** of the **HOST** message?",
    "What is the **DESCRIPTION** of the **HOST** message?",
    "Enter the **REACTION** to collect users:",
    "Enter the **TITLE** of the **PAIR** message:",
    "Enter the **DESCRIPTION** of the **PAIR** message:"
)


def pair_logic(userslist):
    pair = ""
    for i, user in enumerate(userslist):
        if len(userslist) % 2 == 0:  # if user amount is even
            if i % 2 != 0:
                if i != len(userslist) - 1:
                    pair += user.mention
                else:
                    pair += user.mention + "\n"
            else:
                pair += "\n" + user.mention + '\U0001F538'

        else:  # if user amount is odd
            if i < len(userslist) - 1:
                if i % 2 != 0:
                    pair += user.mention
                else:
                    pair += "\n" + user.mention + '\U0001F538'
            if i == len(userslist) - 1:
                pair += '\U0001F538' + user.mention + "\n"
    return pair


#  sets the embed for the !pair command, prints paired users if more than two real users clicked the reaction
#  remove the MENTION_CHANNEL_ID portion in parentheses on line 52 if no channels are being mentioned
def set_pair_embed(userslist, msg_list):
    br = "\n"
    if len(userslist) > 2:
        pair_title = f"{msg_list[4]}"
        pair_desc = f"{br + msg_list[5] + ('<#' + MENTION_CHANNEL_ID + '>' + '.')} "

    else:
        pair_title = msg_list[4] + "\n"
        pair_desc = "No pairings available. Try again when more users react to the host message."

    embed = discord.Embed(title=pair_title,
                          description=f"{pair_desc}",
                          color=0xFF5733)
    embed.set_author(name="Pear", url="https://github.com/kgatineau/pear_discord_bot",
                     icon_url="https://i.ibb.co/2y03dJ5/Pngtree-meb-style-yellow-cute-pear-5867760-1.png")

    return embed


#  exports the data to a CSV to be retrieved later by the !pair command
def export_data(message, answers):
    with open('root_message.csv', 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(message.id)] + answers)


#  parse the data from CSV to a list
def import_data():
    list_msg = pd.read_csv(r'root_message.csv')
    msg_list = list(list_msg)
    return msg_list


#  creates the embed for each iteration of the configuration loop
def create_prompt_embed(i, prompt, answers):
    colours = (
        0xff0000,
        0xffa700,
        0xfff400,
        0xa3ff00,
        0x2cba00
    )

    if len(answers) < 5:
        prompt_t = f"Configuration - Step {i + 1} of 5"
        prompt_d = prompt
        colour = colours[i]
    else:
        prompt_t = answers[0]
        prompt_d = answers[1]
        colour = 0x2cba00

    em = discord.Embed(
        title=prompt_t,
        description=prompt_d,
        color=colour)
    em.set_author(name="Pear", url="https://github.com/kgatineau/pear_discord_bot",
                  icon_url="")
    config_fields(i, em, answers)
    em.set_footer(text="Pear - the Discord User Pairing Bot")
    return em


#  determines the number of added fields the prompt embed object sent gets pending on the value of the loop counter
def config_fields(i_count, embed_, answers):
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
