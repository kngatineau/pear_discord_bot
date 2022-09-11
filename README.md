
# Pear - the Discord user pairing bot


## Introduction
As the community manager of a Discord group called the Femmes and Thems in Tech, I oversee, engage with and host events for thousands of spectacular women and nonbinary users who utilize our platform daily. Every week, it is my duty to manually pair individuals up who opt in to “break the ice” for those participating and allow for users to meet someone new every week. 

Pear is a tool that was not only created for the sake of a school project but serves as the first iteration of a solution to a real-life problem in our community. Manually pairing users worked on a small scale, but the process needed automation and the type of tool necessary to make this happen did not exist at the time of writing for the Discord platform.

Automating the pairing process using a Discord bot not only saves time for the moderation team, but it allows for accuracy and consistency for when pairings would be posted. 
While the bot will be originally utilized to pair people up for networking, it is intended to work as a pairing system for any scenario a Discord admin may deem necessary. Our goal is to create a versatile pairing bot that pairs users for any social/logistical need.

## Tools and Technology
### Programming Language(s) 
The programming language selected for this project is Python. I selected Python to not only meet the needs of the assignment criteria, but to add another programming language to my toolkit. I have created many Java projects and have a project using React JS I am completing in parallel to this one, so this project was a perfect opportunity to branch out and learn a language I have never used before.

### Software
PyCharm IDE 
The IDE selected for this project is PyCharm IDE by JetBrains. 

### IDE Plugins
Along with PyCharm IDE, I am utilizing a few plugins to help with development. They are as follows:
-	EnvFile
-	Highlight Bracket Pair
-	Git/GitHub/GitHub Desktop

### API
-	Discord.py 

## Testing Pear
I opted to structure the bot by pulling out the majority of the function code into a separate python file, bot_functions.py. This made unit testing a bit easier than relying on a mock "context" object to mimick the Discord environment. Unit tests are written to cover the functions in bot_functions.py only.

## Deployment
### Introduction
Deploying Pear to a personal server can be done in minutes. The code is hosted on GitHub for anyone to use and can be executed by anyone with a personal computer, Discord account and access to a server with Administrator privileges.

### Pear Requirements
Pear is designed to only function on the Discord platform, a social network consisting of servers where users gather to chat, network, play games and more.
This bot requires discord.py, a Python API for Discord. Should the API at any point no longer be available, the bot will need to be rewritten using an API that is. 

Pear requires a user to have a Discord account and have Administrator permissions to exist in a Discord. To execute a command using Pair, the user must have the “ban users” permissions designated to them via a role.

Since Pear is not hosted via a cloud server like many live bots are, it will need to be downloaded and recreated as a personal bot via the Discord developer portal. Instructions on how to do this can be found here.

After the bot creation, the user will need to enter the TOKEN data generated in the .env file provided in directory. This will replicate the Pear logic as your own bot. 

For Pear to function, the bot.py file must be running on your personal machine while commands are issued. This can be done by either executing the bot.py as a Python script, or by opening toe repository in an IDE and executing from there. 


## Conclusion
Learning something new is always a memorable experience but doing so while doing something you love makes it beyond enjoyable. This project gave me the opportunity to approach a solution to a real-world problem I faced at an angle I wouldn’t have otherwise. I am thankful for the things I have learned this semester and look forward to seeing what’s next for Pear.

## More Info
Check out [assignment-1](https://github.com/kngatineau/pear_discord_bot/blob/master/pear-assignment-1.pdf), [assignment-2](https://github.com/kngatineau/pear_discord_bot/blob/master/pear-assignment-2.pdf) and assignment-3 for further documentation on this application.


