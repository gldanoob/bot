import os
import sys
import traceback
import discord
from dotenv import load_dotenv
from threading import Thread

import cmds
import util
import prefix
import server



# Env tokens
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Config
PREFIX = '$'


client = discord.Client()


@client.event
# On ready
async def on_ready():

    print("\n\n")
    print(f'{client.user} started')

    await client.change_presence(activity=discord.Game(name="with ur blacc dicc"))

    # Search for the guild in env, assign 'guild' var
    guild = discord.utils.get(client.guilds, id=int(GUILD))
    print(f'Main guild: {guild.name}')



    # Display connected guilds
    print('-' * 50)
    print(f'Connected to:\n\n{chr(10).join(g.name for g in client.guilds)}')
    print('-' * 50)


@client.event
# When messaged
async def on_message(msg):
    # Don't send anything if the message is from the bot itself
    if msg.author == client.user:
        return

    # Reply to commands
    if msg.content.startswith(PREFIX):

        # list including the command name and args
        parsed = util.parse(msg.content[1:])

        # The command name and args list
        cmd, args = parsed[0], parsed[1:]

        # If command not found
        async def default(*_):
            await msg.channel.send("u blacc nigga no command matched")

        # Get the corresponding cmd function from cmds, run it
        cmd_func = getattr(cmds, cmd, default)
        await cmd_func(msg, *args)
        
def run_serv():
    server.app.run(
        host='0.0.0.0',
        port='3000'
    )

def run_bot():
    client.run(TOKEN)

if __name__ == "__main__":
    Thread(target = run_serv).start()
    run_bot()






