import os
import random
import discord
from discord.ext import commands
from discord.utils import get
import yt_dlp
import sqlite3
import buttons
from poker_configs import *

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="/", intents=intents)
CHANNEL_LINK = 1216341359556821093

# Настройка аудиоплеера
player = None

con = sqlite3.connect("data/poker_players.sqlite")
cursor = con.cursor()
some_dict = dict_cards


# Событие при подключении бота на сервер
@bot.event
async def on_ready():
    CHANNEL_LINK = 1231264616596639827
    channel = bot.get_channel(CHANNEL_LINK)
    await channel.send("""
        Привет, я бот Makson. Чтобы ознакомится с моими командами просто напиши /info
     
        """)


# команда инфо, которая предоставляет список всех команд бота
@bot.command()
async def info(ctx):
    await ctx.reply("""
    ```
    Спискок моих комманд:
    1./connect - команда, чтобы добавить меня в голосовой чат, в котором вы находитесь в данный момент.
    2. /play - команда, чтобы начать проигрывать музыку из youtube видео.
    3. /leave - команда, которая говорит мне выйти из голосового чата.
    4. /pause - команда, которая говорит мне остановить воспроизведение музыки.
    5. /poker - подключится к сессии для игры в покер.
    6. /startgame - начать сессию(игру).
    
    ```
    """)


# команда, бладгодаря которой бот переходит в канал, в котором находится пользователь.
@bot.command()
async def connect(ctx):
    try:
        voice = get(bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.reply("""
            ```Вас нет в голосовом чате, я не знаю куда подключится:)```
            """)
            return

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
    except AttributeError:
        await ctx.reply("""
        ```Вас нет в голосовом чате, я не знаю куда подключится:)```
        """)


@bot.command()
async def leave(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice:

        await voice.disconnect()
    else:
        await ctx.reply("""
        ```Я не подключен к голосовому чату```
        """)


@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice:
        if voice.is_playing():
            voice.pause()


        else:
            ctx.reply("""
            ```Я и так молчу (•ˋ _ ˊ•)```
            """)


# команда воспроизведения музыки
@bot.command()
async def play(message, url: str):
    voice = get(bot.voice_clients, guild=message.guild)
    if voice:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(id)s-%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        server = message.guild
        voice_channel = server.voice_client

        if voice_channel is None:
            voice_channel = await server.voice_client.channel.connect()

        audio_source = discord.FFmpegPCMAudio('downloads/' + info['id'] + '-' + info['title'] + '.mp3')
        voice_channel.play(audio_source)

    else:
        await message.reply("""
        ```Я не подключен к голосовому чату```
        """)


# ИГРА ПОКЕР

@bot.command()
async def poker(ctx):
    data = cursor.execute(f"SELECT * FROM session WHERE names='{ctx.author}'").fetchall()

    if data:
        await ctx.reply("```Вы уже внесены в сессию, напишите /start_session для начала игры.```")
        return
    await ctx.author.send(view=buttons.Buttons(), delete_after=10)
    await ctx.message.delete()


@bot.command()
async def startgame(ctx):
    global some_dict
    data = cursor.execute(f"SELECT names FROM session").fetchall()

    if len(data) < 2:
        await ctx.reply("```Недостаточно игроков, нужно хотябы 2```")
        return

    for name in list(data):
        user = discord.utils.find(lambda m: str(m) == f'{name[0]}', bot.users)
        pare = chosing_pare()
        cards_in_data(name[0], pare)
        await user.send(f"Ваши карты: {pare[0]}, {pare[1]}")
    table = chosing_table()
    await ctx.send(', '.join(list(table)))
    await ctx.send("```Победила дружба!```")
    some_dict = {
        '2': ['♥', '♣', '♠', '♦'],
        '3': ['♥', '♣', '♠', '♦'],
        '4': ['♥', '♣', '♠', '♦'],
        '5': ['♥', '♣', '♠', '♦'],
        '6': ['♥', '♣', '♠', '♦'],
        '7': ['♥', '♣', '♠', '♦'],
        '8': ['♥', '♣', '♠', '♦'],
        '9': ['♥', '♣', '♠', '♦'],
        '10': ['♥', '♣', '♠', '♦'],
        'J': ['♥', '♣', '♠', '♦'],
        'Q': ['♥', '♣', '♠', '♦'],
        'K': ['♥', '♣', '♠', '♦'],
        'A': ['♥', '♣', '♠', '♦']
    }


def cards_in_data(name, pare):
    cursor.execute("UPDATE session SET cards=? WHERE names=?", (str(', '.join(list(pare))), name))
    con.commit()


def chosing_table():
    while True:
        card = random.choices(list(some_dict.keys()), k=5)
        if (not some_dict[card[0]] or not some_dict[card[1]] or not some_dict[card[2]] or
                not some_dict[card[3]] or not some_dict[card[4]]):
            continue
        else:

            mast1 = random.choice(some_dict[card[0]])
            mast2 = random.choice(some_dict[card[1]])
            mast3 = random.choice(some_dict[card[2]])
            mast4 = random.choice(some_dict[card[3]])
            mast5 = random.choice(some_dict[card[4]])
            return card[0] + mast1, card[1] + mast2, card[2] + mast3, card[3] + mast4, card[4] + mast5


def chosing_pare():
    global some_dict

    while True:

        card = random.choices(list(some_dict.keys()), k=2)
        if not some_dict[card[0]] or not some_dict[card[1]]:
            continue
        else:

            mast1 = random.choice(some_dict[card[0]])
            mast2 = random.choice(some_dict[card[1]])
            del some_dict[card[0]][some_dict[card[0]].index(mast1)]
            del some_dict[card[1]][some_dict[card[1]].index(mast2)]

            return card[0] + mast1, card[1] + mast2


TOKEN = "MTIzMTI2NDg1Mzg5Nzc3NzI2NQ.G3hggZ.WBQrjayHNdGpsgmtWMNYG5b8Q2dG3dIQJdPKrE"
bot.run(TOKEN)
