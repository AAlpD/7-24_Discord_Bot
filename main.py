import discord
from discord.ext import commands
from keep_alive import keep_alive
import os

intents = discord.Intents.all()
client = commands.Bot(command_prefix="\\", intents=intents)


def get_p(st, element, default):
    for parameter in st:
        if parameter.find(f"{element}=") == 0:
            st.remove(parameter)
            if element == "color":
                return parameter[len(element) + 1:], st
            else:
                return parameter[len(element) + 2:-1], st
    return default, st


def get_i(st, element):
    for parameter in st:
        if parameter.find(f"{element}(") == 0:
            index = st.index(parameter)
            del st[index]
            del st[index + 1]
            return st[index]
    return None


def get_f(st, element):
    for parameter in st:
        if parameter.find(f"{element}(") == 0:
            index = st.index(parameter)
            del st[index]
            for p in st:
                if p == ")":
                    f_index = st.index(p)
            del st[f_index]
            fp = st[index:f_index]
            inline = False
            for p in fp:
                if p.find("name=")==0:
                    name = p[6:-1]
                if p.find("value=")==0:
                    value = p[7:-1]
                if p.find("inline=")==0:
                    if p[7:] == "True":
                        inline = True
                    else:
                        inline = False
                    
            return [name, value, inline]


@client.event
async def on_ready():
    print(f"{client.user} çalışmaya hazır!")


@client.command()
async def embed(ctx, *, msg):
    if msg == "temp" or msg == "template":
        await ctx.send("https://Asistan.ahmetalpdogan.repl.co")
        return
    
    st = msg[3:-3].split("\n")

    title, st = get_p(st, "title", None)
    description, st = get_p(st, "description", "")
    color, st = get_p(st, "color", "2f3136")
    
    e = discord.Embed(title=title,
                      description=description,
                      color=int(color, 16))
    
    for parameter in st:
        if parameter.find("set_thumbnail") == 0:
            e.set_thumbnail(url=get_i(st, "set_thumbnail"))
                            
    for parameter in st:
        if parameter.find("set_image") == 0:
            e.set_image(url=get_i(st, "set_image"))
    
    while True:
        for parameter in st:
            if parameter.find("add_field(") == 0:
                [name, value, inline] = get_f(st, "add_field")
                e.add_field(name=name, value=value, inline=inline)
                continue
        break

    await ctx.message.delete()
    await ctx.send(embed=e)


@client.command()
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return


keep_alive()
client.run(os.environ['token'])
