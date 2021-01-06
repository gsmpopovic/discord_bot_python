# Import mpdules
import os
import discord
from discord.ext import commands
#from dotenv import load_dotenv
import requests
import json
import random
import asyncio
from replit import db
########################################################################
#Load env variables
#DISCORD_TOKEN
#GUILD_NAME
#CLIENT_ID
#PUBLIC_KEY
#CLIENT_SECRET

#load_dotenv()

#Store token in a variable
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_NAME')

#Create an instance of our discord client
# A Client is an object that represents a connection to Discord. 
# A Client handles events, tracks state,
# and generally interacts with Discord APIs.
client = discord.Client()
bot = commands.Bot(command_prefix='!')
########################################################################

#Function declarations
@bot.command(name="quote", help="Will display a random quote.")
async def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_response = json.loads(response.text) 
    quote = ' Quote: ' + json_response[0]['q'] + ' - ' + json_response[0]['a']
    return quote

# greet_user greets user by name. 
# Takes as an argument 
# message.author.name (name of message sender)
@bot.command(name="greet", help="Greets user by name.")
async def greet_user(name):
    greeting = "Oh, hi there " + name + "!"
    return greeting

@bot.command(name="update_commands", help="Create new command based on user inputting a string--name of new command.")
async def update_commands(msg):
    new_command = msg.split("/newcmd ", 1)[1]  
    if "commands" in db.keys():
        commands = db["commands"]
        commands.append(new_command)
        db["commands"] = commands
        return new_command
    else:
        db["commands"] = ["commands"]

    

@bot.command(name="delete_commands", help="Will delete command based on user input--user input will be index of command to be deleted")
async def delete_commands(msg):
    commands = []
    if "commands" in db.keys():
      index = int(msg.split("/delcmd", 1)[1])
      print(index)
      # await delete_commands(index)
      commands = db["commands"]
      if len(commands) > index:
        del commands[index]
        db["commands"] = commands
      return commands
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

    if msg.startswith("/"):

        # commands = ["/greet", "/list", "/inspire", "/delete"]

        # options = commands

        # if "commands" in db.keys():

        #     options = options + db["commands"]

        # if any(command in msg for command in commands):
        #     await message.channel.send(random.choice(options))

        if msg.startswith("/newcmd"):

          new_command = await update_commands(msg)
            # new_command = msg.split("/newcmd ", 1)[1]
            # await update_commands(new_command)
            # await message.channel.send(f"New command '{new_command}' was created!")
          await message.channel.send(f"New command '{new_command}' was created!")

        if msg.startswith("/delcmd"):
            # commands = []
            # if "commands" in db.keys():
            #   index = int(msg.split("/delcmd", 1)[1])
            #   # await delete_commands(index)
            #   commands = db["commands"]
              commands = await delete_commands(msg)
              await message.channel.send("Okay. Here are all the commands I have left over: ")
              for item in commands:
                await message.channel.send(f"{item} {commands.index(item)}")

        if msg == "/greet":
            name = message.author.name
            greeting = await greet_user(name)
            await message.channel.send(greeting)
        
        elif msg == "/list":
            command_keys = db["commands"]

            if len(command_keys) > 0:
              for key in command_keys:
                  await message.channel.send(f"Command: {key}\n")
            else: 
              await message.channel.send("Oops. I don't have any commands as of yet!")


        elif msg == "/clear":
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
            quote = await get_quote()
            return quote 
            
############################################################################
client.run('Nzg5Mjk4NDczNzM1ODE1MTg3.X9wBfA.RtMMwbcw9goAx6IqzTNqIP5Xh-Q')

