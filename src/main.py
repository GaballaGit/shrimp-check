import discord
from discord import app_commands
import datetime
import random
import asyncio 
import os


# --------- Setting up ---------
print("discordpy version:", discord.__version__)

CLIENT_TOK = os.environ["BOT_TOKEN"]
GUILD = int(os.environ["SERVER_ID"])
CHAN = int(os.environ["CHANNEL_ID"])

MY_GUILD = discord.Object(id=GUILD)

intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
    user: discord.ClientUser

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

client = MyClient(intents=intents)

async def getChannel():
    chan = await client.fetch_channel(CHAN)
    return chan


# --------- users participating ---------
users = []
userNames = []
userChance = {}


# --------- messagepool --------- 
messagepool = [
    {"text": "shrimp check 🦐", "weight": 5},
    {"text": "posture check 👀", "weight": 5},
    {"text": "are you shrimping rn", "weight": 4},
    {"text": "unshrimp immediately", "weight": 3},
    {"text": "straighten up, noble vertebrate", "weight": 2},
    {"text": "your spine called. it’s tired.", "weight": 2},
    {"text": "this is a gentle posture intervention", "weight": 4},
    {"text": "back straight. jaw unclench.", "weight": 3},
    {"text": "if you're slouching, this is for you", "weight": 5},
    {"text": "this bot sees your posture and is disappointed", "weight": 1},
    {"text": "the shrimp energy is strong today", "weight": 1},
    {"text": "you are becoming a lowercase gremlin. stand up.", "weight": 1},
    {"text": "unacceptable spinal curvature detected", "weight": 1},
    {"text": "cease goblin mode", "weight": 2},
    {"text": "still here. still trying. good.", "weight": 4},
    {"text": "drop your shoulders", "weight": 4},
    {"text": "hydration check 💧", "weight": 5},
]
# --------- commands: --------- 

cmd_list = ["opt_in", "opt_out", "whos_in"]

# .when the bot loads 
@client.event
async def on_ready():
    print(client.user.name)
    for elm in cmd_list:
        print(f'[ \x1b[1;43m COMMAND \x1b[0m ]: {elm}')
        print()
    chan = await getChannel()
    client.loop.create_task(getTimeLoop(chan))

# .opt_int
@client.tree.command()
async def opt_in(interaction: discord.Interaction):

    if interaction.user in users:
        await interaction.response.send_message(f'You are already registered!')
    else:
        users.append(interaction.user)
        userNames.append(interaction.user.name)
        userChance[interaction.user.name] = 2
        await interaction.response.send_message(f'You have been opted in {interaction.user.mention}')

# .opt_out
@client.tree.command()
async def opt_out(interaction: discord.Interaction):
    try:
        users.remove(interaction.user)
        userNames.remove(interaction.user.name)
        del userChance[interaction.user.name]
        await interaction.response.send_message(f'You have been opted out {interaction.user.mention}')
    except ValueError:
        await interaction.response.send_message(f'You are not opted in {interaction.user.mention}!')


# .whos_in
@client.tree.command()
async def whos_in(interaction: discord.Interaction):
    if len(users) == 0:
        await interaction.response.send_message("No one is opted into shrimp checking!!")
    else:
        msg = ', '.join(str(name) for name in userNames)
        await interaction.response.send_message(msg)



# --------- background time ---------
async def getTimeLoop(chan: discord.abc.GuildChannel):
        while True:
            now = datetime.datetime.now()
            print(now)

            if len(users) != 0:
                chosen = random.choices(
                    [msg["text"] for msg in messagepool],
                    weights=[msg["weight"] for msg in messagepool],
                    k=1
                )[0]

                msg = chosen + " " +', '.join(f'{user.mention}' for user in users) + "\n\n-# React to the message to keep checking. You will automatically be opted out if you consecutively miss two!"
                message = await chan.send(msg)
                await message.add_reaction("✅")
                message = await chan.fetch_message(message.id)
                await asyncio.sleep(5 * 60)
                await checkReactions(message, chan)


            sleepTime = random.randint(20, 160)
            await asyncio.sleep(sleepTime * 60)


# --------- check ---------
async def checkReactions(message: discord.Message, chan: discord.abc.GuildChannel):
    for reaction in message.reactions:
        if str(reaction.emoji) == "✅":
               reaction_users = [user async for user in reaction.users() if not user.bot]
               for user in users:
                if user in reaction_users:
                   userChance[user.name] = 2
                else:
                    userChance[user.name] -= 1
                    if userChance[user.name] <= 0:
                        await chan.send(f'{user.mention} has been opted out for 2 missed reactions')
                        users.remove(user)
                        userNames.remove(user.name)
                        del userChance[user.name]


# --------- run ---------
client.run(CLIENT_TOK)



