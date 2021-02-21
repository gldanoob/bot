from datetime import datetime, timedelta
import discord
import util
import prefix
import reddit
import ids

groups = [
    "general", # 0
    "minecraft" # 1
]

# To create an instance:
# @Cmd(desc, usage, group)
# async def cmd_name(msg, arg1, arg2, ...):

class Cmd:
    def __init__(self, desc, usage, group):
        self.desc = desc
        self.usage = usage
        self.group = group

    def __call__(self, func):

        # Gives the commands this function instead
        async def wrapper(msg, *args, desc=False, usage=False):
            if desc:
                return self.desc
            if usage:
                return self.usage
            await func(msg, *args)

        # Mark the wrapper function as cmd (for distinguishing)
        wrapper.is_cmd = True
        return wrapper

# $help
@Cmd('Shows the help page', '', 0)
async def help(msg, *_):

    # Load commands and put into dict
    cmds_dict = {k: v for k, v in globals().items() if hasattr(v, 'is_cmd')}

    # Create Discord embed
    embed = discord.Embed(
        title="Help", description="can u just shut the fuck up", color=0x05ffe2)

    # Loop through each command, add the corresponding description + usage into the embed
    for i in cmds_dict:
        name = prefix.get() + i
        desc = await cmds_dict[i](None, desc=True)
        usage = await cmds_dict[i](None, usage=True)
        embed.add_field(
            name=name,
            value=f'{desc + chr(10)}Usage: `{name}{usage}`',
            inline=False
        )

    embed.set_footer(text="u lonely orphan")
    await msg.channel.send(embed=embed)

# $ping
@Cmd('Pings the fucking bot', '', 0)
async def ping(msg, *_):
    # Calculate the time difference between now and message timestamp
    now = datetime.utcnow()
    then = msg.created_at
    diff = now - then
    await msg.channel.send(f'{diff.microseconds // 1000} ms')
    await msg.channel.send("shut the fuck up nigga")

# $r
@Cmd('Sends a random reddit post of the subreddit', ' <subreddit>', 0)
async def r(msg, subreddit=None, *_):
    if subreddit is not None:
        while True:
            title, text, url = reddit.random(subreddit)
            print(url)
            if url.endswith('.png') or url.endswith(".jpg"):
                embed = discord.Embed(title=title, url=url, description=text)
                embed.set_image(url=url)
                await msg.channel.send(embed=embed)
                break

    else:
        await msg.channel.send("go succ ur own blacc dicc")

# $horny
@Cmd("Use this if you're too horny", "", 0)
async def horny(msg, *_):
    await msg.channel.send("<@" + str(msg.author.id) + "> おっ... \nおにいっ... お兄ちゃん～:heart:", 
    file=discord.File('assests/stare.jpg'))

# $serv
@Cmd('Changes MC server status (reserved for server op)', ' [on|off] (offset in mins)', 1)
async def serv(msg, status=None, offset=None, *_):

    # Only for server op
    if str(msg.author.id) not in ids.OP:
        return await msg.channel.send("お兄ちゃんじゃないの？")
    
    # Trim off milliseconds and change timezone
    time = msg.created_at.replace(microsecond=0) + timedelta(hours=8)

    # Output message depends on if offset time is specified
    on_msg = [
        "Server up :green_circle:",
        ":green_circle: Server goin online, cum",
        "Server went online :green_circle:"
    ] 

    off_msg = [
        "Server down :red_circle:",
        ":red_circle: Server goin down, time to head out guys",
        "Server went offline :red_circle:"
    ]


    msg_index = 0

    channel = util.get_channel(msg, ids.CHANNELS["SERVER_STATUS"])

    # Choose output message depending on time offset given
    if offset is not None:
        offset = int(offset)
        if offset > 0: msg_index = 1
        elif offset < 0: msg_index = 2

        offset = timedelta(minutes=offset)
        time += offset

    if status == "on":
        await channel.send(f'{on_msg[msg_index]} {chr(10)}Time: {time}')
        await channel.edit(topic="Status: :green_circle:")
    elif status == "off":
        await channel.send(f'{off_msg[msg_index]} {chr(10)}Time: {time}')
        await channel.edit(topic="Status: :red_circle:")

    # Delete the command message
    await msg.delete()