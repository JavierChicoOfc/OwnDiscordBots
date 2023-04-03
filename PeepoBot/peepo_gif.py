import discord
import requests
import constants


client = discord.Client()

embedColour = 0xff0000
CommandKey = 'peepo '

TenorToken = constants.TenorToken
DiscordToken = constants.DiscordToken

#Retrieves GIF from site
def get_gif(searchTerm):  # PEP8: lower_case_names for functions
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
    

@client.event
async def on_ready():
    print(f"{client.user}"[:-5] + " is now Online!")

@client.event
async def on_message(message):
    if message.author == client.user:  # `if/else` doesn't need `()`
        return

    if message.content.lower().startswith(f"{CommandKey}gif"):
        gif_url = get_gif("peepo"+message.content.lower()[5:]) #Collects word after !gif
        
        embed = discord.Embed()
        embed.set_image(url=gif_url)
        await message.channel.send(embed=embed)

# Run

client.run(DiscordToken)