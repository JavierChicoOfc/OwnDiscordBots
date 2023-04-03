# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 20:17:13 2020

@author: MainStream
"""

import discord
from discord.ext import commands
import datetime
from urllib import parse, request
import re
import random

from youtube_dl import YoutubeDL

# Introduce your discord token here. Get it from discord.com/developers
DISCORD_TOKEN = None

# [ Prefijo para llamar al bot ] 
bot = commands.Bot(command_prefix="%", description= "¿Stonks?") 

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

     #searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="skip", help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music()
# [----------------------Comandos----------------------]

# [ Ping ]
@bot.command()
async def ping(ctx):
    await ctx.send("pong")

# [ Info ]
@bot.command()
async def info(ctx):
    #[ Nombre del servidor ]
    embed= discord.Embed(title="StonksBot",
    description= "_*StonksBot*_ by MainStream", timestamp=datetime.datetime.utcnow(), color= discord.Color.purple())
    embed.add_field(name=" Commands:",value="info -> botinfo \nstonks -> stonks img \nnotstonks -> notstonks img\nyt _search_ -> search video\nmeme -> random stonk meme")
    
    #[ Imagen de referencia ]
    embed.set_thumbnail(url="https://i.kym-cdn.com/entries/icons/facebook/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg")
    
    #[ Envío del mensaje ]
    await ctx.send(embed=embed)

# [ Stonks ]
@bot.command()
async def stonks(ctx):
    embed= discord.Embed(color=discord.Color.blue())
    embed.set_image(url="https://i.kym-cdn.com/entries/icons/facebook/000/029/959/Screen_Shot_2019-06-05_at_1.26.32_PM.jpg")
    await ctx.send(embed=embed)

# [ NotStonks ]
@bot.command()
async def notstonks(ctx):
    embed= discord.Embed(color= discord.Color.red())
    embed.set_image(url="https://i.pinimg.com/originals/89/92/ba/8992ba8a5962114770ad9eb4d6be733c.jpg")
    await ctx.send(embed=embed)

# [ YT ] 
@bot.command()
async def yt(ctx, *, search):
    query_string = parse.urlencode({'search_query': search}) # Convierte el str "search" del usuario en formato búsqueda"
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string) # Genera un documento html con la info de la búsqueda
    search_results = re.findall(r'watch\?v=(\S{11})', html_content.read().decode()) # Extraigo el id de los videos
    await ctx.send("http://www.youtube.com/watch?v=" + search_results[0])

# [ StonksMeme ]
@bot.command(name='meme') 
async def randomMeme(ctx): 
    listGifs = [
        'https://media0.giphy.com/media/YnkMcHgNIMW4Yfmjxr/giphy.gif?cid=ecf05e47yvl4vcjip25539tslbojehmz3ocszorf4wibansx&rid=giphy.gif',
        'https://media2.giphy.com/media/Xf1ghvcjLrMn3O6Qe4/giphy.gif?cid=ecf05e47yvl4vcjip25539tslbojehmz3ocszorf4wibansx&rid=giphy.gif',
        'https://media3.giphy.com/media/jSDUHFqUtT07w8ersk/giphy.gif?cid=ecf05e47tb6rlbpkccgidr3ltuq02n7evmb1rylgzcvn4vca&rid=giphy.gif',
        "https://i.kym-cdn.com/photos/images/newsfeed/001/688/917/f1e.jpg",
        "https://i.kym-cdn.com/entries/icons/original/000/032/379/Screen_Shot_2020-01-09_at_2.22.56_PM.png",
        "https://i.kym-cdn.com/entries/icons/original/000/032/330/Screen_Shot_2020-01-06_at_12.12.46_PM.jpg",
        "https://i.kym-cdn.com/entries/icons/original/000/032/521/Screen_Shot_2020-01-21_at_1.59.19_PM.jpg",
        "https://i.kym-cdn.com/entries/icons/original/000/032/746/Screen_Shot_2020-02-06_at_3.21.18_PM.png",
        "https://i.kym-cdn.com/entries/icons/original/000/032/448/Screen_Shot_2020-01-15_at_1.25.29_PM.jpg",
        "https://i.kym-cdn.com/entries/icons/original/000/031/332/temp3.jpg",
        "https://i.kym-cdn.com/entries/icons/original/000/035/141/elevated-1.jpg",

    ] 
    response = random.choice(listGifs) # Seleccionamos un random de la lista
    await ctx.send(response) #Enviamos la respuesta

# [-----------------------Eventos-----------------------]

# [ Listo ]
@bot.event
async def on_ready():
    print("RDY")
    await bot.change_presence(activity=discord.Streaming(name="%info",url="http://www.twitch.tv"))


# [----------------------Ejecución----------------------]

bot.run(DISCORD_TOKEN)
