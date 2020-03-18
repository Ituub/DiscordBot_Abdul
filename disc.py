import discord
from discord.ext import commands
import markovify
import requests
from bs4 import BeautifulSoup as bs


bot = commands.Bot(command_prefix='$')


com = ("$hello - поздороваться\n"
      "$info - инфа о боте\n"
      "$joke - сгенерировать анекдот\n"
      "$dota+'имя героя' - инфа о герое")
res = ""
domain = 'baneksbest'
count = 1
token = "*токен бота*"
headers = {'accept': '*/*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}


with open("C://Users//Boss//PycharmProjects//freetime//posts.txt", "r", encoding="utf-8") as f:
    gen = f.read()

m = markovify.Text(gen)


@bot.event
async def on_ready():
    print('Готов работать', bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def dota(ctx, name: str):
    try:
        buffers = []
        x = "won"
        name = name.lower()
        urlbuff = "https://ru.dotabuff.com/heroes/" + name
        session = requests.Session()
        request = session.get(urlbuff, headers=headers)
        soup = bs(request.content, 'html.parser')
        if soup.find('span', attrs={'class': x}) == None:
            x = "lost"
        win_rate = soup.find('span', attrs={'class': x}).text
        pick_rate = soup.find('dd', attrs={'dd': ''}).text
        desc = soup.find('small', attrs={'small': ''}).text
        tbs = soup.find_all('tr', attrs={'tr': ''})
        for nam in tbs:
            en = nam.find('a', attrs={'class': 'link-type-hero'})
            if en != None:
                buffers.append(en.text)

        friends = str(buffers[0:9])
        enemies = str(buffers[10:len(buffers)])

        name = name.upper()

        embed = discord.Embed(title=name, description="герой " + desc, color=0xBD3520)

        embed.add_field(name="WinRate", value=win_rate)

        embed.add_field(name="Popularity", value=pick_rate)

        embed.add_field(name="Powerfull versus", value=friends)

        embed.add_field(name="Weak versus", value=enemies)

        await ctx.send(embed=embed)
    except Exception:
        await ctx.send("Кажется, вы неправильно указали имя героя.")


@bot.command()
async def joke(ctx):
    await ctx.send(m.make_short_sentence(300))


@bot.command()
async def hello(ctx):
    await ctx.send(":smiley: :wave: Здарова, маслы!")


@bot.command()
async def info(ctx):
    embed = discord.Embed(title="4 What?", description="Понятия не имею.", color=0xeee657)

    embed.add_field(name="Commands", value=com)

    embed.add_field(name="Author", value="SeldereIi#9465")

    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    embed.add_field(name="Users", value=f"{len(bot.users)}")

    await ctx.send(embed=embed)


bot.run(token)
