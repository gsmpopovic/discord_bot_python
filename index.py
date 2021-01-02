# Import mpdules
import os
import discord
import requests
import json
import random
import asyncio
#from replit import db
########################################################################
#Load env variables
#DISCORD_TOKEN
#GUILD_NAME
#CLIENT_ID
#PUBLIC_KEY
#CLIENT_SECRET

#Store token in a variable
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_NAME')

#Variable declarations 
sad_words = [
    "Unhappy",
    "Sad",
    "Blue"
]

starter_encouragements  = [
    "Don't be sad!", 
    "It's okay!"
]

#Create an instance of our discord client
# A Client is an object that represents a connection to Discord. 
# A Client handles events, tracks state,
# and generally interacts with Discord APIs.
client = discord.Client()

########################################################################

#Function declarations

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_response = json.loads(response.text) 
    quote = ' Quote: ' + json_response[0]['q'] + ' - ' + json_response[0]['a']
    return quote

# greet_user greets user by name. 
# Takes as an argument 
# message.author.name (name of message sender)

def greet_user(name):
    greeting = "Oh, hi there " + name + "!"
    return greeting

def update_commands(command):
    if "commands" in db.keys():
        commands = db["commands"]
        commands.append(command)
        db["commands"] = commands
    else:
        db["commands"] = ["commands"]
    
def delete_commands(index):
    commands = db["commands"]
    if len(commands) > index:
        del commands[index]
    commands = db["commands"]
########################################################################
########################################################################

# @client.event
# async def on_ready():
#     # on_ready event handler
#     #  handles the event when the Client has established a connection to Discord 
#     #  and it has finished preparing the data that Discord has sent, 
#     #  such as login state, guild and channel data, and more.

@client.event 
async def on_ready():
    print(f"{client.user} has logged in!")

@client.event
async def on_message(message):

    msg = message.content

    if message.author == client.user:
        return

    elif msg.startswith("/"):

        commands = {
                "/greet":"Greet user by name.",
                "/delete":"Delete all messages in current channel.",
                "$inspire":"See an inspirational quote." 
            }

        options = commands

        if "commands" in db.keys():

            options = options + db["commands"]

        if any(command in msg for command in commands):
            await message.channel.send(random.choice(options))

        if msg.startswith("/new"):
            new_command = msg.split("/new ", 1)[1]
            update_commands(new_command)
            await message.channel.send("New command was created!")

        if msg == "/greet":
            name = message.author.name
            greeting = greet_user(name)
            await message.channel.send(greeting)
        
        elif msg == "/list":           
            for command, description in commands.items():
                await message.channel.send(f"Command: {command}" + "\n" f"Description: {description}")


        elif msg == "/delete":
            await message.channel.send("Clearing messages. Wait just a sec.")
            await asyncio.sleep(5) # This allows the bot to sleep for a few seconds.

            # 12/29/20
            # Giving the bot the ability to delete all messages was an absolute pain.
            # Essentially, what I did was create an admin role on the server,
            # assign it to the bot,
            # and run the below function. 
            messages = message.channel.history(limit=10000)
            async for msg in messages:
                await msg.delete()

        elif msg == "/inspire":
            quote = get_quote()
            
############################################################################
client.run(TOKEN)

