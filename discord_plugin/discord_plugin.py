import discord
import os
from typing import TypedDict
from colorama import Fore
from discord.ext import tasks
from .discord_parser import parseAutoGPTMessage
import json
import time

description = "An AutoGPT discord bot that allows users to interact with their AutoGPT instance through discord."

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


BOT_TOKEN = ""
AUTHORIZED_USER_IDS = []
BOT_PREFIX = ""
CHANNEL_ID = ""

userReply = []
messagesToSend = []
waitingForReply = [False]

finishedLoggingIn = [False]

class Message(TypedDict):
    role: str
    content: str

class AutoGPT_Discord(discord.Client):

    async def on_ready(self):

        print(Fore.GREEN + f'Bot logged in as {self.user} (ID: {self.user.id})')
        print(Fore.GREEN + '------')
        finishedLoggingIn[0] = True

    async def setup_hook(self) -> None:
        self.background.start()
    

    @tasks.loop(seconds=1) 
    async def background(self):
        channel = self.get_channel(int(CHANNEL_ID))

        if len(messagesToSend) > 0:
            for message in messagesToSend:
                try:
                    embedmsg = parseAutoGPTMessage(message)
                    await channel.send(embed = embedmsg)
                except:
                    try:
                        await channel.send("```" + message["role"] + message["content"] + "```")
                    except:
                        await channel.send("A response from AutoGPT was failed to be parsed. Don't worry, this is not critical. However, if this error appears several times in a row, please ask for help. <3")
                messagesToSend.remove(message)
        
        if waitingForReply[0]:
            def check(m):
                return str(m.author.id) in AUTHORIZED_USER_IDS and m.channel == channel
        
            print(Fore.YELLOW + "Waiting for user to reply via discord...")
            user_input = await self.wait_for("message", check = check)
        
            print(Fore.GREEN + "User replied: " + user_input.content)

            await channel.send("--------------------------------------------------")
            await channel.send("You replied: " + user_input.content)

            userReply.append(user_input.content)

            waitingForReply[0] = False


    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if message.content.startswith(BOT_PREFIX + "shutdown") and str(message.author.id) in AUTHORIZED_USER_IDS:
            await message.reply("AutoGPT Shut Down!")
            os._exit(0)
        
        elif message.content.startswith(BOT_PREFIX + "shutdown"):
            await message.reply("You aren't authorized dummy >:(")

    @background.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


def required_info_set():
    global BOT_TOKEN
    global AUTHORIZED_USER_IDS
    global BOT_PREFIX
    global CHANNEL_ID
    global ASK_FOR_INPUT
    BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    authUsers = os.getenv("AUTHORIZED_USER_IDS")
    AUTHORIZED_USER_IDS = authUsers.split(",")
    BOT_PREFIX = os.getenv("BOT_PREFIX")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    ASK_FOR_INPUT = os.getenv("ASK_FOR_INPUT")

    return BOT_TOKEN and AUTHORIZED_USER_IDS and BOT_PREFIX and CHANNEL_ID and ASK_FOR_INPUT
    
def commandUnauthorized(feedback):
    return "This command was not authorized by the user. Do not try it again. Here is the provided feedback: " + feedback

def run_bot():
    global client
    
    client = AutoGPT_Discord(intents=intents)
    client.run(BOT_TOKEN)

def wait_for_user_input(name, args):
    arguments = ""
    
    #TODO: There has to be a bettter way to check this than this shitty if
    if "items" in args:
        for key, value in args.items():
            arguments += f"Argument name: {key} Argument value: {value}\n"

    messagesToSend.append(Message(role="", content="AutoGPT wants to run the command " + name + " with the arguments:\n" + arguments + "Reply with y for yes, n for no or feedback to give to the bot."))
    waitingForReply[0] = True

    while waitingForReply[0]:
        time.sleep(1)

    if userReply[0].lower() == "y":
        userReply.pop(0)
        return "Authorized"
    if userReply[0].lower() == "n":
        userReply.pop(0)
        return "Unauthorized"
    else:
        return userReply.pop(0)
