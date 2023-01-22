import os
import re
import discord
import requests
import tweepy
from bs4 import BeautifulSoup

### .env Secrets
# Discord
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']
# Twitter
TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET = os.environ['TWITTER_API_SECRET']
TWITTER_BEARER_TOKEN = os.environ['TWITTER_BEARER_TOKEN']

### Inits
# Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_message(message):
    # Message contains an iFunny link
    if 'ifunny.co/' in message.content:

        # Extract the link from the message
        url = None
        words = message.content.split()
        for word in words:
            if word.startswith('https://ifunny.co/'):
                url = word
                break

        if url:
            # Send a request to the URL and retrieve the HTML
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers)
            html = response.text

            # Parse the HTML and extract the video link
            soup = BeautifulSoup(html, 'html.parser')
            video_element = soup.find('video')
            print(video_element)
            if video_element and 'data-src' in video_element.attrs:
                video_link = video_element['data-src']
                await message.channel.send(video_link)

    # Message contains an Twitter link
    if 'twitter.com/' in message.content:

        # Extract the link  from the message
        url = None
        words = message.content.split()
        for word in words:
            if word.startswith('https://twitter.com/'):
                url = word
                break

        if url:
            # Authenticate with the Twitter API
            auth = tweepy.OAuth2BearerHandler(TWITTER_BEARER_TOKEN)
            api = tweepy.API(auth)
            # Get the tweet
            try:
                match = re.search(r"status/(\d+)", url)
                if match:
                    url = match.group(1)
                    print("RegEx'ed tweet ID: " + url)
                # Check if the tweet has a media attachment
                tweet = api.get_status(url, tweet_mode='extended')
                media_entities = tweet.extended_entities.get('media', [])
                # Sift through the media attachments for a video
                for media in media_entities:
                    # Check if the media entity is a video
                    if 'video_info' in media:
                        video_url = media['video_info']['variants'][0]['url']
                        print(f'Video url: {video_url}')
                        print("Sending video.")
                        await message.channel.send(video_url)

            except tweepy.errors.NotFound:
                print("404 Tweet not found.")


client.run(DISCORD_TOKEN)
