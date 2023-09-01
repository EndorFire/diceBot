import os
import discord
import random
import re

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv("token")
GUILD = os.getenv("guild")

bot = commands.Bot(command_prefix=';')

symbols = ["+","-","*"]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    global guild 
    guild = discord.utils.get(bot.guilds, name=GUILD)

    # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(f'{bot.user} is connected to {guild.name}')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hello, {member.name} Welcome to {guild.name}")

@bot.event
async def on_message(message):
    if message.content.startswith(';'):
        mChannel = message.channel
        messageContent = "".join(message.content.split())
        messageContent = messageContent[1:]
        
        funcList = ["+"]
        for elem in messageContent:
            if (elem == "+" or elem =="-" or elem =="*"):
                funcList.append(elem)

        segments = re.split(r"\+|\-|\*", messageContent)

        finalTotal = 0
        outputString = ""
        iterCount = 0

        for x in segments:
            try: 
                int(x)
                finalTotal = eval(str(finalTotal)+funcList[iterCount]+str(x))
                outputString += f"\\{funcList[iterCount]}{x}"

            except:
                parts = x.split("d")
                if len(parts)<=1:
                    return ""
                numDice = 1
                numSides = 20
                results = []

                parts[0] = parts[0]
                if parts[0] == "":
                    numDice = 1
                else:
                    try:
                        numDice = int(parts[0])
                    except:
                        await mChannel.send("There was an error while reading your message. #1")
                        return
                
                if parts[1][0] == "a":
                    adv = True
                    parts[1] = parts[1][1:]
                else:
                    adv = False

                try:
                    numSides = int(parts[1])
                except:
                    await mChannel.send("There was an error while reading your message. #2")
                    return



                results = rollDiceFunc(numDice,numSides,adv)
                finalTotal = eval(str(finalTotal)+funcList[iterCount]+str(results[1])) #plus is changed to whatever is the correct formula
                outputString += results[0]
            iterCount+=1


        await mChannel.send(f"{finalTotal} \n> {message.content[1:]}: {outputString}")
        return

def rollDiceFunc(numDice,numSides,adv):
    results = "("
    total = 0
    if adv:
        for i in range(numDice):
            a = random.randint(1,numSides)
            b = random.randint(1,numSides)
            
            if a>b:   
                total+=a
                a = checkMax(a,numSides)
                results = results + a + " "
            else:
                total+=b
                b = checkMax(b,numSides)
                results = results + b + " "

    else:
        for i in range(numDice):
            a = random.randint(1,numSides)
            results = results + checkMax(a,numSides) + " "
            total += a

    results = results[:-1]
    results = results + ")"
    return [results, total]


def checkMax(num,numSides):
    if num == numSides:
        num = "**"+str(num)+"**"
        return str(num)
    else:
        return str(num)






bot.run(TOKEN)