from typing import TypedDict
import json
import discord

class Message(TypedDict):
    role: str
    content: str
    
def parseAutoGPTMessage(message: Message):
    """
    Initialize Discord message embedding
    """
    embed=discord.Embed(title=defineType(message["role"]),
                            url="",
                            description="",
                            color=discord.Color.purple())
    embed.set_author(name="", url="", icon_url="")
    embed.set_thumbnail(url="")

    try:
        parsed = json.loads(message["content"])
        
        """
        Base AutoGPT response formatter
        """
        if defineType(message["role"]) == "Response":
            embed.add_field(name=bold("Thoughts:"), value=parsed["thoughts"]["text"], inline=False)
            embed.add_field(name=bold("Reasoning:"), value=parsed["thoughts"]["reasoning"], inline=False)
            embed.add_field(name=bold("Plan:"), value=parsed["thoughts"]["plan"], inline=False)
            embed.add_field(name=bold("Criticism:"), value=parsed["thoughts"]["criticism"], inline=False)
            embed.add_field(name=bold("Command Name:"), value=parsed["command"]["name"], inline=False)

            command_args = parsed["command"]["args"]
            msg = ""
            for key, value in command_args.items():
                msg += f"{key}, {italic(value)}\n"
            embed.add_field(name=bold("Command Args:"), value=msg, inline=False)
        
        #TODO: Add other message types support
        else:
           embed.add_field(name="", value=message["content"], inline=False)

    except:
        embed.add_field(name="", value=message["content"], inline=False)
    
    return embed

#TODO: There has to be better mapping than this shit
def defineType(message: str) -> str:
    if(message == "ON_RESPONSE"):
        return "Response"
    elif(message == "ON_BOOT"):
        return "Welcome!"
    elif(message == "POST_PLANNING"):
        return "Post Planning"
    elif(message == "POST_INSTRUCTION"):
        return "Post Instruction"
    elif(message == "POST_COMMAND"):
        return "Post Command"
    elif(message == "REQUEST_INPUT"):
        return "Request Input"
    elif(message == "REPORT"):
        return "Report"
    elif(message == ""):
       return "Unknown Source"
    else:
        return message

def italic(txt):
    return '*' + txt +'*'

def bold(txt):
    return '**' + txt +'**'

def underline(txt):
    return '__' + txt +'__'

def strike(txt):
    return '~~' + txt +'~~'

def sl_blockquote(txt):
    return '\n> {}'.format(txt)

def ml_blockquote(txt):
    return '\n> {}'.format(txt)

def sl_code(txt):
    return '`' + txt + '`'

def ml_code(txt):
    return '```' + txt + '```'