#################################################################

# Valrise Tookkit
import discord
from discord.ext.commands import cooldown, BucketType
from discord import Intents
from discord.ext import commands
import discord  # discord.py
from datetime import datetime, timezone, timedelta
from random import randint
import re
import math
import json
import requests
import random
# a discord bot for anything valrise
# need help? read the readme.md
# Galax & realdiegopoptart

#################################################################

bot_name = "Korwnaios"


#################################################################

server_ids = ['1084690016401367140', '1215021399417298944']

COMMANDCOOLDOWN_RATE = 1
COMMANDCOOLDOWN_PER = 12.0

#################################################################

secretJson = open('secret.json')
secret = json.load(secretJson)

client = discord.Bot(intents=Intents.all())

#################################################################

# auth
"""
request_auth_data = {"name":secret['connect.sid'],
    "password":secret['valrise_auth_sesh']}
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

session = requests.Session()
response = session.post("https://panel.valrisegaming.com/api/auth/rpg",
                        headers=headers, data=request_auth_data)

cookie = session.cookies.get_dict()

headers['cookie'] = cookie['connect.sid']

response_with_cookies = session.get(
    "https://panel.valrisegaming.com/api/auth/rpg", headers=headers)
"""


def auth_apikey():
    # return cookie['connect.sid']
    return secret[""]

# end of auth

#################################################################
# start of functions


def escapeName(name):
    # Remove all non-word characters (everything except numbers and letters) which is good to escape the name anyways
    name = re.sub(r"[^\w\s]", '', name)

    # Replace all runs of whitespace with a underscore
    name = re.sub(r"\s+", '_', name)

    return name


def getStaffRank(rankid):

    if rankid == "None":
        return "Player"
    if rankid == "0":
        return ""
    if rankid == "1":
        return "Helper"
    if rankid == "2":
        return "Moderator"
    if rankid == "3":
        return "Admin"
    if rankid == "4":
        return "Senior Admin"
    if rankid == "5":
        return "Manager"
    if rankid == "6":
        return "Server Leader"
    if rankid == "7":
        return "Community Manager"
    if rankid == "8":
        return "Community Owner"


def how_long_ago(api_provided):  # time is in CET(UTC+1, same as valrise)
    CET = timezone(timedelta(hours=1))

    date_str = f"{api_provided}"
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    hour = date_obj.hour
    minute = date_obj.minute
    second = date_obj.second

    target_date = datetime(year, month, day, hour, minute, second, tzinfo=CET)

    # calculate the time difference between now and the target date
    time_difference = datetime.now(timezone.utc) - target_date

    # convert the time difference to a human-readable format
    if time_difference.days > 0:
        return (f"{time_difference.days} day(s)")
    elif time_difference.seconds // 3600 > 0:
        return (f"{time_difference.seconds // 3600} hour(s)")
    elif time_difference.seconds // 60 > 0:
        return (f"{time_difference.seconds // 60} minute(s)")
    else:
        return ("just now")

#################################################################


@client.event
async def on_ready():
    print(f"[!] {bot_name} has loaded!\n[?] Shadow & Mark Korwnaios")


@client.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"Command on cooldown. Try again in {round(error.retry_after, 2)}s")
    else:
        raise error


@client.slash_command(guild_ids=server_ids, name="ping", description="Pong!")
async def ping(ctx):
    return await ctx.respond(f'Ping is {round(client.latency * 1000)}ms')


@client.slash_command(guild_ids=server_ids, name="help", description="Shows a list of bot commands.")
async def help(ctx):

    em = discord.Embed(title=bot_name, description="", color=0xC11D2F)

    em.add_field(name="/players",
                 value="Online players.")

    em.add_field(name="/stats",
                 value="View statistics of a player.")

    em.add_field(name="/search",
                 value="Find players with a keyword.")

    em.add_field(name="/korwnaios",
                 value="Find players with _Korwnaios.")

    em.add_field(name="/ping",
                 value="Pong!")

    em.add_field(name="/dog",
                 value="Random dog picture.")

    em.add_field(name="/duck",
                 value="Random duck picture.")

    em.add_field(name="/help",
                 value="Shows a list of bot commands.")

    em.set_footer(text="Requested by " + str(ctx.author.name) +
                  "#" + str(ctx.author.discriminator))

    await ctx.respond(embed=em)


@client.slash_command(guild_ids=server_ids, name="dog", description="Random dog picture.")
@commands.cooldown(COMMANDCOOLDOWN_RATE, COMMANDCOOLDOWN_PER, commands.BucketType.default)
async def dog(ctx):
    em = discord.Embed(title="Dogs", description="", color=0xC11D2F)
    url = requests.get(
        "https://dog.ceo/api/breeds/image/random").json()["message"]
    em.set_image(url=url)
    em.set_footer(text='Requested by %s' % (ctx.author), icon_url='')
    await ctx.respond(embed=em)


@client.slash_command(guild_ids=server_ids, name="duck", description="Random duck picture.")
@commands.cooldown(COMMANDCOOLDOWN_RATE, COMMANDCOOLDOWN_PER, commands.BucketType.default)
async def duck(ctx):
    num = randint(1, 114)
    em = discord.Embed(title="Ducks", description="", color=0xC11D2F)
    url = 'https://duckgroup.xyz/img/imagebot/duck/%d.jpg' % (num)
    em.set_image(url=url)
    em.set_footer(text='Duck #%d | Requested by %s' %
                  (num, ctx.author), icon_url='')
    await ctx.respond(embed=em)


@client.slash_command(guild_ids=server_ids, name="players", description="View online players. (Valrise Roleplay)")
@commands.cooldown(COMMANDCOOLDOWN_RATE, COMMANDCOOLDOWN_PER, commands.BucketType.default)
async def players(ctx):

    response = requests.get("https://panel-rpg.valrisegaming.com/api/rpg/general/online", headers={"Cookie": "connect.sid=" + auth_apikey(
    ), "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})

    em = discord.Embed(title="Online players", description="", color=0xC11D2F)

    for i in response.json():

        if i["donator"]:
            em.add_field(name=" [VIP] " + i["name"], value=f'{getStaffRank(
                str(i["admin"]))}\nOnline for {how_long_ago(i["online_since"])}\n')
        else:
            em.add_field(name=i["name"], value=f'{getStaffRank(
                str(i["admin"]))}\nOnline for {how_long_ago(i["online_since"])}\n')

    em.set_footer(text="Requested by " + str(ctx.author.name) +
                  "#" + str(ctx.author.discriminator))

    await ctx.respond(embed=em)


@client.slash_command(guild_ids=server_ids, name="stats", description="View statistics of a player. (Valrise Roleplay)")
@commands.cooldown(COMMANDCOOLDOWN_RATE, COMMANDCOOLDOWN_PER, commands.BucketType.default)
async def stats(ctx, *, args=None):

    typedplayer = args.lower()  # lowercase it
    typedplayer = escapeName(typedplayer)

    x = requests.get(f"https://panel-rpg.valrisegaming.com/api/rpg/user/{typedplayer}", headers={"Cookie": "connect.sid=" + auth_apikey(
    ), "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
    request_content = x.content

    PlayerInfo = json.loads(request_content)

    if 'error' in PlayerInfo:
        return await ctx.respond("Player not found, or you may have typed in their username incorrectly.")

    em = discord.Embed(
        title=PlayerInfo['name'] + "'s stats", description="", color=0xC11D2F)

    em.add_field(name="Name:",  # [links](https://discord.com)
                 value="[" + PlayerInfo['name'] + "](https://panel-rpg.valrisegaming.com/player/" + PlayerInfo['name'] + ")")

    em.add_field(name="Level:",
                 value=PlayerInfo['level'])

    em.add_field(name="Experince",
                 value=PlayerInfo['experience'])

    playerminutes = PlayerInfo['time_played'] / 60
    playerminutes = math.trunc(playerminutes)
    em.add_field(name="Playtime (minutes)",
                 value=str(playerminutes) + " minute(s)")

    playerhours = PlayerInfo['time_played'] / 3600
    playerhours = math.trunc(playerhours)
    em.add_field(name="Playtime (hours)",
                 value=str(playerhours) + " hour(s)")

    em.add_field(name="Account created",
                 value=str(PlayerInfo['created_at']).split('T')[0])

    if PlayerInfo["donate_level"] != 0:
        em.add_field(name="Donator",
                     value="Yes")

    if (PlayerInfo["user_ban"]):
        em.set_author(name="Banned for " + PlayerInfo['user_ban']['reason'] + " by: " + PlayerInfo['user_ban']['StaffUser']['name'], url="https://panel-rpg.valrisegaming.com/player/" +
                      PlayerInfo['name'], icon_url="https://panel-rpg.valrisegaming.com/api/assets/heads/" + str(PlayerInfo['user_ban']['StaffUser']['skin']) + ".png")
        # em.add_field(name="[!] This account is banned",
        # value= "Banned for " + PlayerInfo['user_ban']['reason'] + " by: " + PlayerInfo['user_ban']['StaffUser']['name'])

    if PlayerInfo['skin_job'] == 0:
        em.set_thumbnail(
            url="https://panel-rpg.valrisegaming.com/api/assets/heads/" + str(PlayerInfo['skin']) + ".png")
    else:
        em.set_thumbnail(url="https://panel-rpg.valrisegaming.com/api/assets/heads/" +
                         str(PlayerInfo['skin_job']) + ".png")

    if PlayerInfo['passport'] == 1:
        em.add_field(name="Passport", value="Yes")
    else:
        em.add_field(name="Passport", value="No")

    if PlayerInfo['license'] == 1:
        em.add_field(name="Drivers License", value="Yes")
    else:
        em.add_field(name="Drivers License", value="No")

    if PlayerInfo['2faEnabled'] == 1:
        em.add_field(name="2FA Enabled", value="Yes")
    else:
        em.add_field(name="2FA Enabled", value="No")

    em.set_footer(text="Requested by " + str(ctx.author.name) +
                  "#" + str(ctx.author.discriminator))

    await ctx.respond(embed=em)


@client.slash_command(guild_ids=server_ids, name="search", description="Search for a player. (Valrise Roleplay)")
@commands.cooldown(COMMANDCOOLDOWN_RATE, COMMANDCOOLDOWN_PER, commands.BucketType.default)
async def search(ctx, *, args=None):

    if len(args) < 3:
        return ctx.respond("You need at least 3 characters")

    matchingplayers = ""
    totalresults = 0

    x = requests.get(f"https://panel-rpg.valrisegaming.com/api/rpg/search/user/{args}", headers={"Cookie": "connect.sid=" + auth_apikey(
    ), "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
    request_content = x.content

    PlayerInfo = json.loads(request_content)

    em = discord.Embed(title="Valrise Gaming", description="", color=0xC11D2F)

    for i in PlayerInfo:
        matchingplayers += "[" + i['name'] + \
            "](https://panel-rpg.valrisegaming.com/player/" + \
            i['name'] + ")" + "\n"
        totalresults += 1

    em.add_field(name=str(totalresults) +
                 " Matching results for: " + args, value=matchingplayers)

    em.set_footer(text="Requested by " + str(ctx.author.name) +
                  "#" + str(ctx.author.discriminator))
    await ctx.respond(embed=em)


@client.slash_command(guild_ids=server_ids, name="korwnaios", description="See all korwnaios members. (Valrise Roleplay)")
@commands.cooldown(COMMANDCOOLDOWN_RATE, COMMANDCOOLDOWN_PER, commands.BucketType.default)
async def search(ctx):

    matchingplayers = ""
    totalresults = 0

    x = requests.get(f"https://panel-rpg.valrisegaming.com/api/rpg/search/user/_korwnaios", headers={"Cookie": "connect.sid=" + auth_apikey(
    ), "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"})
    request_content = x.content

    PlayerInfo = json.loads(request_content)

    em = discord.Embed(title="Valrise Gaming", description="", color=0xC11D2F)

    for i in PlayerInfo:
        matchingplayers += "[" + i['name'] + \
            "](https://panel-rpg.valrisegaming.com/player/" + \
            i['name'] + ")" + "\n"
        totalresults += 1

    em.add_field(name=str(totalresults) +
                 " Only a maximum of 10 can be shown", value=matchingplayers)

    em.set_footer(text="Requested by " + str(ctx.author.name) +
                  "#" + str(ctx.author.discriminator))
    await ctx.respond(embed=em)


@client.event
async def on_message(message):

    if "korwnaios" in message.content.lower():
        await message.channel.send('Gheaa')
    if "mark" in message.content.lower():
        await message.channel.send('hes retarded wtfff')

    if "locmax" in message.content.lower():
        await message.channel.send('fucking jew wtfff')

    if "benson" in message.content.lower():
     await message.channel.send('Fucking bad arab')

    if "valrise" in message.content.lower():
        await message.channel.send('this retarded tdm server still alive?')

    if "samp" in message.content.lower():
        await message.channel.send('samp is dead bro wtf')

    if "kacper" in message.content.lower():
        await message.channel.send('go to gym xd')

    if "dox" in message.content.lower():
        await message.channel.send('haram wtf')

client.run(secret["discord_bot_token"])
