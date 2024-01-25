import discord 
from discord.ext import commands
import datetime
import discord.ui
from discord.ui import View, Button, Select
import random

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.remove_command("help")


@bot.event
async def on_ready():
    print("The bot is now online")

@bot.command()
async def hello(ctx):
    username = ctx.message.author.name
    await ctx.send("Hii " + username)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner", "Pagato Normalmente", "I sottopagati")
async def ban(ctx, member:discord.Member, *,reason=None):
    if reason == None:
        reason = "This user was banned by " + ctx.message.author.name
    await member.ban(reason=reason)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner", "Pagato Normalmente", "I sottopagati")
async def kick(ctx, member:discord.Member, *,reason=None):
    if reason == None:
        reason = "This user was kicked by " + ctx.message.author.name
    await member.kick(reason=reason)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner", "Pagato Normalmente", "I sottopagati")
async def mute(ctx, member:discord.Member, timelimit):
    if "s" in timelimit:
        gettime = timelimit.strip("s")
        if int(gettime) > 2419000:
            await ctx.send("The time ammount cannot be bigger than 28days")
        else:
            newtime = datetime.timedelta(seconds=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    elif "m" in timelimit:
        gettime = timelimit.strip("m")
        if int(gettime) > 40320:
            await ctx.send("The time ammount cannot be bigger than 28days")
        else:
            newtime = datetime.timedelta(minutes=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    elif "h" in timelimit:
        gettime = timelimit.strip("h")
        if int(gettime) > 672:
            await ctx.send("The time ammount cannot be bigger than 28days")
        else:
            newtime = datetime.timedelta(hours=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    elif "d" in timelimit:
        gettime = timelimit.strip("d")
        if int(gettime) > 28:
            await ctx.send("The time ammount cannot be bigger than 28days")
        else:
            newtime = datetime.timedelta(days=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)
    elif "w" in timelimit:
        gettime = timelimit.strip("w")
        if int(gettime) > 4:
            await ctx.send("The time ammount cannot be bigger than 28days")
        else:
            newtime = datetime.timedelta(weeks=int(gettime))
            await member.edit(timed_out_until=discord.utils.utcnow() + newtime)

@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner", "Pagato Normalmente", "I sottopagati")
async def unmute(ctx, member:discord.Member):
    await member.edit(timed_out_until=None)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="This command displays all the commands available to use with this bot", color=0x02F0FF)
    embed.add_field(name="!ban", value="This command bans a user, must have moderator permission or higher", inline=False)
    embed.add_field(name="!kick", value="This command kicks a user, must have moderator permission or higher", inline=False)
    embed.add_field(name="!mute", value="This command mutes a user, must have moderator permission or higher", inline=False)
    embed.add_field(name="!unmute", value="This command unmutes a user, must have moderator permission or higher", inline=False)
    embed.add_field(name="!Ticket", value="This command opens a ticket if you need to talk with admins for everything", inline=False)
    embed.add_field(name="!cancelTicket", value="If you created a ticket, you close it", inline=False)
    embed.add_field(name="!Games", value="Use it for a complete list of the bot games", inline=False)
    embed.set_footer(text="This bot was made by Akai")
    await ctx.send(embed=embed)

@bot.command()
async def games(ctx):
    embed = discord.Embed(title="Help Games", description="This command displays all the games available", color=0x02F0FF)
    embed.add_field(name="!roulette", value="Use this for a Russian Roulette round, the lose is ... well, discover it by yourself", inline=False)
    embed.set_footer(text="This bot was made by Akai")
    await ctx.send(embed=embed)

async def ticketcallback(interaction):
    guild = interaction.guild
    role = discord.utils.get(guild.roles, name="Moderator")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False), 
        interaction.user: discord.PermissionOverwrite(view_channel=True), 
        role: discord.PermissionOverwrite(view_channel=True),
    }

    select  = Select(options=[
        discord.SelectOption(label="Help Ticket", value="01", emoji="✔️", description="This will open a help ticket"),
        discord.SelectOption(label="Other Ticket", value="02", emoji="❌", description="This will open a ticket in the other section")
    ])

    async def my_callback(interaction):
        if select.values[0] == "01":
            category = discord.utils.get(guild.categories, name="Tickets")
            channel = await guild.create_text_channel(f"{interaction.user.name}+ticket", category=category, overwrites=overwrites)
            await interaction.response.send_message(f"Created ticket - <#{channel.id}")
            await channel.send("Hello, how I help?")
        elif select.values[0] == "01":
            category = discord.utils.get(guild.categories, name="Tickets")
            channel = await guild.create_text_channel(f"{interaction.user.name}-ticket", category=category, overwrites=overwrites)
            await interaction.response.send_message(f"Created ticket - <#{channel.id}")
            await channel.send("Hello, write your problem and a mod will respond to you!")

    select.callback = my_callback
    view = View(timeout=None)
    view.add_item(select)
    await interaction.response.send_message("Choose an option below", view=view, ephemeral=True)

@bot.command()
async def ticket(ctx):

    button = Button(label="Create Ticket", style=discord.ButtonStyle.green)
    button.callback = ticketcallback
    view = View(timeout=None)
    view.add_item(button)
    await ctx.send("Open a ticket below", view=view)

@bot.command()
async def cancelTicket(ctx):
    
    username = ctx.message.author.name + "ticket"
    existChannel = discord.utils.get(ctx.guild.channels, name=username)
    if existChannel:
        await existChannel.delete()
    else:
        await ctx.send(f'No channel named, "{username}", was found')

@bot.command()
async def roulette(ctx):
    number = random.randint(1, 6)
    if(number == 3):
        await ctx.author.kick(reason="roulette")
        await ctx.send("He lost, what a loser")
    else:
        await ctx.send("You are safe .... this time")




bot.run('MTIwMDAyOTQ5NDU5Mzk4MjQ2NA.G6jRs-.bq-sK3gxRnNW2Vwaamfoar-QQEFte9_B1BqVWE')