# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 2021

@author: MainStream
"""

#[Imports]
import discord      # Discord 
import requests     # Url Requests
import constants    # API DiscordToken & API TenorToken
import random       # Select random gif
import datetime     # Datetime

#[Create discord client]
client = discord.Client()

#[Command Key to call the bot]
CommandKey = 'peepo '

#[Tokens]
TenorToken = constants.TenorToken
DiscordToken = constants.DiscordToken

#[Returns a gif from Tenor]
def get_gif(searchTerm):
    response = requests.get("https://g.tenor.com/v1/search?q={}&key={}&limit=1".format(searchTerm, TenorToken))
    data = response.json()
    
    ''' 
    # see urls for all GIFs
    
    for result in data['results']:
        print('- result -')
        #print(result)
        
        for media in result['media']:
            print('- media -')
            print(media)
            print(media['gif'])
            print('url:', media['gif']['url'])
    '''  
    return data['results'][0]['media'][0]['gif']['url']
    
#[On ready]
@client.event
async def on_ready():
    print(f"{client.user}"[:-5] + " is now Online!")
    await client.change_presence(activity=discord.Streaming(name="peepo info",url="http://www.twitch.tv"))

#[On message]
@client.event
async def on_message(message):
    if message.author == client.user: 
        return

    #[Info]
    if message.content.lower().startswith(f"{CommandKey}info"):
        #[Nombre del servidor]
        embed= discord.Embed(title="Peepo Bot",
        description= "_*Peepo Bot*_ by MainStream", timestamp=datetime.datetime.utcnow(), color= discord.Color.green())
        embed.add_field(name=" Commands:",value="info -> botinfo \ngif *search*-> search a peepo gif\nClassic peepos:\nplay\nsad\nshy\nhappy\nclap\nclown\nchristmas\nexamine")
        
        #[Imagen de referencia]
        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1460652910291918853/ENWrdXy1_400x400.jpg")
        await message.channel.send(embed=embed)

    #[Gif]
    elif message.content.lower().startswith(f"{CommandKey}gif"):
        gif_url = get_gif("peepo"+message.content.lower()[5:]) #Collects word after !gif
        
        embed = discord.Embed()
        embed.set_image(url=gif_url)
        await message.channel.send(embed=embed)

    #[Info]
    elif message.content.lower().startswith(f"{CommandKey}play"):
        list_gifs = [
        'https://tenor.com/view/cozy-peepo-pepe-peepocozy-christmas-gif-24023628',
        'https://tenor.com/view/reikouwu2-gif-20327386',
        'https://tenor.com/view/hello-peepo-happy-wholesome-wave-gif-18532353',
        'https://tenor.com/view/peepo-peepo-hoodie-peepochakra-peepo-susanoo-gif-20324571',
        'https://tenor.com/view/peepo-juice-spin-pepojuicespin-juice-spin-peepo-spin-gif-19719206',
        ] 
        response = random.choice(list_gifs) # Random choice of a gif
        await message.channel.send(response) # Send it

    #[Shy]
    elif message.content.lower().startswith(f"{CommandKey}shy"):
        list_gifs = [
        'https://tenor.com/view/peepo-shy-peepo-shy-gif-20024644',
        'https://tenor.com/view/sleep-peeposh-twitch-peeposhy-peepo-gif-21766528',
        'https://tenor.com/view/shy-peepo-peeposhy-gif-19584894',
        'https://tenor.com/view/sad-peepo-sadpeepo-spending-time-without-your-favorite-streamer-heydoubleu-gif-18517365'
        ] 
        response = random.choice(list_gifs) # Random choice of a gif
        await message.channel.send(response) # Send it

    #[Happy]
    elif message.content.lower().startswith(f"{CommandKey}happy"):
        list_gifs = [
        'https://tenor.com/view/heydoubleu-studytogether-widepeepohappy-peepo-peepohappy-gif-18531858',
        'https://tenor.com/view/clapping-hands-pepe-the-frog-smile-happy-clap-gif-17745411',
        'https://tenor.com/view/heydoubleu-widepeepohappy-peepohappy-peepowave-gif-18488101',
        'https://tenor.com/view/peepo-happy-happy-dance-pepe-frog-gif-19259897'
        ] 
        response = random.choice(list_gifs) # Random choice of a gif
        await message.channel.send(response) # Send it

    #[Clap]
    elif message.content.lower().startswith(f"{CommandKey}clap"):
        list_gifs = [
        'https://tenor.com/view/clapping-hands-pepe-the-frog-smile-happy-clap-gif-17745411',
        'https://tenor.com/view/peepo-peepoclap-morais-clap-gif-14598361'
        ] 
        response = random.choice(list_gifs) # Random choice of a gif
        await message.channel.send(response) # Send it

    #[Sad]
    elif message.content.lower().startswith(f"{CommandKey}sad"):
        list_gifs = [
        'https://tenor.com/view/pepe-cry-reading-pepe-the-frog-sad-gif-17607942',
        'https://tenor.com/view/sadgecry-bttv-twitch-gif-22954193',
        'https://tenor.com/view/peeposad-gif-23538668',
        'https://tenor.com/view/hoyocagao-gif-20895153',
        'https://tenor.com/view/peeposad-peepo-sad-xoxo-cry-gif-17762910'
        ] 
        response = random.choice(list_gifs) # Random choice of a gif
        await message.channel.send(response) # Send it

    #[Clown]
    elif message.content.lower().startswith(f"{CommandKey}clown"):
        list_gifs = [
        'https://tenor.com/view/pepe-clown-nose-pepe-the-frog-gif-16275904',
        'https://tenor.com/view/pepe-peepo-clown-gif-20274804',
        'https://tenor.com/view/pepe-peepo-clown-gif-20274828',
        'https://tenor.com/view/pepe-peepo-clown-gif-20274792',
        'https://tenor.com/view/pepe-peepo-clown-gif-20274807'
        ] 
        response = random.choice(list_gifs) # Random choice of a gif
        await message.channel.send(response) # Send it

    #[Christmas]
    elif message.content.lower().startswith(f"{CommandKey}christmas"):
        list_gifs = [
        'https://tenor.com/view/peepochrist-peepochristmas-christmas-gif-19633437',
        'https://tenor.com/view/cozy-peepo-pepe-peepocozy-christmas-gif-24023628',
        'https://tenor.com/view/peepo-snow-widepeepo-gif-19114091'
        ] 
        response = random.choice(list_gifs) # Random choice of a gif
        await message.channel.send(response) # Send it

    #[Examine]
    elif message.content.lower().startswith(f"{CommandKey}examine"):
        list_gifs = [
        'https://tenor.com/view/peepo-d-peepo-gif-22780902',
        'https://tenor.com/view/pepo-g-peepo-gif-22945943',
        'https://tenor.com/view/peepo-snow-widepeepo-gif-19114091',
        'https://tenor.com/view/pepe-peepo-clown-gif-20274835'
        ] 
        response = random.choice(list_gifs) # Random choice of a gif
        await message.channel.send(response) # Send it

# [Run]
client.run(DiscordToken)