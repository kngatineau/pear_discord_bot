import discord


def pair_logic(userslist):
    pair = ""
    for i, user in enumerate(userslist):
        if len(userslist) % 2 == 0:  # if user amount is even
            if i % 2 != 0:
                pair = pair + user.mention if i != len(userslist) - 1 else pair + user.mention + "\n"
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
def set_pair_embed(userslist, msg_list):
    br = "\n"
    if len(userslist) > 2:
        pair_title = f"{msg_list[4]}"
        pair_desc = f"{br + pair_logic(userslist) + br + msg_list[5]} "

    else:
        pair_title = msg_list[4] + "\n"
        pair_desc = "No pairings available. Try again when more users react to the host message."

    embed = discord.Embed(title=pair_title,
                          description=pair_desc,
                          color=0xFF5733)
    embed.set_author(name="Pear", url="https://github.com/kgatineau/pear_discord_bot",
                     icon_url="https://i.ibb.co/2y03dJ5/Pngtree-meb-style-yellow-cute-pear-5867760-1.png")

    return embed
