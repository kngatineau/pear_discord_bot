import os

import discord

prompts = (
    "What is the **TITLE** of the **HOST** message?",
    "What is the **DESCRIPTION** of the **HOST** message?",
    "Enter the **REACTION** to collect users:",
    "Enter the **TITLE** of the **PAIR** message:",
    "Enter the **DESCRIPTION** of the **PAIR** message:"
)


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
